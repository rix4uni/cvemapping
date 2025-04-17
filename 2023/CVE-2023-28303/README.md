# SnipRecover CLI

> **Detection and restoration of Windows Snipping Tool PNG captures vulnerable to CVE-2023-28303**

**SnipRecover CLI** is a minimal, dependency-free command-line utility designed to:

- **Detect** PNG files modified by the Windows Snipping Tool vulnerability (CVE‑2023‑28303).
    
- **Restore** the original image by recovering compressed data appended after the `IEND` chunk.
    

By default, restored images use **RGBA** and a resolution of **1920×1080**, and if no output path is specified, the tool writes to `restored-<original_name>.png`.

---

## 🧠 Theoretical Background

According to the PNG specification ([ISO/IEC 15948](https://www.w3.org/TR/PNG)), all image data (`IDAT` chunks) must appear **before** the final `IEND` chunk. Windows Snipping Tool mistakenly appends additional `IDAT` data **after** `IEND`, violating the standard and exposing the full image content that was “cropped.”

**Standard PNG structure:**

1. **Signature (8 bytes):** `89 50 4E 47 0D 0A 1A 0A`
    
2. **Chunks:**
    
    - `IHDR`: image header (width, height, color type, etc.)
        
    - `IDAT`: compressed pixel data
        
    - `IEND`: end-of-file marker
        

A Snipping Tool–cropped PNG contains **extra bytes** beyond `IEND`. SnipRecover CLI detects this anomaly and reconstructs the compression stream to recover the original image.

---

## 🚀 Installation

**Prerequisites:**

- Python 3.10 or newer
    

**Steps:**

```
git clone https://github.com/m31r0n/SnipRecover-CLI.git
cd SnipRecover-CLI
chmod +x sniprecover
```

_No external libraries are needed—only Python’s standard_ `_struct_`_,_ `_zlib_`_, and_ `_io_` _modules._

---

## ⚙️ Usage

```
# Display help
python3 sniprecover --help

# 1. Detect vulnerable PNG(s)
python3 sniprecover detect /path/to/images/

# 2. Restore a cropped capture
python3 sniprecover restore capture.png --output restored-capture.png
```

> **Note:** If you omit `--width`, `--height`, or `--alpha`, defaults of **1920×1080** and **RGBA** are applied. If you omit `--output`, restored images are saved as `restored-<original_name>.png`.

---

## 🔧 Restore Options

|Option|Description|Default|
|---|---|---|
|`--width <int>`|Original image width|`1920`|
|`--height <int>`|Original image height|`1080`|
|`--alpha`|Include alpha channel (RGBA)|enabled|
|`--output <file>`|Path to save the restored PNG|`restored-<original_name>.png`|

---

## 📁 Project Structure

```
SnipRecover-CLI/
├── sniprecover      # Main CLI executable (make sure it's executable)
└── README.md        # Documentation and theory
```

---

## 🔗 References

- **CVE‑2023‑28303**: Windows Snipping Tool vulnerability – Microsoft Security Response Center
    
- **PNG Specification** (ISO/IEC 15948) – W3C
    

---


## 📜 License

MIT © 2025 – Developed by m31r0n
