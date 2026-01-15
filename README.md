## cvemapping

This repo Gathers all available cve exploits from github.

## Installation
```
go install github.com/rix4uni/cvemapping@latest
```

## Download prebuilt binaries
```
wget https://github.com/rix4uni/cvemapping/releases/download/v0.0.1/cvemapping-linux-amd64-0.0.1.tgz
tar -xvzf cvemapping-linux-amd64-0.0.1.tgz
rm -rf cvemapping-linux-amd64-0.0.1.tgz
mv cvemapping ~/go/bin/cvemapping
```
Or download [binary release](https://github.com/rix4uni/cvemapping/releases) for your platform.

## Compile from source
```
git clone --depth 1 github.com/rix4uni/cvemapping.git
cd cvemapping; go install
```

## Usage
```yaml
Usage of cvemapping:
  -export-json
        Export data to JSON files instead of cloning
  -github-token string
        GitHub Token for authentication
  -page string
        Page number to fetch, or 'all' (default "1")
  -year string
        Year to search for CVEs (e.g., 2024, 2020)
```

## Usage Examples
```yaml
# Clone repositories (default behavior)
echo '"CVE-2024-"' | cvemapping -github-token "TOKEN" -page all -year 2024

# Export to JSON for website
echo '"CVE-2024-"' | cvemapping -github-token "TOKEN" -page all -year 2024 -export-json
```

## Website

This tool can export CVE data to JSON format for use with the included website.

### Generating JSON Data

Use the `-export-json` flag to generate JSON files:
```bash
echo '"CVE-2024-"' | cvemapping -github-token "TOKEN" -page all -year 2024 -export-json
```

This will create JSON files in the `data/` directory (e.g., `data/2024.json`).

### Running the Website

1. Generate JSON data files for desired years
2. Copy JSON files to `web/data/` directory
3. Serve the `web/` directory using any static file server
4. Open in your browser

See `web/README.md` for detailed instructions.