# CVE-2016-3861

An extended version of Mark Brand's libutils exploit, from the Google Project Zero blog post: https://googleprojectzero.blogspot.com/2016/09/return-to-libstagefright-exploiting.html

Main differences:
* all of the mp4 files used for exploitation are generated in the browser dynamically
* comes with an 'extra_groom' option as certain AOSP builds in the 5-6 version regions require additional heap grooming

Does this actually work?
* yes, but it only gets PC control, and does nothing further
* I've only provided hard-coded addresses for one AOSP build that worked on a spare Nexus 5 I had lying around
* I've attempted this exploit on other phone models (e.g. Samsung), and the heap groom seems to be way different
* code is old, and comments aren't exactly fantastic

This was my first foray into browser exploits, and I really just wanted to see if I could do it. Really this just ended up being an exercise in learning mp4 parsing and some libmedia internals.
