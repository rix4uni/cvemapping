# h0nk_bt_exploit

Samsung devices are vulnerable to a critical Bluetooth security vulnerability that allows an attacker to control the targeted device as if they were attached by a Bluetooth keyboard, performing various functions remotely depending on the endpoint. This vulnerability, tracked as CVE-2023-45866, affects macOS, iOS, Android, and Linux device platforms. It works by tricking the Bluetooth host state-machine into pairing with a fake keyboard without user confirmation.

On Android devices, the vulnerability is exploitable whenever Bluetooth is enabled. However, Samsung has released patches for most affected devices, although some older models may not receive updates.
 To mitigate the risk, users are advised to install the latest available security patches and to only enable Bluetooth when strictly necessary.

Additionally, a zero-day vulnerability, tracked as CVE-2024-44068, was discovered in Samsung’s mobile and wearable processors, including Exynos models 9820, 9825, 980, 990, 850, and W920. This vulnerability allows for arbitrary code execution and has been exploited in the wild as part of an exploit chain enabling attackers to escalate privileges on vulnerable devices.

Samsung has released a patch as part of its October 2024 security updates, and users should apply this update to mitigate the risk

## perplexity.ai Antwort:

Es gibt tatsächlich eine kürzlich entdeckte kritische Bluetooth-Schwachstelle, die es Angreifern ermöglicht, Android-, iOS-, macOS- und Linux-Geräte zu kompromittieren, indem sie eine Bluetooth-Tastatur simulieren.

Diese Schwachstelle, bezeichnet als CVE-2023-45866, erlaubt es Angreifern, sich ohne Authentifizierung mit betroffenen Bluetooth-Geräten zu verbinden und Tastatureingaben zu injizieren, um Code-Ausführung zu erreichen. Der Angriff funktioniert, indem das Zielgerät getäuscht wird zu glauben, es sei mit einer Bluetooth-Tastatur verbunden. Dies geschieht durch Ausnutzung eines "nicht authentifizierten Kopplungsmechanismus" im Bluetooth-Protokoll.

Für Samsung-Geräte ist diese Schwachstelle besonders relevant für ältere Modelle wie Galaxy S4, S5 und S6. Der Angriff kann mit einem Linux-Gerät (z.B. Raspberry Pi) mit Bluetooth-Adapter gegen jedes erkennbare Bluetooth-Ziel in Reichweite durchgeführt werden, potenziell bis zu einer Entfernung von etwa 240 Metern.

Um sich vor solchen Angriffen zu schützen, wird empfohlen:

Bluetooth zu deaktivieren, wenn es nicht verwendet wird.

Sichere Kopplungsmethoden zu verwenden.

Regelmäßige Software-Updates durchzuführen.

Das Koppeln in öffentlichen oder nicht vertrauenswürdigen Umgebungen zu vermeiden.

Es ist wichtig zu beachten, dass zum Zeitpunkt der Entdeckung (Dezember 2023) noch keine Sicherheitsupdates für dieses Problem verfügbar waren.

## CVE-2023-45866

🧠 Ziel des Tools
Das Script simuliert eine Bluetooth-Tastatur (HID) und führt über DuckyScript automatisierte Tastatureingaben auf einem Zielgerät aus.

✅ Funktionsweise
Schritt	Beschreibung
1.	Bluetooth-Adapter konfigurieren (Name, Klasse, SSP aktivieren)
2.	Zielgerät (MAC-Adresse) auswählen und koppeln
3.	Bluetooth HID-Profil registrieren
4.	Verbindung zu HID-Ports aufbauen (L2CAP)
5.	DuckyScript ausführen → simulierte Tastaturbefehle
6.	Gerät nach Ausführung entkoppeln
🔧 Plattform-Vergleich
Plattform	Status	Voraussetzungen	Bemerkung
Raspberry Pi	✅ Läuft bereits	BlueZ, Python, root	Klein, mobil, günstig
Linux-Laptop	✅ Voll kompatibel	BlueZ, Python, root	Keine Extra-Hardware nötig
M5Stick / ESP32	⚠️ Teilweise	C++ mit ESP-IDF/Arduino	Nur BLE HID, kein L2CAP / Duckyscript
🔌 Zielgerät: MAC-Adresse
Muss explizit eingegeben werden (get_target_address()).

Wird für Pairing und Verbindung genutzt.

Muss Bluetooth aktiv haben und Verbindungen zulassen.

🧱 Technische Einschränkungen M5Stick
Funktion	Unterstützt auf M5Stick?
Bluetooth Classic HID (L2CAP)	❌ Nicht möglich
BLE HID (BLE Keyboard)	✅ Möglich mit Arduino
DuckyScript-Verarbeitung	❌ Nur mit viel Aufwand
Autopairing	❌ Zielgerät muss Verbindung initiieren
💡 Alternativen mit M5Stick
Idee	Beschreibung
BLE Keyboard	Autarker Mini-Angreifer (fixe Tasteneingaben)
Trigger/Remote	M5Stick sendet Signal über WiFi → Laptop/Pi führt Script aus
Serial Bridge	M5Stick sendet via UART an Laptop, der dann agiert
🔒 Sicherheitsbewertung
Punkt	Einschätzung
Verbindung nach außen	❌ Kein externer Datenabfluss
Verstecktes Verhalten	✅ Bluetooth-Tastatur wird als echt erkannt
Angriffspotenzial	🔥 Hoch (automatisierte Eingabe beliebiger Befehle)
Rechtlich bedenklich?	⚠️ Ja, nur für eigene Geräte oder mit Zustimmung erlaubt

Resource:
 - https://pypi.org/project/PyBluez/

⚠️ Disclaimer
The provided scripts and proof-of-concept code are intended solely for educational and private testing purposes. They must only be executed on devices that you own or have explicit permission to test.

By using these scripts, you agree to take full responsibility for any actions taken. Unauthorized use on networks or devices you do not control may be illegal and is strictly prohibited.

The author of this code is not liable for any damage, disruption, or legal consequences resulting from misuse. Always follow responsible disclosure and ethical testing guidelines.
