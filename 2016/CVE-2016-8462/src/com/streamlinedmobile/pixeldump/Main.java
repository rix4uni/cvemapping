package com.streamlinedmobile.pixeldump;

import org.usb4java.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.IntBuffer;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;

public class Main {

    //Pixel Fastboot IDs
    private static short VENDOR_ID = 0x18d1;
    private static short PRODUCT_ID = 0x4ee0;

    //Fastboot interface and endpoints
    private static int INTERFACE_NUMBER = 0;
    private static byte IN_ENDPOINT = (byte)0x81;
    private static byte OUT_ENDPOINT = 0x01;

    private static Device device = null;
    private static DeviceHandle handle = null;
    private static DeviceList list = null;

    private static int result = 0;
    private static int attached = -1;

    private static int TIMEOUT = 10000;

    private static boolean DEBUG = false;
    private static File output =null;


    public static void main(String[] args) throws NoSuchAlgorithmException {

        if (args.length != 2) {
            print("java -jar PixelDump.jar <partition> <outputfile>");
            return;
        }

        String command = "oem sha1sum " + args[0];
        String partitionName = args[0];
        output = new File(args[1]);

        //Connect to pixel
        connect();

        String sha1Sum = null;
        int partSize = 0;
        int curOffset = 0x1;

        write(command.getBytes(), false);
        String[] resp = read();

        for (String s: resp) {

            if (s.length() == 44) {
                sha1Sum = s.substring(4);
                print(partitionName + " sha1sum: " + sha1Sum);
            } else if (s.contains("partition") && s.contains("offset") && s.contains("size") && s.contains("Hash")) {
                partSize = Integer.parseInt(s.split(" ")[2].substring(7), 16);
                print(partitionName + " size: " + partSize);
            }
        }

        byte[] partition = new byte[0];
        byte[] holder = new byte[0];
        print("Progress:");
        while (curOffset <= partSize) {

            holder = new byte[partition.length + 1];
            System.arraycopy(partition,0,holder,0,partition.length);

            write((command + " " + curOffset).getBytes(), false);

            String[] r = read();

            String newHash = null;
            for (String s: r) {
                if (s.length() == 44) {
                    newHash = s.substring(4);
                }
            }

            while (true) {
                String holderHash=bytesToHex(SHAsum(holder)).trim();
                if (newHash.trim().equals(holderHash)) {
                   // System.out.print(bytesToHex(new byte[]{holder[holder.length -1]}));

                    if (curOffset % 5 == 0) {
                        print(Integer.toString(curOffset) + "/" + Integer.toString(partSize) + "bytes");
                    }
                    break;
                }
                holder[holder.length-1] = (byte)((holder[holder.length-1] + (byte) 0x01));
            }

            partition = holder;
            curOffset++;
        }
        System.arraycopy(partition,0,holder,0,partition.length);

        try {
            FileOutputStream fos = new FileOutputStream(output);
            fos.write(partition);
            fos.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }


        print("File written to " + output.getAbsolutePath());


        //Disconnect from phone
        disconnect();

    }

    public static boolean write(byte[] cmd,boolean readResponse) {
        boolean success = false;

        ByteBuffer buffer = ByteBuffer.allocateDirect(cmd.length);
        buffer.put(cmd);
        IntBuffer transferred = IntBuffer.allocate(1);

        int result = LibUsb.bulkTransfer(handle, OUT_ENDPOINT, buffer, transferred, TIMEOUT);
        if (result != LibUsb.SUCCESS) {
            throw new LibUsbException("Control transfer failed", result);
        }
        //  System.out.println(transferred.get() + " bytes sent");
        success = true;

        if (readResponse) {

            for (String s : read()) {
                System.out.println(s);
            }
        }
        return success;
    }
    private static byte[] readRaw() {
        byte[] out = null;

        ByteBuffer buffer2 = BufferUtils.allocateByteBuffer(1024).order(
                ByteOrder.LITTLE_ENDIAN);
        IntBuffer transferred = BufferUtils.allocateIntBuffer();
        result = LibUsb.bulkTransfer(handle, IN_ENDPOINT, buffer2,
                transferred, TIMEOUT);
        if (result != LibUsb.SUCCESS)
        {
            throw new LibUsbException("Unable to read data", result);
        }

        out = new byte[buffer2.remaining()];
        buffer2.get(out);


        return out;

    }
    public static String[] read() {

        List<String> output = new ArrayList<String>();

        output.add(new String(readRaw()).trim());


        while (true) {
            if (output.get(output.size()-1).startsWith("OKAY") || output.get(output.size()-1).startsWith("FAIL")) {
                break;
            }
            output.add(new String(readRaw()).trim());
        }

        String[] out = new String[output.size()];
        out = output.toArray(out);

        return out;
    }

