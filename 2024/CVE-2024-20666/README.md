# CVE-2024-20666 Vulnerability Patch Guide
- Welcome to the repository for addressing the CVE-2024-20666 vulnerability patch failures in the Windows Recovery Environment (WinRE).
## Overview

This repository provides resources and instructions to resolve patch failures related to the Windows OS update KB5034441. The update addresses a critical security vulnerability identified as CVE-2024-20666, which could allow attackers to bypass BitLocker encryption by exploiting WinRE.

## Problem Identified

Many users have reported failures when attempting to install the KB5034441 update. The primary issue is insufficient disk space in the Windows recovery partition, causing the installation process to fail with error code 0x80070643.

## Solutions Provided

### Manual Partition Resizing

To successfully install the update, you may need to resize your Windows recovery partition manually. Detailed instructions are available on the [Microsoft support page KB5028997](https://support.microsoft.com/kb5028997).

### Automated Update Scripts

Microsoft has released [PowerShell](https://github.com/invaderslabs/CVE-2024-20666/blob/main/CVE-2024-20666_Checker.ps1) scripts to automate the update process for different Windows versions:

- **PatchWinREScript_2004plus.ps1**: For Windows 10 (version 2004 and later) and Windows 11.
- **PatchWinREScript_General.ps1**: For all versions of Windows 10 and Windows 11, especially earlier versions of Windows 10 (pre-2004).

## How to Use This Repository

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/CVE-2024-20666-patch-guide.git
   cd CVE-2024-20666-patch-guide
