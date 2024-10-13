# CVE-2018-20343
This is a PoC for [CVE-2018-20343](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-20343), a vulnerability in Ken Silverman's Build Engine.
The generated .map file triggers a buffer overflow and overwrites the stack as shown below:

---

<figure>
  <img src="https://github.com/Alexandre-Bartel/CVE-2018-20343/blob/master/wd_stack.png" width="400">
  <figcaption>Open Watcom under DosBox 0.74-2: the analyst controls the stack</figcaption>
<figure>
  
---

<figure>
  <img src="https://github.com/Alexandre-Bartel/CVE-2018-20343/blob/master/freedos_EIP.png" width="400">
  <figcaption>Under FreeDos 1.2: the analyst controls EIP</figcaption>
<figure>

---

The vulnerable code is in ENGINE.C:

```c
1935   kread(fil,&numsectors,2);
1936   kread(fil,&sector[0],sizeof(sectortype)*numsectors);
```

Variable *sector* has a declared size of *MAXSECTORS* * sizeof(struct sectortype) = 1024 * 40 = 40960 bytes.
The analyst controls *numsectors* (because it is read from the map file) and can thus create a map file to initialize *numsectors* with a value greater than 40960 to trigger the overflow.

Ken Silverman pointed out that code relying on the *kread* function, such as the following code snippets, might also be vulnerable:

In ENGINE.C:
```c
1938  kread(fil,&numwalls,2);
1939  kread(fil,&wall[0],sizeof(walltype)*numwalls);
1940
1941  kread(fil,&numsprites,2);
1942  kread(fil,&sprite[0],sizeof(spritetype)*numsprites);
```

```c
2033   kread(fil,palette,768);
2034   kread(fil,&numpalookups,2);
[...]
2046   kread(fil,palookup[globalpal],numpalookups<<8);
2047   kread(fil,transluc,65536);
```

```c
2453       kread(fil,&artversion,4);
2454       if (artversion != 1) return(-1);
2455       kread(fil,&numtiles,4);
2456       kread(fil,&localtilestart,4);
2457       kread(fil,&localtileend,4);
2458       kread(fil,&tilesizx[localtilestart],(localtileend-localtilestart+1)<<1);
2459       kread(fil,&tilesizy[localtilestart],(localtileend-localtilestart+1)<<1);
2460       kread(fil,&picanm[localtilestart],(localtileend-localtilestart+1)<<2);
````

```c
2520     kread(fil,&dasiz,4);
2521       //Must store filenames to use cacheing system :(
2522     voxlock[voxindex][i] = 200;
2523     allocache(&voxoff[voxindex][i],dasiz,&voxlock[voxindex][i]);
2524     ptr = (char *)voxoff[voxindex][i];
2525     kread(fil,ptr,dasiz);
```

In KDMENG.C:
```c
1155     kread(fil,&dawaversionum,4);
1156     if (dawaversionum != 0) { kclose(fil); return; }
1157  
1158     kread(fil,&numwaves,4);
1159     for(i=0;i<numwaves;i++)
1160     {
1161       kread(fil,&instname[i][0],16);
1162       kread(fil,&wavleng[i],4);
1163       kread(fil,&repstart[i],4);
1164       kread(fil,&repleng[i],4);
1165       kread(fil,&finetune[i],4);
```

```c
1194     kread(fil,snd,totsndbytes);
```

```c
1214   kread(fil,&kdmversionum,4);
1215   if (kdmversionum != 0) return(-2);
1216   kread(fil,&numnotes,4);
1217   kread(fil,&numtracks,4);
1218   kread(fil,trinst,numtracks);
1219   kread(fil,trquant,numtracks);
1220   kread(fil,trvol1,numtracks);
1221   kread(fil,trvol2,numtracks);
1222   kread(fil,nttime,numnotes<<2);
1223   kread(fil,nttrack,numnotes);
1224   kread(fil,ntfreq,numnotes);
1225   kread(fil,ntvol1,numnotes);
1226   kread(fil,ntvol2,numnotes);
1227   kread(fil,ntfrqeff,numnotes);
1228   kread(fil,ntvoleff,numnotes);
1229   kread(fil,ntpaneff,numnotes);
```

---

The PoC for this vulnerability has been tested using the following environments:

* Ken Silverman's [Build engine](http://www.advsys.net/ken/buildsrc/default.htm) [KENBUILD.ZIP](http://www.advsys.net/ken/buildsrc/kenbuild.zip) (sha256sum 704a5eee1b722ed5f452d3fb1aff197f0d201ff9737839846268c6b1e07f8e1f)
* target binary GAME.EXE (sha256sum 120acdf872af56ac65982a0c21e3aa2fdd06b70bd6203869ba777ce3e6daa5e4) compiled with the [Open Watcom compiler 1.9](http://www.openwatcom.org/)
* [DOSBox](https://www.dosbox.com/) 0.74-2 || [FreeDOS](https://www.freedos.org/) 1.2 under [QEMU](https://www.qemu.org/).

---

The Build engine has been used in many games. 
Below is a list of games based on the Build engine which have been tested against the PoC (which overflows the *sector* variable):

| Game            | Release Date | Version | Status          |
|-----------------|--------------|---------|-----------------|
| Duke Nukem 3D   | 1996         | 1.5     | `vulnerable`    |
| Shadow Warrior  | 1997         | 1.2     | `vulnerable`    |
| Redneck Rampage | 1997         | 1.01    | `vulnerable`    |
| Blood           | 1997         | 1.0     | not vulnerable  |
