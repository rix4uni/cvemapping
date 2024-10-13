# CVE-2019-17564 FastJson + SpringFramework Gadget for Dubbo 2.7.3
Our full write-up is available at https://www.checkmarx.com/blog/apache-dubbo-unauthenticated-remote-code-execution-vulnerability

Note that *this is not an exploit*; it is a POC gadget chain used in an exploit used to demonstrate deserialization in scopes containing certain dependencies.

# Overview
Basic code for creating the Alibaba FastJson + Spring gadget chain, as used to exploit Apache Dubbo in CVE-2019-17564. This code will print, and locally deserialize, a gadget based on dependencies available in the scope of Dubbo 2.7.3, Dubbo Common 2.7.3, and Spring Framework 

# Gadget Chain Structure
1.	HashMap.putVal(h,k,v)
    a.	The result of hashCode(), h, is identical for HotSwappableTargetSource objects, triggering a deeper equals() call on HashMap keys when a second value is inserted
2.	HotSwappableTargetSource.equals()
3.	XString.equals()
4.	com.alibaba.fastjson.JSON.toString()
5.	com.alibaba.fastjson.JSON.toJSONString()
6.	com.alibaba.fastjson.serializer.MapSerializer.write()
7.	TemplatesImpl.getOutputProperties()
8.	TemplatesImpl.newTransformer()
9.	TemplatesImpl.getTransletInstance()
10.	TemplatesImpl.defineTransletClasses()
11.	ClassLoader.defineClass()
12.	Class.newInstance()
13.	MaliciousClass.<clinit>()
14.	Runtime.exec()

# Credits
Credits are in order to Chris Frohoff and Moritz Bechler for their research and tools (ysoserial and marshalsec), as some of their code was used in the gadget chain, and their research laid the foundation for this exploit.

Credits are also in order to Checkmarx, who enable this type of research, and our fantastic research group for pitching ideas, reviewing, and bearing the fact that I won't shut up about this type of stuff.
