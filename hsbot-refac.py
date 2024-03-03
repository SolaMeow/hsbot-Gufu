import asyncio
import os
# import PIL.Image as Image
from urllib.request import urlretrieve
import requests
import json
from bs4 import BeautifulSoup
import cloudscraper
import os
import random
import collections
from amiyabot import AmiyaBot, Message, Chain
import aiohttp

# init the hs bot
# read the appid and token from local bot.json
f = open('bot.json', 'r')
bot_content = json.loads(f.read())
appid, token = bot_content["appid"], bot_content["token"]
bot = AmiyaBot(appid=appid, token=token)
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

region_dict = {
    'US': '美',
    'EU': '欧',
    'AP': '亚'
}

leaderboardId_dict = {
    'WLD': '狂野',
    'STD': '标准',
    'arena': '竞技场'
}

leaderboard_dict = {
    'wild': '狂野',
    'standard': '标准'
}

async def reqRank(data: Message, region: str, leaderboardId: str, keyword: str):
    target = data.text[data.text.find(keyword):]
    id = target[5:]
    
    html = f"https://www.hsguru.com/leaderboard?leaderboardId={leaderboardId}&region={region}&search=" + id
    response = requests.get(html, headers=headers)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.body
    
    ht = body.text.split()
    if ht[0] == "Bad":
        return Chain(data).text(f'hsguru挂了，暂时查不了，有其他问题请反馈Sola')
    if leaderboardId == "STD":
        start_index = ht.index("Tour", 0, len(ht))
    else:
        start_index = ht.index("Battletag", 0, len(ht))
    
    res_ht = ht[start_index+1:]
    res_text = ""
    
    for item in res_ht:
        if not str(item).isalnum():
            res_ht.remove(item)
        if "history" in item:
            res_ht.remove(item)
            
    for i in range(0, len(res_ht)-1, 2):
        pair = "rank: " + res_ht[i] + ", " + "name: " + res_ht[i+1] + "\n"
        res_text += pair
    
    return Chain(data).text(f'{region_dict[region]}服{leaderboardId_dict[leaderboardId]}, \n{res_text}')

@bot.on_message(keywords='查美服狂野')
async def reqUSRankWLD(data: Message):
    return await reqRank(data, 'US', 'WLD', "查美服狂野")

@bot.on_message(keywords='查美服标准')
async def reqUSRankSTD(data: Message):
    return await reqRank(data, 'US', 'STD', "查美服标准")

@bot.on_message(keywords='查美服幻变')
async def reqUSRankSTD(data: Message):
    return await reqRank(data, 'US', 'twist', "查美服幻变")

@bot.on_message(keywords='查欧服狂野')
async def reqEURankWLD(data: Message):
    return await reqRank(data, 'EU', 'WLD', "查欧服狂野")

@bot.on_message(keywords='查欧服标准')
async def reqEURankSTD(data: Message):
    return await reqRank(data, 'EU', 'STD', "查欧服标准")

@bot.on_message(keywords='查亚服狂野')
async def reqAPRankWLD(data: Message):
    return await reqRank(data, 'AP', 'WLD', "查亚服狂野")

@bot.on_message(keywords='查亚服标准')
async def reqAPRankSTD(data: Message):
    return await reqRank(data, 'AP', 'STD', "查亚服标准")

async def fetch_page(session, url):
    async with session.get(url) as response:
        info = await response.text()
        json_dict = json.loads(info)
        rank_name = json_dict["leaderboard"]["rows"]
        page_results = []
        for item in rank_name:
            rank, name = item['rank'], item['accountid']
            page_results.append((rank, name))
        return page_results

async def reqRankLev(data: Message, region: str, leaderboardId: str):
    all_results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 5):
            html = f"https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region={region}&leaderboardId={leaderboardId}&page={i}"
            tasks.append(fetch_page(session, html))
        results = await asyncio.gather(*tasks)
        for page_results in results:
            all_results.extend(page_results)
    
    # Sort all results by rank
    all_results.sort(key=lambda x: x[0])
    
    # Convert sorted results to string
    res = "\n".join(f"{rank}: {name}" for rank, name in all_results)
    
    return Chain(data).text(f'{region_dict[region]}服{leaderboard_dict[leaderboardId]}月榜, \n{res}')

