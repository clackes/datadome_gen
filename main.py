from datadome import Datadome
from datetime import datetime
import newdragon
import time

class Logger:
    def message(self, message):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] {message}')

class DatadomeSolver(Logger):
    ddk = "A55FBF4311ED6F1BF9911EB71931D5"
    ddv = "4.18.0"
    dd_domain = "https://api-js.datadome.co/js/"
    def solve_datadome(self,session:newdragon.Session, domain, event=False):
        datadome = Datadome(session, domain, self.ddk, self.ddv, self.dd_domain)
        value = datadome.generate_datadome(event)["value"]
        session.delete_cookie("datadome","footlocker.it")
        session.set_cookie("datadome",value ,".footlocker.it", "/")
        self.cid_url = datadome.cid_url
        
class Main(DatadomeSolver):
    def __init__(self, session:newdragon.Session):
        self.session = session
        self.home_url = "https://www.footlocker.it/"
        self.solve_datadome(self.session, self.home_url, False)
        time.sleep(5)
        self.login()
    def login(self):
        headers = {
            'authority': 'www.footlocker.it',
            'accept': 'application/json',
            'accept-language': 'it-IT,it;q=0.8',
            'content-lenght':'',
            'content-type': 'application/json',
            'accept-encoding':'gzip, deflate, br',
            'origin': 'https://www.footlocker.it',
            'referer': 'https://www.footlocker.it/',
            'sec-ch-device-memory': '8',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="119.0.6045.160", "Chromium";v="119.0.6045.160", "Not?A_Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-api-lang': 'it-IT',
            'x-csrf-token': '9cabe01d-c8be-48a9-aeff-0f80deb414ca',
            'x-fl-request-id': 'a74d99d0-8e2c-11ee-9b69-17f364d9aeb6',
            'x-flapi-session-id': '590258c7-693c-4c9c-bc95-b5460ca7c6e6',
        }
        json_data = {
            'uid': '',
            'password': '',
        }

        response = self.session.post(f'https://www.footlocker.it/api/auth?timestamp={datetime.now()}', headers=headers, json=json_data)
        print(response.status_code)

def create_session() -> newdragon.Session:
    session = newdragon.Session()
    session.headers['User-Agent'] = 'ua'
    session.proxies = {
        #"http":"http://127.0.0.1:8888",
        #"https":"http://127.0.0.1:8888"
        "http":"http://PRIM_SDA6Y9JE11-cc-gb-pool-bd-sessionid-2846720:4DI71ZICJ1SAHO@bright.primedproxiesresi.com:8888",
        "https":"http://PRIM_SDA6Y9JE11-cc-gb-pool-bd-sessionid-6692439:4DI71ZICJ1SAHO@bright.primedproxiesresi.com:8888"
        }
    session.accept_language = 'it-IT,it;q=0.8'
    session.secchua = '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"'
    session.verify = False
    return session
session = create_session()
Main(session)

