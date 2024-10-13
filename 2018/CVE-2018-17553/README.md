# CVE-2018-17553
CVE-2018-17553 PoC (Navigate CMS version 2.8 and prior)

This proof of concept was put together when working on the Black Pearl box from TCM.  I couldn't find anyone that put out a PoC other than just using Metasploit.  As I'm avoiding Metasploit in my hacking journey to then go back and do everything all over again with it, I whipped this together quickly for anyone else in the same boat.

This PoC assumes that you've already manually exploited CVE-2018-17552 to gain access (or have gained access in some other fashion).

I currently do not have the script performing any validation of your input or error checking of the results spit back out by cURL.  It's up to you to understand what you're doing and to put in a modicum of work if it fails.

Obviously, this requires that you have cURL installed on whatever machine you run this from.

The original intended use was to load a PHP webshell, but realistically, you can upload any file that will then become a PHP page.