@bot.on_message(keywords='打印亚服狂野月榜')
async def reqAPRankeleven(data: Message):
    return await reqRankLev(data, 'AP', 'wild')

@bot.on_message(keywords='打印欧服狂野月榜')
async def reqEURankeleven(data: Message):
    return await reqRankLev(data, 'EU', 'wild')

@bot.on_message(keywords='打印美服狂野月榜')
async def reqUSRankeleven(data: Message):
    return await reqRankLev(data, 'US', 'wild')

@bot.on_message(keywords='打印美服标准月榜')
async def reqUSRankeleven(data: Message):
    return await reqRankLev(data, 'US', 'standard')

@bot.on_message(keywords='打印欧服标准月榜')
async def reqUSRankeleven(data: Message):
    return await reqRankLev(data, 'EU', 'standard')

@bot.on_message(keywords='打印亚服标准月榜')
async def reqUSRankeleven(data: Message):
    return await reqRankLev(data, 'AP', 'standard')
    
async def fetch_num(session, url):
    async with session.get(url) as response:
        info = await response.text()
        json_dict = json.loads(info)
        return json_dict["leaderboard"]["pagination"]["totalSize"]

@bot.on_message(keywords='查三服狂野人数')
async def reqNumLeaderBoard(data: Message):
    urls = [
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=US&leaderboardId=wild&page=1",
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=EU&leaderboardId=wild&page=1",
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=AP&leaderboardId=wild&page=1"
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_num(session, url) for url in urls]
        USWILD, EUWILD, APWILD = await asyncio.gather(*tasks)
    res_text = "美服：" + str(USWILD) + "\n欧服：" + str(EUWILD) + "\n亚服：" + str(APWILD)
    return Chain(data).text(f'三服狂野人数, \n{res_text}')

@bot.on_message(keywords='查三服标准人数')
async def reqNumLeaderBoard(data: Message):
    urls = [
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=US&leaderboardId=standard&page=1",
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=EU&leaderboardId=standard&page=1",
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=AP&leaderboardId=standard&page=1"
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_num(session, url) for url in urls]
        USWILD, EUWILD, APWILD = await asyncio.gather(*tasks)
    res_text = "美服：" + str(USWILD) + "\n欧服：" + str(EUWILD) + "\n亚服：" + str(APWILD)
    return Chain(data).text(f'三服标准人数, \n{res_text}')


async def reqRankArena(data: Message, region: str, leaderboardId: str, keyword: str):
    target = data.text[data.text.find(keyword):]
    id = target[len(keyword):]
    
    html = f"https://www.hsguru.com/leaderboard?leaderboardId={leaderboardId}&region={region}&search=" + id
    response = requests.get(html, headers=headers)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.body
    
    ht = body.text.split()
    start_index = ht.index("Rating", 0, len(ht))
    
    res_ht = ht[start_index+1:]
    res_text = ""
    
    for item in res_ht:
        if not str(item).isalnum():
            res_ht.remove(item)
            
    for i in range(0, len(res_ht)-1, 2):
        pair = "rank: " + res_ht[i] + ", " + "name: " + res_ht[i+1] + "\n"
        res_text += pair
    
    return Chain(data).text(f'{region_dict[region]}服{leaderboardId_dict[leaderboardId]}, \n{res_text}')

@bot.on_message(keywords='查美服竞技场')
async def reqUSRankarena(data: Message):
    return await reqRankArena(data, 'US', 'arena', "查美服竞技场")

@bot.on_message(keywords='查欧服竞技场')
async def reqEURankarena(data: Message):
    return await reqRankArena(data, 'EU', 'arena', "查欧服竞技场")

@bot.on_message(keywords='查亚服竞技场')
async def reqAPRankarena(data: Message):
    return await reqRankArena(data, 'AP', 'arena', "查亚服竞技场")

