<img width="1086" alt="cb_thumbnail" src="https://github.com/morganwdavis/overread/assets/4434533/8247adfa-0fbb-43f7-a185-babd4a619ad0">

# overread
**Simulates CVE-2023-4966 Citrix Bleed overread bug**

This is my final project for [Harvard CS50 Cybersecurity 2023](https://cs50.harvard.edu/cybersecurity/2023/).  It's about a bug. A small bug – with huge, ongoing consequences. In this presentation, I’ll be sharing the “bleeding insights” from one developer’s tiny mistake. A mistake that continues to cause big problems for potentially millions of people.

## Video
[Citrix Bleed Video on YouTube](https://youtu.be/7rLOzA3lf6s)

Recorded December 4, 2023

## Notes

This demonstration program in C makes a call to `snfprintf()` in a way that forces it to truncate the output.  It then attempts to actually overread a memory buffer to show how the CVE-2023-4966 exploit works.

Depending on your compiler and the size of the buffers used here, `malloc()` might introduce page-alignment padding which could break the demonstration. The constants I use are chosen so the output fits on one terminal display screen. Changing them can cause the results to differ and might not demonstrate the issue at all.

## Output
<img width="1197" alt="Screenshot 2023-12-11 131451" src="https://github.com/morganwdavis/overread/assets/4434533/49c4e780-eb82-41af-8abc-20243026feb1">
