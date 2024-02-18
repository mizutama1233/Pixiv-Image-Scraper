import requests, json, os, time
from bs4 import BeautifulSoup as bs

# cookies = ''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Referer': "https://www.pixiv.net/",
    # 'Cookie': cookies
}
current_path = os.getcwd()

userId = input("User Id : ")

userpage = requests.get(f"https://www.pixiv.net/users/{userId}", headers=headers)
user_soup = bs(userpage.text, 'html.parser')
user_meta = json.loads(user_soup.find_all('meta')[-1].get('content'))
user_name = user_meta["user"][userId]["name"]

data = requests.get(f"https://www.pixiv.net/ajax/user/{userId}/profile/all", headers=headers).json()
if data["error"] == False:
    folder_name = f"images/{user_name}"
    new_folder_path = os.path.join(current_path, folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    illusts = data["body"]["illusts"]
    keys = list(illusts.keys())
    print(len(keys))

    for illustId in keys:
        p = 0
        
        html = requests.get(f"https://www.pixiv.net/artworks/{illustId}", headers=headers)
        if html.status_code == 429:
            print("Status 429 error.")
            time.sleep(10)
        soup = bs(html.text, "lxml")
        meta = soup.find_all("meta")[-1]
        meta_content = json.loads(meta.get("content"))
        img_url = meta_content["illust"][f"{illustId}"]["urls"]["original"]

        while True:
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
else:
    print("could not find user")
