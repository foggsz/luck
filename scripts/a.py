# from Crypto.Cipher import AES
# print(AES)
# import requests
# from bs4 import BeautifulSoup 
# import shutil
# from os import path
# proxies = {
#     "http": 'socks5h://127.0.0.1:1080' ,
#     "https": 'socks5h://127.0.0.1:1080' ,
# }
# s = requests.Session()
# s.proxies = proxies
# s.stream = True


# def get_img(url):
#     res =  s.get(url)
#     body = res.content.decode("utf-8")
# #     with open("1.html", "a+") as f:
# #         f.write(body)
#     soup = BeautifulSoup(body, features="html.parser")
#     img_url = soup.find(attrs={"property": "og:image"}).get("content")
#     if img_url:
#         res =  s.get(img_url)
#         res.raw.decode_content = True
#         filename = path.basename(img_url).split("?")[0]
#         with open(filename, 'wb') as f:
#             shutil.copyfileobj(res.raw,f)
#     else:
#         return None

# def get_body(*,url, tag):
#     if tag == "img":
#         get_img(url)


# get_body(**{'url': "https://www.instagram.com/p/BrdL6Kwgmdo/?utm_source=ig_web_button_share_sheet", 'tag':'img'})



 