    public static boolean connect() {
        boolean success = false;
        System.out.println("Connecting to " + Short.toString(VENDOR_ID) + ":" + Short.toString(PRODUCT_ID));

        result = LibUsb.init(null);
        if (result != LibUsb.SUCCESS) {
            throw new LibUsbException("Unable to initialize libusb.", result);
        }

        list = new DeviceList();
        result = LibUsb.getDeviceList(null, list);
        if (result < 0) {
            throw new LibUsbException("Unable to get device list", result);
        }

        for (Device d: list) {
            DeviceDescriptor descriptor = new DeviceDescriptor();
            result = LibUsb.getDeviceDescriptor(d, descriptor);
            if (result != LibUsb.SUCCESS) {
                throw new LibUsbException("Unable to read device descriptor", result);
            }
            if (descriptor.idVendor() == VENDOR_ID && descriptor.idProduct() == PRODUCT_ID) {
                System.out.println("Found device " + Short.toString(descriptor.idVendor()) + ":" + Short.toString(descriptor.idProduct()));
                device = d;
            }
        }

        if (device == null) {
            System.out.println("Device not found");
            return success;
        } else {
            handle = new DeviceHandle();
            result = LibUsb.open(device,handle);
            if (result != LibUsb.SUCCESS) {
                throw new LibUsbException("Unable to open USB device", result);
            }

            attached = LibUsb.kernelDriverActive(handle, INTERFACE_NUMBER);
            if (attached < 0)
            {
                throw new LibUsbException(
                        "Unable to check kernel driver active", result);
            }

            result = LibUsb.detachKernelDriver(handle, INTERFACE_NUMBER);
            if (result != LibUsb.SUCCESS &&
                    result != LibUsb.ERROR_NOT_SUPPORTED &&
                    result != LibUsb.ERROR_NOT_FOUND)
            {
                throw new LibUsbException("Unable to detach kernel driver",
                        result);
            }

            result = LibUsb.claimInterface(handle, INTERFACE_NUMBER);
            if (result != LibUsb.SUCCESS)
            {
                throw new LibUsbException("Unable to claim interface", result);
            }

            success = true;
            System.out.println("Connected");
        }

        return success;
    }

    public static boolean disconnect() {
        boolean success = false;
        System.out.println("Disconnecting");
        // Release the interface
        result = LibUsb.releaseInterface(handle, INTERFACE_NUMBER);
        if (result != LibUsb.SUCCESS)
        {
            throw new LibUsbException("Unable to release interface",
                    result);
        }

        // Re-attach kernel driver if needed
        if (attached == 1)
        {
            LibUsb.attachKernelDriver(handle, INTERFACE_NUMBER);
            if (result != LibUsb.SUCCESS)
            {
                throw new LibUsbException(
                        "Unable to re-attach kernel driver", result);
            }
        }

        LibUsb.close(handle);
        LibUsb.freeDeviceList(list, true);
        LibUsb.exit(null);
        System.out.println("Disconnected");

        return success;
    }

    public static String bytesToHex(byte[] bytes) {
        char[] hexArray = "0123456789abcdef".toCharArray();
        char[] hexChars = new char[bytes.length * 2];
        for ( int j = 0; j < bytes.length; j++ ) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = hexArray[v >>> 4];
            hexChars[j * 2 + 1] = hexArray[v & 0x0F];
        }
        return new String(hexChars);
    }


    public static byte[] SHAsum(byte[] convertme) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        return md.digest(convertme);
    }


    public static void print(String msg) {
        System.out.println("[+]\t" + msg);
    }

    public static void printDebug(String msg) {
        if (DEBUG) {
            System.out.println("[\uD83D\uDC1E]\t" + msg);
        }
    }
}
