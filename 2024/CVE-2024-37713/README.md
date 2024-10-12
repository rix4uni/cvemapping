
# CVE-2024-37713

## Summary
> An issue in Dewmobile, Inc Zapya Android App allows a remote attacker to execute arbitrary code via the open ports of the device.


## Target
> Dewmobile, Inc. Zapya Android App(https://play.google.com/store/apps/details?id=com.dewmobile.kuaiya.play)


## Details
> On all devices with the Zapya app installed, port 9876 remains open at all times, regardless of the user's intention. Because this open service lacks any authentication process, anyone, including attackers, can access the device through port 9876.


## Impact 
> External Port Opening, Incorrect Access Control, System/Resource Access capability


## Discoverer
> Kwon Youngwoo(fullbbadda1208)
