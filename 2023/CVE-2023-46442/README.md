# CVE-2023-46442_POC

# Environment: Java 8

POC for CVE-2023-46442, Denial of Service vulnerability found within Soot before 4.4.1 under Java 8

When retrieving the body of a maliciously crafted method, a very small size class file or method can cause

huge resource consumption and loop forever until a OutOfMemory is reached(depending on JVM settings)

src/main/java/POC.java -> example vulnerable program

src/main/resources/Build$Builder.class -> example class file that can cause DoS/Indefinte loop(attack payload)