@bot.on_message(keywords='猫猫虫')
async def reqNumLeaderBoard(data: Message):
    # 查询本地图片，随机选择一个
    local_mmc = "./capoo_origin_gif"
    mmc_ = [os.path.join(local_mmc, f) for f in os.listdir(local_mmc)]
    random_mmc = random.sample(mmc_, 1)

    return Chain(data).image(random_mmc)


# @bot.on_message(keywords='代码')
# async def reqCode(data: Message):
    target = data.text_origin[data.text_origin.find("代码"):]
    deck_code = target[2:].strip()
    # deck_code = "AAEBAZICBrS7AsX9AomLBM+sBP3EBZ/zBQzpAYoOoM0CntICv/ICj/YCr4AErsAEhO8E2/oF/Y0GqZ4GAAED6awC/cQFtLsC/cQFuNkE/cQFAAA="
    url = "https://api.blizzard.com/hearthstone/deck?code=" + deck_code + "&locale=zh_CN"

    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Authorization': 'Bearer KRWpkSRImus70XdDJxtFmU78r8l2hXSIpR'
    }

    response = requests.request("GET", url, headers=headers, data={})
    json_dict = json.loads(response.text)
    deck_format = json_dict["format"]
    deck_class = json_dict["class"]["name"]
    card_list = json_dict["cards"]
    if "sideboardCards" in json_dict :
        ntr = json_dict["sideboardCards"][0]["cardsInSideboard"]
    mana_name = collections.defaultdict(list)
    name_pic = collections.defaultdict(list)
    mana_name_ntr = collections.defaultdict(list)
    name_pic_ntr = collections.defaultdict(list)

    for card in card_list:
        card_mana = card["manaCost"]
        card_name = card["name"]
        card_img = card["image"]
        
        mana_name[card_mana].append(card_name)
        name_pic[card_name].append(card_img)
        
    if "sideboardCards" in json_dict :
        for card in ntr:
            card_mana = card["manaCost"]
            card_name = card["name"]
            card_img = card["image"]
        
            mana_name_ntr[card_mana].append(card_name)
            name_pic_ntr[card_name].append(card_img)

    mana_name = sorted(mana_name.items(), key=lambda d: d[0])
    mana_name_ntr = sorted(mana_name_ntr.items(), key=lambda d: d[0])

    # card without pic, only name, support ntr
    # card with pic
    # save the card pic in ./card_source
    card_list = os.listdir("./card_source")

    for name, url in name_pic.items():
        curname = name + ".png"
        if curname not in card_list:
            location = "./card_source/" + curname 
            urlretrieve(url[0], location)

    # generate image
    row, col = 7, 7
    imgh, imgw = 404, 558

    res_img = Image.new('RGB', (col * imgh, row * imgw))
    location = []
    for mana, namelist in mana_name:
        for name in namelist:
            location.append("./card_source/" + name + ".png")
            # res_img.paste(Image.open(location))

    cnt = 0
    for y in range(1, row + 1):
        for x in range(1, col + 1):
            if cnt >= len(location):
                break
            # print(location[cnt])
            res_img.paste(Image.open(location[cnt]), ((x - 1) * imgh, (y - 1) * imgw))

            cnt += 1

        else:
            continue

    def transparent_back(img):
        img = img.convert('RGBA')
        L, H = img.size
        color_0 = img.getpixel((0,0))
        for h in range(H):
            for l in range(L):
                dot = (l,h)
                color_1 = img.getpixel(dot)
                if color_1 == color_0:
                    color_1 = color_1[:-1] + (0,)
                    img.putpixel(dot,color_1)
        return img

    # ntr
    if "sideboardCards" in json_dict :
        for name, url in name_pic_ntr.items():
            curname = name + ".png"
            if curname not in card_list:
                location = "./card_source/" + curname 
                urlretrieve(url[0], location)
                
        location = []
        for mana, namelist in mana_name_ntr:
            for name in namelist:
                location.append("./card_source/" + name + ".png")
        
        cnt = 0
        # last row
        y = 7
        for x in range(1, col + 1):
            if cnt >= len(location):
                break
            res_img.paste(Image.open(location[cnt]), ((x - 1) * imgh, (y - 1) * imgw))
            cnt += 1
        
        
    res_img = transparent_back(res_img)
    res_img.save("./deck_gen/2.png")
    
    os.system('pngquant /home/hsbot/deck_gen/2.png --force --ext res.png')
    return Chain(data).image("./deck_gen/2res.png")


