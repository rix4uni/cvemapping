# CVE-2019-15514
**Type:** Information Disclosure

**Affected Users, Versions, Devices:** All Telegram Users

Still not fixed/unpatched. [brute.py](brute.py) is available exploit written under python.

## Description
Suppose `ali` is hacktivist. His telegram user ID is `21788973` and mobile number is hidden. He lives in pakistan (+92).
We can add any user to contact by phone number. We will add phones numbers from range `+92-0000000000` to `+92-9999999999`.
So if any number successfully added and that user ID is `21788973`, that's mean `ali` number is successfully exposed !

**Note:** All above information supplied is hypothetical.

Remember, current example range was 9 digits long. We can reduce it more by social engineerring, sim code knowledge, password resets (specially gmail,paypal)...
The more low range, the more less time will it take.

## Background
This bug been exploited in wild from long. This appreciated us to investigate and open source its exploit for making telegram to patch it soon. 

## Proof Of Concept
### Generate wordlist:

Suppose, we have an telegram victim that number starts with `92313`, ends with `89` and in between there are `5` unknown digits 
We will generate all comibnations of number list within range `92313-xxxxx-89`. 

Use [num_gen.py](num_gen.py). It will write numbers to `92313xxxxx89.txt`. Before, must edit following:
- [prefix](num_gen.py#L1): a number should starts with. Here example, its `92313`
- [middle_range](num_gen.py#L2): total digits of unknown middle range. Here example, its `5`
- [suffix](num_gen.py#L3): a number should ends with. Here example, its `89`

### Brute force:
- [\*phone](brute.py#L2): insert your phone number including country code, without including spaces or +(plus)
- [\*api_id](brute.py#L3): create app and insert api id. [learn more](https://core.telegram.org/api/obtaining_api_id)
- [\*api_hash](brute.py#L4): create app and api hash. [learn more](https://core.telegram.org/api/obtaining_api_id)
- [\*numlist ](brute.py#L5): the path to your numbers list or wordlist
- [\*username_or_id](brute.py#L6): insert numeric id or username without `@` of victim. Better use [kotatogram](https://github.com/kotatogram/kotatogram-desktop/issues/274#issuecomment-997372621) as it supports showing user id in profile.

- [use_proxy](brute.py#L10): Enable or Disable proxy
- [proxy_server](brute.py#L11): domain or ip of proxy DNS
- [proxy_secret](brute.py#L12): hex encoded secret of proxy that serves as password
- [proxy_port](brute.py#L13): numeric port, mostly 443

- [should_resume](brute.py#L16): resume capability. whether to start from where numbers left ?
- [threads](brute.py#L17): # numbers to be tried on each try, don't increase else won't work
- [delay](brute.py#L18): delay in seconds on each try to lower telegram block time interval

#### Features:
1. multi-threaded i.e checks 19 numbers at time
2. resume capability
3. waits when blocked, time it waits equals to time telegram blocks 
4. accurate results

# Credits:
- [Telethon](https://github.com/LonamiWebs/Telethon) for providing easy library,[Telethon community](https://t.me/TelethonChat) for help about api usage
- [swagkarna](https://github.com/swagkarna/Telegram_User_Number_Finder) for inspiration
# I Love ALLAH + Holy Prophet + Islam and Pakistan.
