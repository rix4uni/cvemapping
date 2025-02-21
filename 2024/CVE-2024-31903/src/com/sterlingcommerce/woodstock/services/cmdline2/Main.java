package com.sterlingcommerce.woodstock.services.cmdline2;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class Main {
    public static void main(String[] args) throws Exception {
        if(args.length < 2) {
            System.err.println("Usage: Main <cmdLine> <outfile_or_SEND> [host] [port]");
            System.exit(1);
        } else {
            System.out.println("[+] Creating object...");
        }

        CmdLine2Parms cmdLine2Parms = new CmdLine2Parms();
        cmdLine2Parms.cmdLine = args[0];
        // cmdLine2Parms.workingDir = "/tmp/";
        cmdLine2Parms.useOutput = false;
        cmdLine2Parms.debug = true;
        cmdLine2Parms.wait = false;
        cmdLine2Parms.useInput = false;

        boolean savetoFile = !args[1].equals("SEND");
        if(savetoFile){
            String filename = args[1];
            try (FileOutputStream fileOutputStream = new FileOutputStream(filename)){
                ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
                objectOutputStream.writeObject(cmdLine2Parms);
                objectOutputStream.flush();
                objectOutputStream.close();
                System.out.println("[+] Saved object to "+filename);
                System.exit(0);
            } catch (IOException e) {
                e.printStackTrace();
                System.exit(5);
            }
        }else{
            if(args.length < 4) {
                System.err.println("Provide [host] and [port] to send to!");
                System.exit(2);
            }
            String host = args[2];
            int port = Integer.parseInt(args[3]);
            System.out.printf("[+] Sending object to %s:%d...\n",host,port);
            try (Socket s = new Socket(host,port)){
                ObjectOutputStream oos = new ObjectOutputStream(new BufferedOutputStream(s.getOutputStream()));
                oos.writeObject(cmdLine2Parms);
                oos.flush();
                System.out.println("[+] ...Sent!");
            
                System.out.println("[+] Receiving header...");
                BufferedInputStream bis = new BufferedInputStream(s.getInputStream());
                ObjectInputStream ois = new ObjectInputStream(bis);
                String header = (String) ois.readObject();
                System.out.printf("[+] ...header received: %s\n",header);

                if(header.equals("RESULT")){
                    System.out.println("[+] Receiving result...");
                    CmdLine2Result clr = (CmdLine2Result) ois.readObject();
                    System.out.println("[+] Result received:");
                    System.out.println(clr.toString());

                    System.out.printf("[+] clr.statusRpt:       %s\n", clr.statusRpt != null ? clr.statusRpt : "null");
                    System.out.printf("[+] clr.exceptionString: %s\n", clr.exceptionString != null ? clr.exceptionString.toString() : "null");
                    System.out.printf("[+] clr.somethingToLog:  %s\n", clr.somethingToLog !=null ? clr.somethingToLog.toString() : "null");
                } else {
                    System.err.printf("[!] Non-RESULT header received: %s. Exiting...\n", header);
                }
            } catch (IOException e) {
                e.printStackTrace();
                System.exit(4);
            }


        }

    }
}
