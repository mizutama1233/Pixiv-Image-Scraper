import requests, json, os
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Referer': "https://www.pixiv.net/"
}

userId = input("User Id : ")

userpage = requests.get(f"https://www.pixiv.net/users/{userId}")
user_soup = bs(userpage.text, 'html.parser')
user_meta = json.loads(user_soup.find_all('meta')[-1].get('content'))
user_name = user_meta["user"][userId]["name"]

data = requests.get(f"https://www.pixiv.net/ajax/user/{userId}/profile/all").json()
if data["error"] == False:

    fo_name = f"images/{user_name}"
    current_path = os.getcwd()
    new_fo_path = os.path.join(current_path, fo_name)
    os.makedirs(new_fo_path, exist_ok=True)
    illusts = data["body"]["illusts"]
    keys = list(illusts.keys())
    print(len(keys))

    for illustId in keys:
        p = 0
        while True:
            html = requests.get(f"https://www.pixiv.net/artworks/{illustId}")
            soup = bs(html.text, "lxml")
            meta = soup.find_all("meta")[-1]
            meta_content = json.loads(meta.get("content"))

            img_url = meta_content["illust"][f"{illustId}"]["urls"]["original"]
            img_url = img_url.replace("_p0", f"_p{p}")
            p += 1
            img_name = img_url.split("/")[-1]

            
            r = requests.get(img_url, stream=True, headers=headers)
            if r.status_code == 200:
                print(f"{img_url}:  {img_name}")
                with open(f"./images/{user_name}/{img_name}", "wb") as f:
                    f.write(r.content)
                print("Success")
            if r.status_code == 404:
                break
        
