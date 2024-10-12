# CVE-2022-24818: Java Deserialization via Unchecked JNDI Lookups in GeoServer and GeoTools

The GeoTools library has a number of data sources that can perform unchecked JNDI lookups, which in turn can be used to perform class deserialization and result in arbitrary code execution.

As an example this can happen in GeoServer, but requires admin-level login to be triggered.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://github.com/geotools/geotools/security/advisories/GHSA-jvh2-668r-g75x).

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2022-24818/blob/main/GeoServer%20-%20CVE-2022-24818.pdf).

### Additional Resources:

[ysoserial](https://github.com/frohoff/ysoserial)
