import re
import time
import subprocess
import requests
from bs4 import BeautifulSoup


def ouo_bypass(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    tempurl = url.replace("ouo.press", "ouo.io")
    id = tempurl.split('/')[-1]

    try:
        print(f"[🔗] İşleniyor: {url}")
        res = requests.get(tempurl, headers=headers)
        bs4 = BeautifulSoup(res.text, 'html.parser')

        token = bs4.find("input", {"name": re.compile(r"token$")})['value']
        next_url = f"{tempurl}/go/{id}"
        data = {'token': token}

        res = requests.post(next_url, headers=headers, data=data, allow_redirects=False)
        if 'Location' in res.headers:
            bypassed_link = res.headers['Location']
            print(f"[✓] Bypass edildi: {bypassed_link}")
            return bypassed_link
        else:
            print("[-] Bypass başarısız.")
            return None
    except Exception as e:
        print(f"[!] Hata: {e}")
        return None


if __name__ == "__main__":
    print("OUO linklerini gir (her satıra 1 link). Boş satır bırakınca başlayacak:\n")

    links = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        links.append(line)

    if not links:
        print("[-] Hiç link girilmedi.")
        exit()

    for link in links:
        if not re.match(r"^https://(ouo\.io|ouo\.press)/[A-Za-z0-9]+$", link):
            print("[-] Geçersiz OUO bağlantısı, atlandı.")
            continue

        start_time = time.time()
        result = ouo_bypass(link)
        elapsed = round(time.time() - start_time, 2)

        if result:
            print(f"[⏱️] Süre: {elapsed} saniye")
        else:
            print("[-] Bypass başarısız.")