@bot.on_message(keywords='查主播')
async def bli(data: Message):
    res_tag = {"0": "未开播", "1": "直播中", "2": "轮播中"}
    result = ""
    
    # 天捷
    result += liveReq(res_tag, 30033896, "天捷")

    # tsu
    result += liveReq(res_tag, 261955, "tsu")
    
    # soda
    result += liveReq(res_tag, 14138500, "soda")
    
    # fox11
    result += liveReq(res_tag, 3817924, "fox11")

    # mimei
    result += liveReq(res_tag, 30072416, "米霉")
    
    # changsha
    result += liveReq(res_tag, 539119, "长沙")
    
    # 甜宝
    result += liveReq(res_tag, 24017611, "甜宝")

    # 小指
    result += liveReq(res_tag, 24405493, "小指")

    # 神抽狗
    result += liveReq(res_tag, 22637234, "神抽狗")

    # lingmeng
    result += liveReq(res_tag, 26919877, "lingmeng")

    # nanami
    result += liveReq(res_tag, 26101101, "nanami")

    # taffy
    result += liveReq(res_tag, 22603245, "taffy")
    
    # azusa
    result += liveReq(res_tag, 80397, "阿梓")
    
    # 東雪蓮
    result += liveReq(res_tag, 22816111, "東雪蓮")
    
    # 010
    result += liveReq(res_tag, 21452505, "010")
    
    # 眞白かのん
    result += liveReq(res_tag, 21402309, "眞白かのん")

    # 星瞳
    result += liveReq(res_tag, 22886883, "星瞳")
    
    # 雫るる
    result += liveReq(res_tag, 21013446, "雫るる")

    # 猫雷
    result += liveReq(res_tag, 22676119, "猫雷")
        
    return Chain(data).text(result)

def liveReq(res_tag, id, name):
    url = "https://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(id)

    response = requests.request("GET", url, headers=headers, data={})
    json_dict = json.loads(response.text)
    result = name + ": " + res_tag[str(json_dict["data"]["live_status"])] + "\n"
    if json_dict["data"]["live_status"] == 1:
        result += "房间号：" + str(id) + "\n"
    return result


# 新增审核
@bot.on_message(keywords='传说人数')
async def reqNumLeaderBoard(data: Message):
    urls = [
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=US&leaderboardId=wild&page=1",
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=EU&leaderboardId=wild&page=1",
        "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=AP&leaderboardId=wild&page=1"
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_num(session, url) for url in urls]
        USWILD, EUWILD, APWILD = await asyncio.gather(*tasks)
    
    res_text = "快捷查询只能查狂野，标准需要使用教程中的命令。" + "\n"
    res_text += "美服：" + str(USWILD) + "\n欧服：" + str(EUWILD) + "\n亚服：" + str(APWILD) 

    return Chain(data).text(f'三服狂野人数, \n{res_text}')


@bot.on_message(keywords='月榜查询')
async def reqRankLev(data: Message):
    all_results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 5):
            html = f"https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=US&leaderboardId=wild&page={i}"
            tasks.append(fetch_page(session, html))
        results = await asyncio.gather(*tasks)
        for page_results in results:
            all_results.extend(page_results)
    
    # Sort all results by rank
    all_results.sort(key=lambda x: x[0])
    
    # Convert sorted results to string
    res = "\n".join(f"{rank}: {name}" for rank, name in all_results)
    
    return Chain(data).text(f'快捷查询只能查狂野，其他服务器需要使用教程中的命令, \n{res}')

asyncio.run(bot.start())
