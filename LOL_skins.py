#encoding = 'utf-8'
import requests,json,os
from PIL import Image
from io import BytesIO

url = 'https://lol.qq.com/biz/hero/champion.js'
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}
res = requests.get(url,headers = headers )
res.encoding = 'gbk'
html = res.text
print(html)
data = json.loads("{"+res.text.strip("if(!LOLherojs)var LOLherojs={};LOLherojs.champion=")+"}")
# print(data)
heroid_list = []
hero_cnnames = []
hero_names = data.get("data").keys()
print(hero_names)
for hero_name in hero_names:
    heroid_list.append(hero_name)
print(heroid_list)
for heroid in heroid_list:
    print(heroid)
    first_name = data.get("data").get(heroid).get("name")
    second_name = data.get("data").get(heroid).get("title")
    hero_cnname = first_name + " " + second_name
    #print(hero_cnname)
    hero_cnnames.append(hero_cnname)
print(hero_cnnames)

for i in range(len(heroid_list)):
    id = heroid_list[i]
    hero_url = 'https://lol.qq.com/biz/hero/' + id + '.js'
    res = requests.get(hero_url, headers=headers)
    data = json.loads("{" + res.text.strip("if(!LOLherojs)var LOLherojs={champion:{}};LOLherojs.champion." + id + "=") + "}")
    # print(data)
    skins = data.get("data").get("skins")
    skin_ids = []
    skin_names = []
    skin_urls = []
    for skin in skins:
        skin_names.append(skin.get("name"))
        skin_ids.append(skin.get("id"))
    skin_names[0] = hero_cnnames[i]  # 将默认皮肤default的名称改为英雄名称
    #print(skin_names)
    for skin_id in skin_ids:
        skin_url = "https://ossweb-img.qq.com/images/lol/web201310/skin/big" + skin_id + ".jpg"
        skin_urls.append(skin_url)
    #print(skin_urls)
    for j in range(len(skin_ids)):
        filename = "D:\\LOL\\" + hero_cnnames[i] + "\\" + skin_names[j] + ".jpg"
        filepath = "D:\\LOL\\" + hero_cnnames[i] + "\\"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        try:
            res = requests.get(skin_urls[j])
            image = Image.open(BytesIO(res.content))
            image.save(filename)
            print('成功下载' + skin_names[j] + '.jpg')
        except:
            sname = skin_names[j].replace('/', '')
            filename = "D:\\LOL\\" + hero_cnnames[0] + "\\" + sname + ".jpg"
            res = requests.get(skin_urls[j])
            image = Image.open(BytesIO(res.content))
            image.save(filename)
            print('成功下载' + skin_names[j] + '.jpg')
print('所有皮肤下载完成')
