import requests
from flask import send_file
from bs4 import BeautifulSoup 
import shutil
from os import path
import tempfile
def get_img(url):
    proxies = {
    "http": 'socks5h://127.0.0.1:1080' ,
    "https": 'socks5h://127.0.0.1:1080' ,
    }
    s = requests.Session()
    s.proxies = proxies
    s.stream = True
    res =  s.get(url,)
    body = res.content.decode("utf-8")
    soup = BeautifulSoup(body, features="html.parser")
    img_url = soup.find(attrs={"property": "og:image"}).get("content")
    if img_url:
        res =  s.get(img_url)
        filename = path.basename(img_url).split("?")[0]
        res = send_file(res.raw, mimetype="image/jpg")
        res.headers["filename"] = filename
        return res
    else:
        return None


def get_video(url):
    proxies = {
    "http": 'socks5h://127.0.0.1:1080' ,
    "https": 'socks5h://127.0.0.1:1080' ,
    }
    s = requests.Session()
    s.proxies = proxies
    s.stream = True
    res =  s.get(url,)
    body = res.content.decode("utf-8")
    # with open("1.html", "a+") as f:
    #     f.write(body)
    soup = BeautifulSoup(body, features="html.parser")
    vido_url = soup.find(attrs={"property": "og:video"}).get("content")
    if vido_url:
        res =  s.get(vido_url)
        # content_type = res.headers.get("Content-Type")
        filename = path.basename(vido_url).split("?")[0]
        filename = "video/"+filename
        if not path.isfile(filename):
            with open(filename, 'wb') as f:
                f.seek(0)
                shutil.copyfileobj(res.raw, f)

        return  {
            "video_url" : filename
        }
    else:
        return None


def get_data(*,url, tag):
    try:
        if tag == "img":
            return  get_img(url)
        elif tag == "video":
            return get_video(url)
    except Exception as e:
        print(e)
        raise ValueError("发生未知错误")
