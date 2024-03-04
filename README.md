<!-- projectInfo  -->
<div align="center">
    <img alt="hsbot" src="./fig/gufu.png" width=280 height=230/
    >

# 古夫Gufu-hsbot

Gufu-hsbot是基于 [AmiyaBot](https://www.amiyabot.com/) 框架的 QQ 聊天机器人<br>


</div>
<!-- projectInfo end -->

<div>
    <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
    <img alt="version" src="https://img.shields.io/badge/version-1.0-orange">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.7-%233776AB?logo=python&logoColor=white"><br>
</div>

    「成长，生命，幸福，还有朋友」 -- 野性之心•古夫


## 功能

1. **三服排名查询**：在频道内输入“@古夫-hsbot 查（美/欧/亚）服（狂野/标准）（id）”。例如：`查美服狂野Sola`。
2. **三服月榜（前百）查询**：在频道内输入“`@古夫-hsbot 打印美服狂野月榜`”。
3. **查三服传说人数**：在频道内输入“`@古夫-hsbot 查三服（标准/狂野）人数`”。
4. **随机猫猫虫图片**：输入“`@古夫-hsbot 猫猫虫`”。
5. **查询主播开播情况**：查询方式为输入“`@古夫-hsbot 查主播`”。
6. **查三服竞技场排名**：查询方式为在频道内输入“`@古夫-hsbot 查（美/欧/亚）服竞技场（id）`”。

## 使用

如果你仅想体验古夫的功能，可以直接加入正在使用Gufu-hsbot的QQ频道。

### 古夫的查询频道

小团体，完整功能，及时性bug反馈。如果仅体验古夫功能或者提出相关问题，加入链接[古夫的查询频道](https://pd.qq.com/s/44ww72e4s)。

### 炉石传说讨论群

炉石传说讨论群是目前QQ频道中相对最活跃的玩家社区，成员人数超5000人，除古夫之外还提供交流讨论、新卡速递等信息源。加入链接[炉石传说讨论群](https://pd.qq.com/s/cfdq2t6rr)。

## 本地化部署

如果你想私有化部署古夫，有以下三种途径。但是首先，你需要将你的机器人的`botid`与`token`保存在根目录下的json文件中，文件格式类似于：

```json

{
    "appid":"xxx",
    "token":"xxx"
}

```

### 本地编译 🥰

按照提供的[`environment.yml`](https://github.com/SolaMeow/hsbot-Gufu/blob/main/environment.yml) 部署conda环境。

部署完成之后，在根目录下执行

``` shell

conda activate hsbot

python3 hsbot_refac.py

```

### docker本地编译 🤗


``` shell

docker build -t hsbot .

docker run -dP --restart always --name my_hsbot -v ./bot.json:/app/bot.json -v ./capoo_origin_gif:/app/capoo_origin_gif hsbot

```

### docker镜像部署 😎

推荐使用这种方式进行部署。

``` shell

docker pull mildfol/hsbot:latest

docker run -dP --restart always --name my_hsbot -v ./bot.json:/app/bot.json -v ./capoo_origin_gif:/app/capoo_origin_gif hsbot

```

将机器人添加到你的频道，然后按照上述指令进行操作即可。


## 贡献

如果你有任何建议或问题，欢迎提issue或者加QQ频道反馈。


## 版本信息

### 历史版本：V1

- [x] 继承私有仓库hsbot-V1.6及对应机器人功能。
- [x] 在此基础上重构hsbot代码，整理部署文档，新增部署方式。
- [x] 移除问题功能三个：卡组代码转卡组图片预览，Bark版主播开播提醒，Hsreplay高胜职业/卡组信息。

### 当前版本：V2

- [x] 重构代码，进一步移除hsguru依赖，查询月榜改为官方源。
- [x] 重构代码，查询月榜与传说人数功能改为并行执行，查询速度提升至5s内。

### 下版本V3待补充功能

- [x] 镜像上传至docker hub。
- [ ] 修复问题功能Hsreplay高胜职业/卡组信息。
- [ ] 修复问题功能卡组代码转卡组图片预览。
- [ ] 可能的新增功能。
- [x] 数据来源与隐私策略补充。


## 数据来源

- [炉石传说官方API](https://develop.battle.net/documentation/hearthstone/game-data-apis)
- [d0nkey.top](https://www.hsguru.com/)
- Bilibili直播API

## 许可证

[MIT](https://choosealicense.com/licenses/mit/)