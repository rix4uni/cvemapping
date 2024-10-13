# Live Networks LIVE555 streaming media RTSPServer lookForHeader code execution vulnerability
CVE-2018-4013
### Summary
An exploitable code execution vulnerability exists in the HTTP packet-parsing functionality of the LIVE555 RTSP server library. A specially crafted packet can cause a stack-based buffer overflow, resulting in code execution. An attacker can send a packet to trigger this vulnerability.

### Details
The LIVE555 Media Libraries are a lightweight set of multimedia streaming libraries for RTSP/RTCP/RTSP/SIP, with code support for both servers and clients. They are utilized by popular media players such as VLC and MPlayer, as well as a multitude of embedded devices (mainly cameras). This vulnerability is in the server component which interacts with these media players but does not impact the media players.

One of the functionalities enabled by LIVE555 for their standard RTSP server is the ability to tunnel RTSP over HTTP, which is served by a different port bound by the server, typically TCP 80, 8000, or 8080, depending on what ports are available on the host machine. This port can support normal RTSP, but in certain cases, the HTTP client can negotiate the RTSP-over-HTTP tunnel. The code that handles this feature is:

      // liveMedia/RTSPServer.cpp:607
      void RTSPServer::RTSPClientConnection::handleRequestBytes(int newBytesRead) {
      [...]
          // The request was not (valid) RTSP, but check for a special case: HTTP commands 
          // (for setting up RTSP-over-HTTP tunneling):
         char sessionCookie[RTSP_PARAM_STRING_MAX];  //[1]
         char acceptStr[RTSP_PARAM_STRING_MAX];          //[2]
                *fLastCRLF = '\0'; // temporarily, for parsing
                parseSucceeded = parseHTTPRequestString(cmdName, sizeof cmdName,
                            urlSuffix, sizeof urlPreSuffix,
                            sessionCookie, sizeof sessionCookie,
                            acceptStr, sizeof acceptStr);                        //[3]
As shown above at [3], the “Accept” and “x-sessioncookie” HTTP headers are what decide if it is an RTSP-over-HTTP tunnel or not. Thus, the parameters are read from the input bytes into the sessionCookie [1] and acceptStr [2] buffers on the stack (both of size 200), and then parsed further down.

The code path leads into the parseHTTPRequestString function:

      Boolean RTSPServer:: RTSPClientConnection::parseHTTPRequestString(char*     resultCmdName, unsigned resultCmdNameMaxSize,
      char* eurlSuffix, unsigned urlSuffixMaxSize,
      char* sessionCookie, unsigned sessionCookieMaxSize,
      char* acceptStr, unsigned acceptStrMaxSize) { 
      [...]
      lookForHeader("x-sessioncookie", &reqStr[i], reqStrSize-i, sessionCookie,   sessionCookieMaxSize);  // [1]
      lookForHeader("Accept", &reqStr[i], reqStrSize-i, acceptStr, acceptStrMaxSize); //[2]
The only really important things to note are that the char arrays from the parent function are once again passed into a new function directly at [1] (sessionCookie) and [2] (acceptStr). This leads into the lookForHeader function:

      static void lookForHeader(char const* headerName, char const* source, unsigned
                                sourceLen, char* resultStr, unsigned resultMaxSize) {
          resultStr[0] = '\0'; // by default, return an empty string
          unsigned headerNameLen = strlen(headerName);
          for (int i = 0; i < (int)(sourceLen-headerNameLen); ++i) {
              if (strncmp(&source[i], headerName, headerNameLen) == 0 && source[i+headerNameLen] == ':') { // [1]
              // We found the header. Skip over any whitespace, then copy the rest of the line to "resultStr":
              for (i += headerNameLen+1; i < (int)sourceLen && (source[i] == ' ' || source[i] == '\t'); ++i) {} 
              for (unsigned j = i; j < sourceLen; ++j) {          // [4]
                  if (source[j] == '\r' || source[j] == '\n') { // [2]
                  // We've found the end of the line. Copy it to the result (if it will fit):
                  if (j-i+1 > resultMaxSize) break;
                  char const* resultSource = &source[i];
                  char const* resultSourceEnd = &source[j];
                  while (resultSource < resultSourceEnd) *resultStr++ = *resultSource++; // [5]
                  *resultStr = '\0';
                  break; //[3]
                  }
              }
              }
          }
      }
The outermost loop iterates over our input bytes until the headerName is found. In the case of this program, it continuously looks for “Accept:” and “x-sessioncookie:” with strncmp at [1]. As the comment notes, another loop skips over any whitespace found, and then starts to look for the expected newline chars ‘\r\n’ at [2]. After this, the program correctly limits the size of the copy to resultMaxSize, which is correctly set to 0xc8 (200) on both calls into this function.

After the copy, the break at [3] is hit, which only actually breaks out of the loop at [4], causing the code to jump back to the initial strncmp loop that was mentioned above. Thus, if there’s another “Accept:” or “x-sessioncookie” string within the buffer, the copy again takes place, and if we examine the actual method of copying at [5], we can see that our initial pointer (that’s pointing to an address in the stack frame of the handleRequestBytes function) continues to increment, and while the length of any given copy is limited to the size of the buffer, when there’s no limit on the amount of copies that can occur on an ever increasing destination address, a stack-based buffer overflow can be easily triggered.

      Crash Output
      ==38574==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffffffd878 at pc 0x555555aad1fb bp 0x7fffffffced0 sp 0x7fffffffcec8
      WRITE of size 1 at 0x7fffffffd878 thread T0 
      #0 0x555555aad1fa in lookForHeader /root/boop/work_work/triages/live555/live/liveMedia/RTSPServer.cpp:398
      #1 0x555555aad847 in RTSPServer::RTSPClientConnection::parseHTTPRequestString(char*, unsigned int, char*, unsigned int, char*, unsigned int, char*, unsigned int) /root/boop/work_work/triages/live555/live/liveMedia/RTSPServer.cpp:479
      #2 0x555555ab82ac in RTSPServer::RTSPClientConnection::handleRequestBytes(int) /root/boop/work_work/triages/live555/live/liveMedia/RTSPServer.cpp:828
      #3 0x555555aa9c17 in GenericMediaServer::ClientConnection::incomingRequestHandler() /root/boop/work_work/triages/live555/live/liveMedia/GenericMediaServer.cpp:246
      #4 0x555555e0063b in BasicTaskScheduler::SingleStep(unsigned int) /root/boop/work_work/triages/live555/live/BasicUsageEnvironment/BasicTaskScheduler.cpp:153
      #5 0x555555e12c75 in BasicTaskScheduler0::doEventLoop(char volatile*) /root/boop/work_work/triages/live555/live/BasicUsageEnvironment/BasicTaskScheduler0.cpp:80
      #6 0x555555a9452c in main /root/boop/work_work/triages/live555/live/mediaServer/live555MediaServer.cpp:89
      #7 0x7ffff550b2b0 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x202b0)
      #8 0x555555a978e9 in _start (/root/boop/work_work/triages/live555/live555MediaServer+0x5438e9)

      Address 0x7fffffffd878 is located in stack of thread T0 at offset 2024 in frame
      #0 0x555555ab6b9f in RTSPServer::RTSPClientConnection::handleRequestBytes(int) /root/boop/work_work/triages/live555/live/liveMedia/RTSPServer.cpp:607

      This frame has 12 object(s):
      [32, 33) 'reuseConnection'
      [96, 97) 'deliverViaTCP'
      [160, 164) 'contentLength'
      [224, 232) 'proxyURLSuffix'
      [288, 488) 'cmdName'
      [544, 744) 'urlPreSuffix'
      [800, 1000) 'urlSuffix'
      [1056, 1256) 'cseq'
      [1312, 1512) 'sessionIdStr'
      [1568, 1768) 'sessionCookie'
      [1824, 2024) 'acceptStr' <== Memory access at offset 2024 overflows this variable
      [2080, 2480) 'urlTotalSuffix'
      HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
      SUMMARY: AddressSanitizer: stack-buffer-overflow /root/boop/work_work/triages/live555/live/liveMedia/RTSPServer.cpp:398 in lookForHeader
      Shadow bytes around the buggy address:
      0x10007fff7ab0: f4 f4 f2 f2 f2 f2 00 00 00 00 00 00 00 00 00 00
      0x10007fff7ac0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f4
      0x10007fff7ad0: f4 f4 f2 f2 f2 f2 00 00 00 00 00 00 00 00 00 00
      0x10007fff7ae0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f4
      0x10007fff7af0: f4 f4 f2 f2 f2 f2 00 00 00 00 00 00 00 00 00 00
      =>0x10007fff7b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00[f4]
      0x10007fff7b10: f4 f4 f2 f2 f2 f2 00 00 00 00 00 00 00 00 00 00
      0x10007fff7b20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x10007fff7b30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x10007fff7b40: 00 00 00 00 00 00 00 00 f4 f4 f3 f3 f3 f3 00 00
      0x10007fff7b50: 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1 00 00

## CREDIT
Discovered by Lilith ¯\_(ツ)_/¯ of Cisco Talos.
