from datetime import datetime
import math
import random
import json
import numpy as np
import urllib.parse
from urllib.parse import urlencode, urlparse, quote
import newdragon as tls_client
import time

class Logger:
    def message(self, message):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] {message}')
with open("E:\OneDrive\lavoro\proxy.json", "r") as f:
    proxy_file = json.load(f)["proxy"]
    

class Datadome(Logger):
    def __init__(self, session:tls_client.Session, domain, datadome_key, datadome_version, datadome_domain):
        self.session = session
        self.origin =f'https://{urlparse(domain).netloc}'
        self.referer = domain
        self.datadome_key = datadome_key
        self.datadome_version = datadome_version
        self.cid_url=None
        self.datadome_domain = datadome_domain
        self.device = self.getDevice()
        self.navigator = self.device["navigator"]
        self.screen = self.device["screen"]
        self.uar = self.session.headers["User-Agent"]
        if "Chrome" in self.uar:
            self.version = self.uar.split("Chrome/")[1].split(".")[0]
        else:
            self.version = "112"
        if "Mac" in self.uar:
            self.platform = 'macOS'
        elif "Windows" in self.uar:
            self.platform = 'Windows'
        elif "Linux" in self.uar:
            self.platform = 'Linux'
        elif "CrOS" in self.uar:
            self.platform = 'Chrome OS'
        else:
            self.platform = 'Unknown'
        # Get dynamic data
        self.get_cookie_domain()
        self.getGraphics()
        self.getScreen()
        # 
        self.datadome_headers = {
                #'Host': urlparse(self.origin).netloc,
                #'authority': urlparse(self.datadome_domain).netloc ,
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': self.session.accept_language,
                'content-lenght':'',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': self.origin,
                'referer': self.referer,
                'sec-ch-ua': self.session.secchua,
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': self.uar,
            }
        self.cid_cookie = self.get_cid()

    def get_cookie_domain(self):
        parsed = urlparse(self.referer).netloc
        splitted=parsed.split('.')
        try:
            self.cookie_domain = '.'.join(splitted[-2:])
        except:
            self.cookie_domain = '.' + splitted[1] + '.' + splitted[2]

    def get_cid(self):
        headers = {
            'cache-control': 'max-age=0',
            'sec-ch-device-memory': '8',
            'sec-ch-ua': self.session.secchua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-arch': 'x86',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-full-version-list': '"Chromium";v="118.0.5993.118", "Google Chrome";v="118.0.5993.118", "Not=A?Brand";v="99.0.0.0"',
            'upgrade-insecure-requests': '1',
            'user-agent': self.session.headers["User-Agent"],
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': self.session.accept_language,
            'if-none-match': 'W/"bd1c6-DY/xUWtkB/SrfXGOWg2xxibmsQo"'
        }
        status_code = 403
        while status_code ==403:
            r = self.session.get(
                self.referer,
                headers = headers
            )
            try:
                status_code = r.status_code
                if status_code == 200 or status_code ==304:
                    self.cid_url = r.url
                    self.cid_cookie = self.session.get_cookie("datadome",self.cookie_domain)["value"]
                    #self.session.set_cookie("datadome",self.cid_cookie ,self.cookie_domain, "/")
                    self.message(f"Found proper cid {r.status_code}")
                else:
                    newproxy = random.choice(proxy_file)
                    self.session.proxies = {
                        "http":f"http://{newproxy}",
                        "https":f"http://{newproxy}"
                    }
                    self.message("Changing proxy and clearing cookies")
                    self.session.delete_cookie("datadome", self.cookie_domain)
            except Exception as e:
                self.message(f"Didn't found proper cid: {r.status_code}")
            time.sleep(2)

    def generate_datadome(self, event):
        self.ttst = round(random.uniform(8,40),15)
        self.tagpu = round(self.ttst - (0.20 * self.ttst),14)
        time.sleep(1)
        data = self.generateData(event)
        time.sleep(1)
        try:
            gen_dd_res = self.session.post(
                url=self.datadome_domain,
                headers = self.datadome_headers,
                data = data
            )
        except Exception as e:
            self.message(e)
        if gen_dd_res.status_code == 200:
            cookie = gen_dd_res.json()["cookie"]
            return {
                "value": cookie.split("=")[1].split(";")[0],
                "cookie": cookie.split(";")[0] + ";",
                "raw": cookie,
            }
        else:
            self.message(gen_dd_res.status_code)

    @staticmethod
    def getDevice():
        with open("devices-2_1.json") as devices_file:
            devices = json.load(devices_file)
            return random.choice(devices)

    def getGraphics(self):
        self.glvd = self.device["wv"]
        self.glrd = self.device["wr"]
        
    def getScreen(self):
        self.br_h = self.device["window"]["innerHeight"]
        self.br_w = self.device["window"]["innerWidth"]
        self.br_oh = self.device["window"]["outerHeight"]
        self.br_ow = self.device["window"]["outerWidth"]
        self.rs_h = self.screen["height"]
        self.rs_w = self.screen["width"]
        self.rs_cd = self.screen["colorDepth"]
        self.ars_h = self.screen["availHeight"]
        self.ars_w = self.screen["availWidth"]

    def generateData(self, event : bool = False):
        # jsType
        self.jsType = "ch"
        self.jset = int(time.time() * 1000)
        # Events
        self.events = []
        self.eventCounters = []
        jsData = {
            "opts" : "ajaxListenerPath",
            "ttst": self.ttst,
            "ifov":False,"wdif":False,"wdifrm":False,
            "npmtm":False,
            "dp0":True,
            "tagpu": self.tagpu,
            "glvd":self.glvd,
            "br_h": self.br_h,
            "br_w": self.br_w,
            "br_oh": self.br_oh,
            "br_ow": self.br_ow,
            "nddc": self.isCookie(),  #is Cookie
            "rs_h": self.rs_h,
            "rs_w": self.rs_w,
            "rs_cd": self.rs_cd,
            "phe":False,"nm":False,"jsf":False,
            "ua": self.uar,
            "lg": self.navigator["language"],
            "pr": self.device["window"]["devicePixelRatio"],
            "hc": 8,
            "ars_h": self.ars_h,
            "ars_w": self.ars_w,
            "tz": -60,
            "str_ss":True,"str_ls":True,"str_idb":True,"str_odb":True,"plgod":False,
            "plg": len(self.navigator["plugins"]),
            "plgne":True,"plgre":True,"plgof":False,"plggt":False,"pltod":False,"hcovdr":False,"hcovdr2":False,"plovdr":False,"plovdr2":False,"ftsovdr":False,"ftsovdr2":False,"lb":False,
            "eva": 33, # For Chrome eval.toString().length = 33
            "lo":False,
            "ts_mtp": 0,
            "ts_tec":False,"ts_tsa":False,
            "vnd": self.navigator["vendor"],
            "bid": "NA", # Only for Firefox
            "mmt": self.getMimeTypes(),
            "plu": ",".join(self.navigator["plugins"]),
            "hdn":False,"awe":False,"geb":False,"dat":False,"med":"defined","aco":"probably","acots":False,"acmp":"probably","acmpts":True,"acw":"probably","acwts":False,"acma":"maybe","acmats":False,"acaa":"probably","acaats":True,"ac3":"","ac3ts":False,"acf":"probably","acfts":False,"acmp4":"maybe","acmp4ts":False,"acmp3":"probably","acmp3ts":False,"acwm":"maybe","acwmts":False,"ocpt":False,"vco":"probably","vcots":False,"vch":"probably","vchts":True,"vcw":"probably","vcwts":True,"vc3":"maybe","vc3ts":False,"vcmp":"","vcmpts":False,"vcq":"","vcqts":False,"vc1":"probably","vc1ts":True,
            "dvm": 8,
            "sqt":False,"so":"landscape-primary","wbd":False,"wdw":True,
            "cokys":"bG9hZFRpbWVzY3NpYXBwL=",
            "ecpc":False,"lgs":True,"lgsod":False,"psn":True,"edp":True,"addt":True,"wsdc":True,"ccsr":True,"nuad":True,"bcda":True,"idn":True,"capi":False,"svde":False,"vpbq":True,"ucdv":False,"spwn":False,"emt":False,"bfr":False,"dbov":False,
            "cfpfe":"RXJyb3I6IENhbm5vdCByZWFkIHByb3BlcnRpZXMgb2YgbnVsbCAocmVhZGluZyAndG9TdHJpbmcnKQ==",
            "stcfp":"MzUzYTZiY2Y2NDQ5MzM5ZTQ3Nzc1ZGEwMzI3YWM3Lm1pbi5qczo4OjIxNzE4KQogICAgYXQgZS5leHBvcnRzIChodHRwczovL2Fzc2V0cy5hZG9iZWR0bS5jb20vbGF1bmNoLUVOMmUzNTNhNmJjZjY0NDkzMzllNDc3NzVkYTAzMjdhYzcubWluLmpzOjg6MTE4NTkp",
            "prm":True,"tzp":"Europe/Rome","cvs":True,"usb":"defined","jset":int(self.jset/1000),
        }
        if event:
            self.jsType = "le"
            self.generateEvent()
            jsData["dcok"] = '.' + self.cookie_domain
            self.getMouseData()
            if self.eventCounters["mousemove"] > 0:
                jsData["mp_cx"] = self.mp_cx
                jsData["mp_cy"] = self.mp_cy
                jsData["mp_tr"] = self.mp_tr
                jsData["mp_mx"] = self.mp_mx
                jsData["mp_my"] = self.mp_my
                jsData["mp_sx"] = self.mp_sx
                jsData["mp_sy"] = self.mp_sy
                jsData["mm_md"] = self.mm_md
                jsData["m_s_c"] = self.eventCounters["scroll"]
                jsData["m_m_c"] = self.eventCounters["mousemove"]
                jsData["m_c_c"] = self.eventCounters["click"]
                jsData["m_mc_r"] = 0
                jsData["m_ms_r"] = -1
            #jsData["tbce"] = random.randint(90,150)
            jsData["es_sigmdn"] = self.es_sigmdn
            jsData["es_mumdn"] = self.es_mumdn
            jsData["es_distmdn"] = self.es_distmdn
            jsData["es_angsmdn"] = self.es_angsmdn
            jsData["es_angemdn"] = self.es_angemdn
        data = {
            "jsData": json.dumps(jsData, separators=(',', ':')),
            "eventCounters": self.eventCounters,
            "jsType": self.jsType,
            "cid": self.cid_cookie,
            "ddk": self.datadome_key,
            "Referer": urllib.parse.quote_plus(self.referer),
            "request": urllib.parse.quote_plus(urlparse(self.referer).path),
            "responsePage": "origin",
            "ddv": self.datadome_version,
        }
        return urlencode(data)
    
    def getMimeTypes(self):
        mt = self.navigator["mimeTypes"]
        mmt = ",".join(t["type"] for t in mt)
        return mmt
    
    def getMouseData(self):
        self.mp_cx = random.randint(200, 900)
        self.mp_cy = random.randint(200, 500)
        self.mp_tr = True
        self.mp_mx = random.randint(-40,40)
        self.mp_my = random.randint(-40,40)
        self.mp_sx = self.mp_cx + random.randint(100,300)
        self.mp_sy = self.mp_cy + random.randint(100,300)
        self.mm_md = random.randint(1,100)
        mouseEvents = [e for e in self.events if e["message"] == "mousemove"]
        mouseEventCounter = self.eventCounters["mousemove"]
        es_sigmdn_array = []
        es_mumdn_array = []
        es_distmdn_array = []
        startAngels = []
        endAngels = []
        for e in mouseEvents:
            x = math.log(e["date"])
            q = mouseEventCounter
            y = math.log(e["date"]) * math.log(e["date"])
            es_sigmdn_array.append(round(np.longfloat(math.sqrt((q*y-x*x)/(q*(q-1))) / 10000),21))
            es_mumdn_array.append(x/q)
            if q < 4:
                D =  q - 1
            else:
                D = 3
            E = mouseEvents[D]
            F = mouseEvents[len(mouseEvents) - D - 1]
            def calculateAngle(m, p, q, u):
                v = q - m
                w = u - p
                x = math.acos(v / math.sqrt(v * v + (w * w)))
                if w < 0:
                    return -x
                return x
            startAngels.append(calculateAngle(mouseEvents[0]["source"]["x"], mouseEvents[0]["source"]["y"], E["source"]["x"], E["source"]["y"]))
            endAngels.append(calculateAngle(mouseEvents[-1]["source"]["x"], mouseEvents[-1]["source"]["y"], F["source"]["x"], F["source"]["y"]))
        
        for i in range(len(mouseEvents)):
            try:
                diff_x = mouseEvents[i+1]["source"]["x"] - mouseEvents[i]["source"]["x"]
                diff_y = mouseEvents[i+1]["source"]["y"] - mouseEvents[i]["source"]["y"]
                es_distmdn_array.append(math.sqrt(diff_x**2 + diff_y**2))
            except IndexError:
                pass
        
        def getValue(sorted_array):
            u = (len(sorted_array) - 1) * 50 / 100
            v = math.floor(u) + 1
            try:
                if sorted_array[v] != 0:
                    w = u - v
                    try:
                        return str(sorted_array[v] + w * (sorted_array[v + 1] - sorted_array[v]))
                    except IndexError:
                        return str(sorted_array[v])
                else:
                    return str(sorted_array[v])
            except IndexError:
                return None
        
        self.es_sigmdn = getValue(sorted(es_sigmdn_array))
        self.es_mumdn = getValue(sorted(es_mumdn_array))
        self.es_distmdn = getValue(sorted(es_distmdn_array))
        self.es_angsmdn = getValue(sorted(startAngels))
        self.es_angemdn = getValue(sorted(endAngels))
    
    def generateEvent(self):
        startingPos = [random.randint(0, self.br_w), random.randint(0, self.br_h)]
        currentPos = startingPos
        endingPos = [random.randint(0, self.br_w), random.randint(0, self.br_h)]
        x = [startingPos[0]]
        y = [startingPos[1]]
        while endingPos[0] != currentPos[0] and len(x) < 500:
            deltaPos1 = (random.randint(2, 8), random.randint(2, 8))
            deltaPos2 = (random.randint(5, 12), random.randint(5, 12))
            deltaPosList = [deltaPos1, deltaPos2]
            deltaPos = random.choice(deltaPosList)
            if currentPos[0] < endingPos[0] and endingPos[0] - currentPos[0] > 50:
                currentPos[0] += deltaPos[0] + random.randint(-100, 100)
            elif currentPos[0] < endingPos[0] and endingPos[0] - currentPos[0] < 50:
                currentPos[0] += endingPos[0] - currentPos[0]
            elif currentPos[0] > endingPos[0] and currentPos[0] - endingPos[0] > 50:
                currentPos[0] -= deltaPos[0] + random.randint(-100, 100)
            elif currentPos[0] > endingPos[0] and currentPos[0] - endingPos[0] < 50:
                currentPos[0] -= currentPos[0] - endingPos[0]
            if currentPos[0] > 0:
                x.append(currentPos[0])
        y = np.linspace(startingPos[1], endingPos[1], len(x), dtype=int)
        self.events = [{"source":{"x":int(x[i]),"y":int(y[i])},"message":"mousemove","date":None,"id":0}for i in range(len(x))]
        if random.random() > 0.2 and len(x) > 50:
            for i in range(random.randint(1, 10)):
                event = random.choice(self.events)
                event["message"] = "click"
                event["id"] = 1
        scrollStart = random.randint(1, 10)
        scrollCurrent = scrollStart
        steps = random.randint(30, 200)
        scrollY = [scrollStart]
        for _ in range(steps):
            if scrollCurrent > 250:
                scrollCurrent -= random.randint(10, 100)
            else:
                scrollCurrent += random.randint(10, 100)
            scrollY.append(scrollCurrent)
        scrollEvents = [{"source":{"x":0,"y":scrollY[i]},"message":"scroll","date":None,"id":2} for i in range(len(scrollY))]
        self.events.extend(scrollEvents)
        for i, event in enumerate(self.events):
            event["date"] = self.jset - (len(event)-i)*0.5
        self.eventCounters = {"mousemove":len([i for i,e in enumerate(self.events) if e["message"] == "mousemove"]),"click":len([i for i,e in enumerate(self.events) if e["message"] == "click"]),"scroll":len([i for i,e in enumerate(self.events) if e["message"] == "scroll"]),"touchstart":0,"touchend":0,"touchmove":0,"keydown":0,"keyup":0}
    def isCookie(self):
        if self.cid_cookie:
            return 1
        else:
            return 0