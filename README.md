# cvemapping

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Language: Go](https://img.shields.io/badge/Language-Go-blue.svg)](https://golang.org)
[![Platform: Cross-platform](https://img.shields.io/badge/Platform-Cross--platform-blue.svg)](https://github.com/rix4uni/cvemapping)
[![Stars](https://img.shields.io/github/stars/rix4uni/cvemapping?style=flat-square)](https://github.com/rix4uni/cvemapping)

> This repo Gathers all available CVE exploits from GitHub.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📥 Installation](#-installation)
- [💻 Usage](#-usage)
- [🌐 Website](#-website)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 CVE Search | Search GitHub for repositories related to specific CVEs |
| 📦 Repo Cloning | Automatically clone exploit repositories |
| 📊 JSON Export | Export CVE data to JSON for websites |
| 🌐 Cross-platform | Runs on Linux, macOS, and Windows |
| ⚡ Fast | Efficient GitHub API usage with token support |

## 🚀 Quick Start

```bash
# Install via Go
go install github.com/rix4uni/cvemapping@latest

# Search for CVE-2024 exploits (clone repos)
echo '"CVE-2024-"' | cvemapping -github-token "YOUR_TOKEN" -page all -year 2024

# Export to JSON instead
echo '"CVE-2024-"' | cvemapping -github-token "YOUR_TOKEN" -page all -year 2024 -export-json
```

## 📥 Installation

### Option 1: Install via Go

```bash
go install github.com/rix4uni/cvemapping@latest
```

### Option 2: Download Prebuilt Binaries

```bash
# Linux/macOS
wget https://github.com/rix4uni/cvemapping/releases/download/v0.0.1/cvemapping-linux-amd64-0.0.1.tgz
tar -xvzf cvemapping-linux-amd64-0.0.1.tgz
rm cvemapping-linux-amd64-0.0.1.tgz
mv cvemapping ~/go/bin/

# Download other platforms: https://github.com/rix4uni/cvemapping/releases
```

### Option 3: Compile from Source

```bash
git clone --depth 1 github.com/rix4uni/cvemapping.git
cd cvemapping
go install
```

## 💻 Usage

### Command-line Flags

| Flag | Type | Description | Default |
|------|------|-------------|---------|
| `-github-token` | string | GitHub authentication token | required |
| `-year` | string | Year to search (e.g., 2024, 2020) | required |
| `-page` | string | Page number or 'all' | "1" |
| `-export-json` | bool | Export to JSON instead of cloning | false |

### Usage Examples

```bash
# Clone all 2024 CVE repos
echo '"CVE-2024-"' | cvemapping -github-token "TOKEN" -page all -year 2024

# Export CVE data to JSON for a website
echo '"CVE-2024-"' | cvemapping -github-token "TOKEN" -page all -year 2024 -export-json

# Search specific page only
echo '"CVE-2023-0001"' | cvemapping -github-token "TOKEN" -page 1 -year 2023
```

## 🌐 Website

This tool exports CVE data to JSON format for use with the included website.

### Generating JSON Data

```bash
echo '"CVE-2024-"' | cvemapping -github-token "TOKEN" -page all -year 2024 -export-json
```

JSON files are created in the `data/` directory (e.g., `data/2024.json`).

### Running the Website

1. Generate JSON data files for desired years
2. Copy JSON files to `web/data/` directory
3. Serve the `web/` directory using any static file server
4. Open in your browser

See `web/README.md` for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

---

README optimized with [Gingiris README Generator](https://gingiris.github.io/github-readme-generator/)
