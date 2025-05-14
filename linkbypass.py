import re
import time
import webbrowser
import pyperclip
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)

def RecaptchaV3():
    import requests
    ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8ucHJlc3M6NDQz&hl=en&v=pCoGBhjs9s8EhFOHJFe8cqis&size=invisible&cb=ahgyd1gkfkhe'
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({'content-type': 'application/x-www-form-urlencoded'})
    matches = re.findall(r'([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0] + '/'
    params = matches[1]
    res = client.get(url_base + 'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base + 'reload', params=f'k={params["k"]}', data=post_data)
    return re.findall(r'"rresp","(.*?)"', res.text)[0]

def ouo_bypass(url):
    client = requests.Session()
    client.headers.update({
        'authority': 'ouo.io',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'referer': 'http://www.google.com/ig/adde?moduleurl=',
        'upgrade-insecure-requests': '1',
    })

    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    res = client.get(tempurl, impersonate="chrome110")
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = {input.get('name'): input.get('value') for input in inputs}
        data['x-token'] = RecaptchaV3()

        h = {'content-type': 'application/x-www-form-urlencoded'}

        res = client.post(next_url, data=data, headers=h,
                          allow_redirects=False, impersonate="chrome110")
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return {
        'original_link': url,
        'bypassed_link': res.headers.get('Location')
    }

if __name__ == "__main__":
    print(Fore.CYAN + "OUO linklerini gir (her satıra 1 link). Boş satır bırakınca başlayacak:\n")

    links = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        links.append(line)

    if not links:
        print(Fore.RED + "[-] Hiç link girilmedi.")
        exit()

    for link in links:
        print(Fore.CYAN + f"\n[🔗] İşleniyor: {link}")

        if not re.match(r"^https:\/\/(ouo\.io|ouo\.press)\/[A-Za-z0-9]+$", link):
            print(Fore.RED + "[-] Geçersiz OUO bağlantısı, atlandı.")
            continue

        start_time = time.time()
        result = ouo_bypass(link)
        elapsed = round(time.time() - start_time, 2)

        print(Fore.BLUE + "[•] Orijinal link: " + Style.RESET_ALL + result['original_link'])

        if result['bypassed_link']:
            print(Fore.GREEN + "[✓] Bypass edildi: " + Style.RESET_ALL + result['bypassed_link'])
            print(Fore.YELLOW + f"[⏱️] Süre: {elapsed} saniye")

            pyperclip.copy(result['bypassed_link'])
            print(Fore.MAGENTA + "[📋] Link panoya kopyalandı.")
            webbrowser.open(result['bypassed_link'])
            print(Fore.YELLOW + "[🌐] Tarayıcıda açılıyor...")
        else:
            print(Fore.RED + "[-] Bypass başarısız.")
