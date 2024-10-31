import base64
import json
import random
from time import sleep
import io
import sys
import os
from typing import Dict
import nonebot
# 规则
from nonebot.rule import Rule, to_me
# 框架规则
from nonebot import on_command, require, on_notice, on_message, on_regex, on_request
# 通讯协议
from nonebot.adapters.onebot.v11 import Event, Bot, Message, MessageSegment, Adapter, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent, PokeNotifyEvent, GroupMessageEvent, GroupRequestEvent
# QQ白名单
from plugins.chobits.white_list_qq import white_list_qq
# 群白名单
from plugins.chobits.white_list_group import white_list_group
# 处理 Markdown
from plugins.chobits.handle_markdown import menu as handle_markdown_menu, get_send_markdown_message, develop_menu as handle_markdown_develop_menu
# httpx
import httpx
# 事件响应器
from nonebot.matcher import Matcher
# 参数
from nonebot.params import CommandArg, ArgPlainText
# 聊天机器人
from plugins.chobits.chat import chat

from datetime import datetime

from nonebot import get_driver
from nonebot.drivers import URL, Request, Response, ASGIMixin, HTTPServerSetup

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler


# 机器人白名单
async def is_bot_white_list(event: Event, bot: Bot) -> bool:
    # 获取当前bot的QQ
    bot_qq = str(bot.self_id)
    if bot_qq in ['3218366812']:
        return False
    else:
        return True


# 好友白名单
async def is_qq_white_list(event: Event) -> bool:
    if event.get_user_id() in ['319203727', '3077334686', '3192299626', '2123537057', '1758657468', '1786222977', '1030736086']:
        return False
    return True
    # return event.get_user_id() in white_list_qq


# 群白名单
async def is_group_white_list(event: Event) -> bool:
    # if event.group_id == '115082089':
    #     pass
    return True
    # if event.sub_type == 'normal':
    #     return str(event.group_id) in white_list_group
    # else:
    #     return True


# 禁言权限
async def is_group_ban(event: Event) -> bool:
    return False


ban_rule = Rule(is_group_ban)

# 规则权限
rule = Rule(is_qq_white_list, is_group_white_list, is_bot_white_list)


# 发送 Markdown
async def send_markdown(bot, event, markdown):
    qq = event.get_user_id()
    if event.sub_type == 'normal':
        await bot.send_group_msg(group_id=event.group_id, message=markdown)
        await menu.finish()
        # await menu.finish(MessageSegment.at(qq))
    else:
        await bot.send_private_msg(user_id=int(qq), message=markdown)
        await menu.finish()


# 监听
chat_rule = on_regex(pattern=r'.*', rule=rule)


@chat_rule.handle()
async def handle_chat_rule(bot: Bot, event: Event):
    qq = event.get_user_id()
    if qq == '3218366812' and event.sub_type == 'normal':
        await bot.call_api(api="set_group_reaction", group_id=event.group_id, message_id=event.message_id, code='66')
    if qq == '3267675260' and event.sub_type == 'normal':
        await bot.call_api(api="set_group_reaction", group_id=event.group_id, message_id=event.message_id, code='298')
    if qq == '229073389' and event.sub_type == 'normal':
        await bot.call_api(api="set_group_reaction", group_id=event.group_id, message_id=event.message_id, code='344')
    if qq == '3420673881' and event.sub_type == 'normal':
        await bot.call_api(api="set_group_reaction", group_id=event.group_id, message_id=event.message_id, code='265')
    if qq == '1553712360' and event.sub_type == 'normal':
        await bot.call_api(api="set_group_reaction", group_id=event.group_id, message_id=event.message_id, code='38')
    print(qq)
    current_message = event.get_plaintext()
    print(current_message)
    # 禁言监听
    taboo_list = ['nm', 'cnm', 'sz', 'lz', '艹',
                  '操你妈', '你妈', '草泥马', '特么的', '撕逼', '玛拉戈壁', '爆菊',
                  'JB', '呆逼', '本屌', '齐B短裙', '法克鱿', '丢你老母', '扑街',
                  '达菲鸡', '装13', '逼格', '蛋疼', '傻逼', '绿茶婊', '煞笔', '狗屎',
                  '你妈的', '表砸', '屌爆了', '买了个婊', '已撸', '吉跋猫', '妈蛋',
                  '逗比', '我靠', '碧莲', '碧池', '然并卵', '日了狗', '狗东西',
                  '屁民', '吃翔', 'xx狗', '淫家', '你妹', '浮尸国', '滚粗',
                  '性生活', '性交', '生殖器', '回回', '靴子', '高丽棒子',
                  '老毛子', '黑鬼', '血统', '杂种', '东亚病夫', '蛮夷',
                  '大男人', '小女人', '男尊女卑', '重男轻女']
    if any(str(current_message).find(taboo_string) != -1 for taboo_string in taboo_list):
        message = Message(
            [
                MessageSegment.reply(event.message_id),
                MessageSegment.at(qq),
                MessageSegment.text("你已经触犯了银河正义法中不可饶恕之侮辱谩骂罪,我阿离宣布剥夺你的一切权利并对你进行封印缉捕，束手就擒吧！")
            ]
        )
        await chat_rule.send(MessageSegment.image("file:///work/Python/chat-qq-bot/plugins/chobits/image/73E15FE56632C556C2FB8E9D99C2E1C3.jpg"))
        await chat_rule.send(message)
        if event.sub_type == 'normal':
            group = event.group_id
            if qq not in ['3218366812']:
                await bot.set_group_ban(group_id=group, user_id=int(qq), duration=60 * 60 * 24 * 2)
        await chat_rule.finish()
    # text_list = ["你这人是不是出生脑袋屁股长反了呀?说话有一股子屎味,你干脆别说话了，去医院看看吧,让医生给你脑袋装下面去", "有父母生没父母教的智障东西去死吧!"]
    # text = random.choice(text_list)
    # if qq in ['2917382816']:
    #     message = Message(
    #         [
    #             MessageSegment.at(qq),
    #             MessageSegment.text(text)
    #         ]
    #     )
    #     await chat_rule.finish(message)
    # if qq in ['1553712360']:
    #     if event.sub_type == 'normal':
    #         await bot.call_api(api="set_group_reaction", group_id=event.group_id, message_id=event.message_id, code='38')
    #     message = Message(
    #         [
    #             MessageSegment.at(qq),
    #             MessageSegment.text("变态来啦!变态来啦!")
    #         ]
    #     )
    #     await chat_rule.finish(message)
    # await chat_rule.finish()


# 菜单
menu = on_command('菜单', rule=rule)


@menu.handle()
async def handle_menu(bot: Bot, event: Event):
    # markdown = await handle_markdown_menu(bot=bot)
    # await send_markdown(bot=bot, event=event, markdown=markdown)
    group = event.group_id
    qq = event.get_user_id()
    message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text("""
主动技能:
0. 菜单
1. 随机图片
2. 随机视频
3. 猜数字(非同一般的猜数字,请随时打乱别人的数字[喜])
4. 戳(戳,就是戳咯)
5. 召唤喵天依~
6. 招魂(都说是招魂啦!)
7. 今日占卜(不负责占卜,小声哔哔:不准的话不准怪我哦~)
8. 纸片人老婆征集(待定,我没鸽!)
9. 喵(你叫一下试试呗)
10. 唱歌(暂时就那几首随机播放)
11. 阿离(就...叫一下阿离?)
12. 汪(你叫一下试试呗)
13. 工作时间(阿离是有工作时间的哦[小声哔哔:才不是主人的上班时间呢])

被动技能:
1. 每小时报时
2. Ciallo卖萌
3. 骂人违禁词逮捕

注: 想要加的有趣功能可以和雪兔提哦~"""),
            MessageSegment.image("file:///work/Python/chat-qq-bot/plugins/chobits/image/D0EF1CCF4494D5481D2523A02A350417.webp"),
        ]
    )
    try:
        await bot.call_api("group_poke", group_id=group, user_id=qq)
    except Exception as e:
        poke_message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text("呜呜呜,戳不到你啦.")
            ]
        )
        await menu.send(poke_message)
        print(e)
    await menu.finish(message)


# 开发菜单
develop_menu = on_command('开发菜单', rule=rule)


@develop_menu.handle()
async def handle_develop_menu(bot: Bot, event: Event):
    markdown = await handle_markdown_develop_menu(bot=bot)
    await send_markdown(bot=bot, event=event, markdown=markdown)


# 点赞
like = on_command('点赞', rule=rule)


@like.handle()
async def handl(event: Event, bot: Bot):
    qq = event.get_user_id()
    for i in range(20):
        # 阻塞 1 秒
        sleep(1)
        await bot.send_like(user_id=int(qq), times=10)
    await like.finish('点赞完成')


def get_all_files(directory):
    """
    获取指定目录下的所有文件
    """
    files = []
    # 获取目录下的所有文件和文件夹的列表
    entries = os.listdir(directory)
    # 过滤出所有文件
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
    return files


anime_image_list = []

files = get_all_files('/work/PHP/phpinfo/Image/anime/')
for file in files:
    anime_image_list.append({'url': f'file:///work/PHP/phpinfo/Image/anime/{file}'})

obscene_image_list = []

files = get_all_files('/work/PHP/phpinfo/Image/obscene/')
for file in files:
    obscene_image_list.append({'url': f'file:///work/PHP/phpinfo/Image/obscene/{file}'})

# 随机图片
image = on_command('随机图片', rule=rule)


@image.handle()
async def handle_image(event: Event, bot: Bot):
    global anime_image_list, obscene_image_list
    image_list = anime_image_list
    print(event.group_id)
    if event.sub_type == 'normal':
        if str(event.group_id) in ['881971669']:
            await image.finish("本群已禁用此功能")
    image_info = random.choice(image_list)
    url = image_info['url']
    await image.finish(MessageSegment.image(url))


# 戳
group_poke = on_command('戳', rule=rule)


@group_poke.handle()
async def handle_group_poke(event: Event, bot: Bot):
    group = event.group_id
    try:
        qq = event.get_message()["at"][0].data["qq"]
    except Exception as e:
        print(e)
        qq = event.get_user_id()
    if qq == "3218366812":
        poke_message = Message(
            [
                MessageSegment.at(event.get_user_id()),
                MessageSegment.text(" 你坏!不准戳主人!")
            ]
        )
        await group_poke.finish(poke_message)
    try:
        await bot.call_api("group_poke", group_id=group, user_id=qq)
    except Exception as e:
        print(e)
        poke_message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text("呜呜呜,戳不到你啦.")
            ]
        )
        await group_poke.finish(poke_message)
    await group_poke.finish()


# # 毒鸡汤
# poisonous = on_command('毒鸡汤', rule=rule)
#
# @poisonous.handle()
# async def handle_poisonous():
#     # 创建一个异步client
#     async with httpx.AsyncClient() as client:
#         message = await client.get('https://api.wer.plus/api/djt', timeout=None)
#         if message.status_code == 200:
#             await poisonous.finish(message.json()['data']['comment'])

# 获取最新提交
git_last_commit = on_command('最新提交', rule=rule)


@git_last_commit.handle()
async def handle_resid(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("owner_ref", args)


@git_last_commit.got("owner_ref", prompt="请输入 帐户所有者/仓库名")
async def got_resid(event: Event, bot: Bot, owner_ref: str = ArgPlainText()):
    # 创建一个异步client
    async with httpx.AsyncClient() as client:
        message = await client.get(f'https://api.github.com/repos/{owner_ref}/commits', timeout=None)
        if message.status_code == 200:
            await git_last_commit.finish(message.json()[0]['sha'])


# 测试resid
test_resid = on_command("测试resid", rule=rule)


@test_resid.handle()
async def handle_resid(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("resid", args)


@test_resid.got("resid", prompt="请输入resid")
async def got_resid(event: Event, bot: Bot, resid: str = ArgPlainText()):
    markdown = {
        "type": "longmsg",
        "data": {
            "id": resid
        }
    }
    await send_markdown(bot=bot, event=event, markdown=markdown)


# 测试forward
test_forward = on_command("测试forward", rule=rule)


@test_forward.handle()
async def handle_forward(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("forward", args)


@test_forward.got("forward", prompt="请输入forward")
async def got_forward(event: Event, bot: Bot, forward: str = ArgPlainText()):
    markdown = {
        "type": "forward",
        "data": {
            "id": forward
        }
    }
    await send_markdown(bot=bot, event=event, markdown=markdown)


# 测试Markdown
test_markdown = on_command("测试Markdown", rule=rule)


@test_markdown.handle()
async def handle_markdown(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("markdown", args)


@test_markdown.got("markdown", prompt="请输入Markdown")
async def got_markdown(event: Event, bot: Bot, markdown: str = ArgPlainText()):
    markdown = await get_send_markdown_message(bot=bot, markdown=markdown)
    await send_markdown(bot=bot, event=event, markdown=markdown)


# 测试JSON
test_json = on_command('测试JSON', rule=rule)


@test_json.handle()
async def handle_json(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("json", args)


@test_json.got("json", prompt="请输入JSON")
async def got_markdown(event: Event, bot: Bot, json: str = ArgPlainText()):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.json(json),
            MessageSegment.at(qq),
        ]
    )
    if event.sub_type == 'normal':
        await test_json.finish(data)
    else:
        await test_json.finish(data)


# 横向图卡
transverse = on_command('横向图卡', rule=rule)


@transverse.handle()
async def handle_transverse(bot: Bot, event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.json(
                '{"app":"com.tencent.imagetextbot","config":{"autosize":1,"ctime":1710228958,"token":"9b4a4df03888800526c55924d51024b1"},"meta":{"robot":{"cover":"https:\/\/api.mrgnb.cn\/api\/tz.php?url=https:\/\/api.likepoems.com\/img\/pc\/","jump_url":"","subtitle":"","title":""}},"prompt":"\u52a8\u753b\u8868\u60c5","ver":"1.0.0.14","view":"index"}'),
            MessageSegment.at(qq),
        ]
    )
    await transverse.finish(data)


# 纵向图卡
portrait = on_command('纵向图卡', rule=rule)


@portrait.handle()
async def handle_portrait(bot: Bot, event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.json(
                '{"app":"com.tencent.imagetextbot","config":{"autosize":1,"ctime":1710231632,"token":"ea4fa7feefea09749a8b81c16b71789b"},"meta":{"robot":{"cover":"https:\/\/api.mrgnb.cn\/api\/tz.php?url=https:\/\/gchat.qpic.cn\/offpic_new\/3218366812\/\/3218366812-1260311223-6FA5EE584CFE32B0D7C2383FEB36A5B4\/0","jump_url":"","subtitle":"","title":""}},"prompt":"\u52a8\u753b\u8868\u60c5","ver":"1.0.0.14","view":"index"}'),
            MessageSegment.at(qq),
        ]
    )
    await portrait.finish(data)


# Lagrange.Core
lagrange = on_command('Lagrange.Core', rule=rule)


@lagrange.handle()
async def handle_lagrange(bot: Bot, event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.json(
                '{"app":"com.tencent.imagetextbot","config":{"autosize":1,"ctime":1710677816,"token":"c29d7804384eb855dcc4269df748537f"},"meta":{"robot":{"cover":"https:\/\/api.mrgnb.cn\/api\/tz.php?url=https:\/\/api.kaitomoe.org\/lgrbanner.php","jump_url":"","subtitle":"","title":""}},"prompt":"[Lagrange.Core]","ver":"1.0.0.14","view":"index"}'),
            MessageSegment.at(qq),
        ]
    )
    await lagrange.finish(data)


# 对话
dialogue = on_command('对话', rule=rule)


@dialogue.handle()
async def handle_dialogue(bot: Bot, event: Event):
    qq = event.get_user_id()
    message = event.get_message()
    string = str(message).replace('对话 ', '')
    member = await bot.get_stranger_info(user_id=int(qq))
    markdown = await chat(bot=bot, message=string, qq=qq, nickname=member['nickname'])
    await send_markdown(bot, event, markdown)


# 获取信息中所有at的qq
def get_qq_list(obj: Message) -> list[str]:
    return [i.data["qq"] for i in obj["at"]]


# 全群禁言
group_ban = on_command('全群禁言', rule=ban_rule)


@group_ban.handle()
async def handle_group_ban(bot: Bot, event: Event):
    if event.sub_type == 'normal':
        group = event.group_id
        await bot.set_group_whole_ban(group_id=group, enable=True)
        await group_ban.finish("禁言成功~")


# 全群解禁
group_lift_ban = on_command('全群解禁', rule=rule)


@group_lift_ban.handle()
async def handle_group_lift_ban(bot: Bot, event: Event):
    if event.sub_type == 'normal':
        group = event.group_id
        await bot.set_group_whole_ban(group_id=group, enable=True)
        await group_lift_ban.finish("解除成功~")


# 单人禁言
user_ban = on_command(cmd='单人禁言', aliases={'禁言', '封印'}, rule=ban_rule)


@user_ban.handle()
async def handle_group_ban(bot: Bot, event: Event):
    message = event.get_message()
    try:
        qq = message["at"][0].data["qq"]
    except Exception as e:
        qq = event.get_user_id()

    duration = random.randint(1, 60)
    if event.sub_type == 'normal':
        group = event.group_id
        if qq in ['3218366812']:
            await bot.set_group_ban(group_id=group, user_id=int(event.get_user_id()), duration=duration)
            await user_ban.finish("此号禁止禁言~")
        else:
            await bot.set_group_ban(group_id=group, user_id=int(qq), duration=duration)
            await user_ban.finish("禁言成功~")


# 单人解禁
user_lift_ban = on_command('单人解禁', aliases={'解禁', '解封'}, rule=ban_rule)


@user_lift_ban.handle()
async def handle_group_ban(bot: Bot, event: Event):
    message = event.get_message()
    qq = message["at"][0].data["qq"]
    if event.sub_type == 'normal':
        group = event.group_id
        await bot.set_group_ban(group_id=group, user_id=int(qq), duration=0)
        await user_lift_ban.finish("解除成功~")


# 召唤喵天依~
mew = on_command('召唤喵天依~', rule=rule)


@mew.handle()
async def handle_mew():
    await mew.send(MessageSegment.image("/work/PHP/phpinfo/Image/Download/D507CDC00A8896981A70648BD2B6466F.jpg"))
    await mew.send("喵天依应召而来~")
    await mew.finish()


# 招魂
evocation = on_command('招魂', rule=rule)


@evocation.handle()
async def handle_evocation():
    await evocation.finish("""
魂兮归来...
𓀃𓀅𓀇𓀋𓀌
魂兮归来.....驱长鞭而架六辔兮....
𓀌𓀎𓀠𓀤𓀫
魂兮归来...翻山而歌兮...归来....魂兮归来...
𓀋𓀌𓀎𓀙𓀠
魂兮归来...振高歌而凯旋兮...期同袍而尽泽...
𓀋𓀠𓀤𓀥𓀫
魂兮归来...魂兮归来....
𓀋𓀌𓀎𓀙𓀠𓀤𓀥𓀫𓀃𓀅𓀇𓀋𓀌𓀀𓀁𓀃𓀅𓀇𓀋𓀌

""")


# 铁锈指令
rusted_warfare = on_command('铁锈指令', rule=rule)


@rusted_warfare.handle()
async def handle_rusted_warfare():
    await rusted_warfare.finish("""
.start 开始
.stop 停止
.maps 列出地图列表
.map 选择某地图
.fog off 无雾
.fog basic 黑幕
.fog los 迷雾
.startingunits 开局单位
.credits 开局金钱
.income α 生产金钱的倍数(“α”可替换为1、2、3)
.addai 增加一个AI
.ai α AI的难度(“α”必须为整数)
.nukes true 未禁核
.nukes false 禁核
.sharedControl true 队友共享控制
.sharedControl false 关闭共享
.share off 房主开启共享时可用此指令拒绝共享
.t (说话内容) 和队友聊天，其他队伍的人看不到你和队友说话的
.afk 如果房主在30秒内不说话，则将房主权限给你
.give ID 把房主权限给予指定玩家
.who 查看谁为房主
.kick ID 踢某人(注意空格) (“ID”可替换为玩家名称)
.move 1 3 (注意空格)交换位置来更换出生点
备注：以上命令直接在聊天栏中输入并发送即可。

""")


# 随机视频
video = on_command('随机视频', rule=rule)


@video.handle()
async def handle_video(event: Event, bot: Bot):
    qq = event.get_user_id()
    url_list = ["https://www.yujn.cn/api/heisis.php", "https://api.yujn.cn/api/xjj.php?type=video"]
    url = random.choice(url_list)
    if event.sub_type == 'normal':
        if str(event.group_id) in ['881971669']:
            await image.finish("本群已禁用此功能")
    await video.send(MessageSegment.video(url))
    await video.finish(MessageSegment.at(qq))


# 测试大图
big_picture = on_command('测试大图', rule=rule)


@big_picture.handle()
async def handle_big_picture(event: Event, bot: Bot):
    await big_picture.send(MessageSegment.image("file:///work/PHP/phpinfo/Image/anime/9EC82833B80001DF57065DA697A418CA.jpg"))


# 勇敢的心
video = on_command('勇敢的心', rule=rule)


@video.handle()
async def handle_video(event: Event, bot: Bot):
    qq = event.get_user_id()
    # await video.send(MessageSegment.record("/mnt/e/Work/PHP/my/SnowRabbit/storage/app/public/music/ud7qo-txck6.wav"))
    await video.send(MessageSegment.record("https://webfs.hw.kugou.com/202404201515/9fd67d5b3a78dbfdc174ae2672643399/v2/b9a974e272f36cead2b2e693121fcd82/G366/M00/0C/28/TpUEAGVLZMCAKV05AEICsH8LxvM801.mp3"))
    await video.finish(MessageSegment.at(qq))


# 嘤嘤嘤
yingyingying = on_command('嘤嘤嘤', rule=rule)


@yingyingying.handle()
async def handle_yingyingying(event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(" 我一拳一个嘤嘤怪~"),
        ]
    )
    await yingyingying.finish(data)


# 呜呜呜
wuwuwu = on_command('呜呜呜', rule=rule)


@wuwuwu.handle()
async def handle_wuwuwu(event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(" 我一拳一个呜呜怪~"),
        ]
    )
    await wuwuwu.finish(data)


# 获取信息
info = on_command('获取信息', rule=rule)


@info.handle()
async def handle_info(bot: Bot, event: Event):
    qq = event.get_user_id()
    member = await bot.get_stranger_info(user_id=int(qq))
    # member = await bot.get_group_member_info(group_id=event.group_id, user_id=int(qq))
    print(member['nickname'])
    data = Message(
        [
            MessageSegment.image(f"https://q1.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640"),
            MessageSegment.at(qq),
        ]
    )
    await info.finish(data)


# 我喜欢你
i_love_you = on_command('我喜欢你', rule=rule)


@i_love_you.handle()
async def handle_i_love_you(bot: Bot, event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(f' 阿离也喜欢你呢~ 贴贴~'),
            MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/A37E28B2EADF3AFE84D9E476FF779882.jpg"),
        ]
    )
    await i_love_you.finish(data)


# 真的吗
really = on_command('真的吗', rule=rule)


@really.handle()
async def handle_really(bot: Bot, event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.reply(event.message_id),
            MessageSegment.at(qq),
            MessageSegment.text(f' 当然是真的哦~'),
        ]
    )
    await really.finish(data)


# 可爱
lovely = on_regex(r'可爱', rule=rule)


@lovely.handle()
async def handle_lovely(bot: Bot, event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.text('阿离也觉得好可爱呢~'),
        ]
    )
    await lovely.finish(data)


# 获取信息
dm = on_command('dm', rule=rule)


@dm.handle()
async def handle_dm():
    await dm.finish(MessageSegment.image(f"https://manhua.acimg.cn/manhua_detail/0/15_15_57_2c33f6e3c9a1d2fbacad119f92912506_1171.jpg/0"))


# 我是谁
who_am_i = on_command('我是谁', rule=rule)


@who_am_i.handle()
async def handle_who_am_i(event: Event):
    qq = event.get_user_id()
    if qq == '3218366812':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是阿离的主人哦~'),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '1553712360':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f""" 你是一只变态的话唠猫猫!!!
(变态猫娘,变态猫娘,变态猫娘.)"""),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '3267675260':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你呀,你是超级大笨蛋呢~'),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '3136889839':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是一天天只会犯贱的贱逼~(呜呜呜,为什么要逼阿离这么说,哭唧唧)'),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '3665258498':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是一只鬼👻👻👻~'),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '2314698196':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 不知道呢~,但是阿离很讨厌你呢~'),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '3357290752':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是身体虚弱的空虚公子,你是爱欺负新人的无厘头群主,你是群友们的傲娇小妾,你是群中任劳任怨的牛马,就是你辣~'),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/444e0b288b0ba29f8748d00cde8edec4.jpg"),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/e21fd4b3be3963db29021bcbbaf54db3.jpg"),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/5cd68a5677c25b6b021259eb2b2c098b.jpg"),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/d9830ab56b7a504744d0eea805fea48f.jpg"),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/fb2362ec24d269fcbfe93dbae1032a21.jpg"),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '1721270769':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是玩不起就红温的格林!!! 哼~'),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/2F35BF22FA49BACE9A486DA3574872D1.gif"),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '1758657468':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是狼狈的杂鱼GoSp!!! '),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/F9F0F808F723844C0AFD34A5C2672A2E.jpg"),
            ]
        )
        await who_am_i.finish(message)
    elif qq == '1740167165':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是拟掉了，沉了，冒不了泡的大病猫~ '),
                MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/E85440CDF53B776913F4CB3BA06522B9.png"),
            ]
        )
        await who_am_i.finish(message)
    else:
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' emmmmm, 阿离不认识你呢~'),
            ]
        )
        await who_am_i.finish(message)


# 回复消息
reply = on_command('回复', rule=rule)


@reply.handle()
async def handle_reply(bot: Bot, event: Event):
    # 获取回复消息的 ID
    # 检查是否有回复消息 ID
    if event.message_id:
        # 使用 Message 对象的 reply 方法引用原始消息并回复
        # 这里的 message 参数是用户发送的原始消息，可以是 Message 对象或者消息 ID
        # 由于示例中没有具体的 Message 对象，这里使用 event.message 作为示例
        message = Message(
            [
                MessageSegment.reply(event.message_id),
                MessageSegment.text(f'回复消息 ID 是：{event.message_id}')
            ]
        )  # 将事件消息转换为 Message 对象
        await reply.finish(message)
    else:
        await reply.finish('没有找到回复消息 ID。')


# 撤回消息
withdraw = on_command('撤回', rule=rule)


@withdraw.handle()
async def handle_withdraw(bot: Bot, event: Event):
    # 获取引用消息 ID
    reply_id = event.reply.message_id
    print(reply_id)
    # 撤回消息
    await bot.call_api('delete_msg', message_id=reply_id)
    await withdraw.finish()


# 合并转发
merge_forwarding = on_command('合并转发', rule=rule)


@merge_forwarding.handle()
async def handle_merge_forwarding(bot: Bot, event: Event):
    event_dict = {"message_id": '103025680'}
    dict_ = await bot.call_api("get_msg", **event_dict)
    print(f"{dict_}")
    # forward_event_dict = {"message_id": '120236236'}
    # dict_ = await bot.call_api("get_forward_msg", **forward_event_dict)
    # print(f"合并转发内容：{dict_}")
    # # 检查raw_message是否包含'forward'
    # if 'forward' in dict_['raw_message']:
    #     # 提取message数组中的id
    #     for item in dict_['message']:
    #         if 'data' in item and 'id' in item['data']:
    #             forward_id = item['data']['id']
    #             forward_event_dict = {"message_id": forward_id}
    #             dict_ = await bot.call_api("get_forward_msg", **forward_event_dict)
    #             print(f"合并转发内容：{dict_}")


# 群成员加入
def group_increase_notice_event_rule(event: Event):
    return isinstance(event, GroupIncreaseNoticeEvent)


join = on_notice(rule=group_increase_notice_event_rule)


@join.handle()
async def group_increase_handle(bot: Bot, event: GroupIncreaseNoticeEvent):
    member = await bot.get_stranger_info(user_id=int(event.user_id))
    message = Message(
        [
            MessageSegment.at(event.user_id),
            MessageSegment.text(f' 欢迎 {member["nickname"]}({event.user_id}) 加入我们的大家庭!'),
            MessageSegment.image(f"https://q1.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=640"),
        ]
    )
    await join.finish(message)


# 群成员退群
def group_decrease_notice_event_rule(event: Event):
    return isinstance(event, GroupDecreaseNoticeEvent)


leave = on_notice(rule=group_decrease_notice_event_rule)


@leave.handle()
async def group_decrease_handle(bot: Bot, event: GroupDecreaseNoticeEvent):
    member = await bot.get_stranger_info(user_id=int(event.user_id))
    message = Message(
        [
            MessageSegment.at(event.user_id),
            MessageSegment.text(f' 很遗憾, {member["nickname"]}({event.user_id}) 离开了我们'),
        ]
    )
    await leave.finish(message)


# 定时任务
@scheduler.scheduled_job('interval', seconds=30 * 60)
async def my_hourly_task():
    console_adapter = nonebot.get_adapter(Adapter)
    bots = console_adapter.bots
    wink_list = ["Ciallo～(∠・ω< )⌒★!", "Ciallo～(∠・ω<)⌒⚡!", "Ciallo～(∠・ω<)⌒♥!", "Ciallo～(ゝ∀･)⌒☆!", "Ciallo～(∠・ω< )⌒♡!", "Ciallo～(∠・ω<)⌒✿!"]
    wink = random.choice(wink_list)
    await bots['2944307407'].send_group_msg(group_id=881971669, message=wink)
    await bots['2944307407'].send_group_msg(group_id=115082089, message=wink)
    await bots['2944307407'].send_group_msg(group_id=166891314, message=wink)
    await bots['2944307407'].send_group_msg(group_id=905607644, message=wink)
    await bots['2944307407'].send_group_msg(group_id=1006740933, message=wink)
    await bots['2944307407'].send_group_msg(group_id=927631582, message=wink)
    await bots['2944307407'].send_group_msg(group_id=606049581, message=wink)
    await bots['2944307407'].send_group_msg(group_id=962238411, message=wink)
    await bots['2944307407'].send_group_msg(group_id=660948621, message=wink)
    await bots['2944307407'].send_group_msg(group_id=1012614168, message=wink)
    await bots['2944307407'].send_group_msg(group_id=463707499, message=wink)
    await bots['2944307407'].send_group_msg(group_id=963870882, message=wink)
    await bots['2944307407'].send_group_msg(group_id=863511589, message=wink)
    await bots['2944307407'].send_group_msg(group_id=857433826, message=wink)
    await bots['2944307407'].send_group_msg(group_id=417192938, message=wink)
    await bots['2944307407'].send_group_msg(group_id=431553197, message=wink)


def get_time():
    # 获取当前时间
    now = datetime.now()

    # 获取年、月、日、时、分、秒
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    # 获取星期（0是星期一，6是星期日）
    weekday = now.weekday()

    # 星期的名称
    weekday_name = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    week = weekday_name[weekday]

    print(f"Year: {year}")
    print(f"Month: {month}")
    print(f"Day: {day}")
    print(f"Hour: {hour}")
    print(f"Minute: {minute}")
    print(f"Second: {second}")
    print(f"Week: {week}")
    return f"{year}年{month}月{day}日 {hour}时{minute}分{second}秒 {week}"


# 设置定时任务
# 格式说明：
# - `0` 分钟
# - `0` 小时
# - `*` 日
# - `*` 月
# - `?` 星期（不需要关心星期几，用 ? 表示不指定）
@scheduler.scheduled_job('cron', minute=0, hour='*')
async def hourly_job():
    console_adapter = nonebot.get_adapter(Adapter)
    bots = console_adapter.bots
    current_datetime = get_time()
    print(get_time())
    await bots['2944307407'].send_group_msg(group_id=881971669, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=115082089, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=166891314, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=905607644, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=1006740933, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=927631582, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=606049581, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=962238411, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=660948621, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=1012614168, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=463707499, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=963870882, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=863511589, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=857433826, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=417192938, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    await bots['2944307407'].send_group_msg(group_id=431553197, message=f"这是来自阿离的整点报时哦, 当前时间：{current_datetime}")
    print("每小时的第一秒执行任务")


# cscs181/QQ-GitHub-Bot

# nonebot_plugin_alconna
# nonebot_plugin_waiter
# 猜数字
guess_number = on_command('猜数字', rule=rule)
target_number = 0


@guess_number.handle()
async def handle_function(args: Message = CommandArg()):
    global target_number
    target_number = random.randint(1, 100)
    print(target_number)
    await guess_number.send(f"猜猜我想的是哪个数字呢（1-100）？")


@guess_number.got("number", prompt="请输入你猜想的数字嘛~")
async def got_location(number: str = ArgPlainText()):
    global target_number
    if number == "退出":
        await guess_number.finish("游戏已退出,下次再来玩哦~")
    # 判断是否是数字
    if not number.isdigit():
        await guess_number.reject(f"请输入数字哦~")
    if int(number) == target_number:
        await guess_number.finish(f"恭喜你猜对了！我想的数字就是 {target_number} 哦~")
    elif int(number) > target_number:
        await guess_number.reject(f"猜错了，比我猜想的数字大了哦~")
    elif int(number) < target_number:
        await guess_number.reject(f"猜错了，比我猜想的数字小了哦~")


# 掷骰子
roll_dice = on_command('掷骰子', rule=rule)


@roll_dice.handle()
async def handle_function(bot: Bot, event: Event):
    qq = event.user_id
    message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(f" 你掷出了 {random.randint(1, 6)} 点"),
        ]
    )
    await roll_dice.finish(message)


# 今日占卜
divine = on_command('今日占卜', rule=rule)


@divine.handle()
async def handle_function(bot: Bot, event: Event):
    qq = event.user_id
    divine_info = f"""
今日财富运：{random.randint(1, 100)}
今日事业运：{random.randint(1, 100)}
今日桃花运：{random.randint(1, 100)}
今日健康运：{random.randint(1, 100)}
今日学业运：{random.randint(1, 100)}
今日出行运：{random.randint(1, 100)}
今日爱情运：{random.randint(1, 100)}

注：本占卜结果仅供参考，不作为诊断依据，请谨慎使用(wink~)。
"""
    message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(divine_info),
        ]
    )
    await divine.finish(message)


# 降龙十八戳
eighteen_group_poke = on_command('降龙十八戳', rule=rule)


@eighteen_group_poke.handle()
async def handle_group_poke(event: Event, bot: Bot):
    qq = event.get_user_id()
    if qq in ["3218366812", "3357290752", "271702375", "3767215109"]:
        group = event.group_id
        # 判断@是否存在
        if event.get_message()["at"]:
            qq = event.get_message()["at"][0].data["qq"]
        try:
            for i in range(18):
                await bot.call_api("group_poke", group_id=group, user_id=qq)
        except Exception as e:
            print(e)
            poke_message = Message(
                [
                    MessageSegment.at(qq),
                    MessageSegment.text("呜呜呜,戳不到你啦.")
                ]
            )
            await eighteen_group_poke.finish(poke_message)
        await eighteen_group_poke.finish()
    else:
        menu_message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text("你坏，你没有权限使用这个命令!")
            ]
        )
        await eighteen_group_poke.finish(menu_message)


def check_poke_me(event: PokeNotifyEvent):
    return event.target_id == event.self_id


poke_me = on_notice(rule=check_poke_me)


@poke_me.handle()
async def handle_poke_me(event: PokeNotifyEvent, bot: Bot):
    qq = event.get_user_id()
    if qq in ['319203727', '3077334686', '3192299626', '2123537057']:
        await eighteen_group_poke.finish()
        return
    group = event.group_id
    try:
        await bot.call_api("group_poke", group_id=group, user_id=qq)
    except Exception as e:
        print(e)
        poke_message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text("呜呜呜,戳不到你啦.")
            ]
        )
        await eighteen_group_poke.send(poke_message)
    text_list = ["就你小子乱戳我，找打！！！", "说了不要戳了！", "要被戳坏了啦！", "你坏，不许戳我!", "你个坏耶，不准戳我!", "不要再拍啦,再拍就傻掉了啦!", "干什么!!!", "你违法了,你知道吗!!!", "不要摸阿离的头,会长不高的啦!!!", "就...就只有这一次哦"]
    text = random.choice(text_list)
    poke_message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(text)
        ]
    )
    await eighteen_group_poke.send(poke_message)
    if text.find('违法') != -1:
        await you_are_an_idiot.send("你")
        await you_are_an_idiot.send("违")
        await you_are_an_idiot.send("法")
        await you_are_an_idiot.send("了")
        await you_are_an_idiot.send("!!!")
        await bot.set_group_ban(group_id=group, user_id=int(qq), duration=random.randint(1, 24))
    await eighteen_group_poke.finish()


# 笨蛋
you_are_an_idiot = on_regex(pattern=r'笨蛋', rule=to_me())


@you_are_an_idiot.handle()
async def handle_function(bot: Bot, event: Event):
    qq = event.user_id
    await you_are_an_idiot.send("你")
    await you_are_an_idiot.send("才")
    await you_are_an_idiot.send("是")
    await you_are_an_idiot.send("笨")
    await you_are_an_idiot.send("蛋")
    message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(f" 你!才!!是!!!大!!!!笨!!!!!蛋!!!!!!"),
        ]
    )
    await you_are_an_idiot.finish(message)


# 六
six = on_command(cmd='6', aliases={'6', '六'}, rule=to_me())


@six.handle()
async def handle_function(bot: Bot, event: Event):
    qq = event.user_id
    message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.image(f"file:///work/Python/chat-qq-bot/plugins/chobits/881971669/image/8F0A185D456B1E64CB4D733E59587FA1.jpg"),
        ]
    )
    await six.finish(message)


# 柚子厨
ciallo = on_command(cmd='柚子厨', rule=rule)


@ciallo.handle()
async def handle_function(bot: Bot, event: Event):
    text = "什么千恋万花（慌乱）（把笔记本熄屏）（四处张望）我不玩千恋万花（慌乱地把笔记本藏到身后）（假装冷静）（试图走近解释）（摔倒）（狼狈爬起）（再次摔倒）（着急）（抓你们裤脚）（惊慌）我不玩千恋万花啊求求你们别鄙视我，求求你们不要不和我玩（慌乱）我……我真没玩过什么galgame（眼神四处乱瞟）（惊恐）（哭泣）（在地上打滚）（想起身后的笔记本）（丢掉笔记本）我…我笔记本是用来玩原神的，我真的不是柚子厨……（发疯）（跳走）（尖叫）你们不要问了啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊我真的很容易死的！！！（阴暗地逃跑）我真的不是柚子厨啊😭我才不会表演那个的😱就是那个………………………Ciallo～(∠・ω< )⌒☆"
    text = "什么千恋万花（慌乱）（把电脑熄屏）（四处张望）我不玩千恋万花（慌乱地清理电脑后台)（假装冷静）（试图走近解释）（摔倒）（狼狈爬起）（再次摔倒）（着急)（抓你们裤脚）（惊慌）我不玩千恋万花啊求求你们别鄙视我，求求你们不要不和我玩（慌乱）我…….我真的不玩千恋万花（眼神四处乱瞟）（惊恐）(哭泣）（在地上打滚）（想起身后的电脑)(丟掉电脑） 我…我电脑是用来玩原神的，我真的没有玩千恋万花….…（发疯）（发出尖锐的爆鸣声）"
    await ciallo.finish(text)


# 你是谁
who_is_it = on_command(cmd='你是谁', rule=rule)


@who_is_it.handle()
async def handle_function(bot: Bot, event: Event):
    await who_is_it.finish("我是阿离呀~")


# 阿离
a_li = on_command(cmd='阿离', rule=rule)


@a_li.handle()
async def handle_function(bot: Bot, event: Event):
    text_list = ["这儿呢~这儿呢~【跳起来】", "我在~", "到！", "来啦来啦~", "你要和阿离一起玩耍吗?"]
    text = random.choice(text_list)
    await a_li.finish(text)


# ciallo
ciallo = on_command(cmd='ciallo', aliases={'Ciallo', '千恋万花'}, rule=rule)


@ciallo.handle()
async def handle_function(bot: Bot, event: Event):
    wink_list = ["Ciallo～(∠・ω< )⌒★!", "Ciallo～(∠・ω<)⌒⚡!", "Ciallo～(∠・ω<)⌒♥!", "Ciallo～(ゝ∀･)⌒☆!", "Ciallo～(∠・ω< )⌒♡!", "Ciallo～(∠・ω<)⌒✿!"]
    wink = random.choice(wink_list)
    await ciallo.finish(wink)


# 疑问
amazed = on_command(cmd='啊?', aliases={'啊？', '诶？', '诶?', '?', '？'}, rule=rule)


@amazed.handle()
async def handle_function(bot: Bot, event: Event):
    qq = event.user_id
    message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text("在惊讶什么吗？告诉阿离叭(◍ ´꒳` ◍)~"),
        ]
    )
    await amazed.finish(message)


# 喵
mew = on_regex(pattern=r'喵', rule=rule)

mew_image_list = []

files = get_all_files('/work/Python/chat-qq-bot/plugins/chobits/miao')
for file in files:
    mew_image_list.append({'url': f'file:///work/Python/chat-qq-bot/plugins/chobits/miao/{file}'})


@mew.handle()
async def handle_function(bot: Bot, event: Event):
    image_info = random.choice(mew_image_list)
    message = Message(
        [
            MessageSegment.image(image_info['url'])
        ]
    )
    await mew.finish(message)


# 汪
wang = on_regex(pattern=r'汪', rule=rule)

wang_image_list = []

files = get_all_files('/work/Python/chat-qq-bot/plugins/chobits/wang')
for file in files:
    wang_image_list.append({'url': f'file:///work/Python/chat-qq-bot/plugins/chobits/wang/{file}'})


@wang.handle()
async def handle_function(bot: Bot, event: Event):
    image_info = random.choice(wang_image_list)
    message = Message(
        [
            MessageSegment.image(image_info['url'])
        ]
    )
    await wang.finish(message)


# 催图
urge_for_pictures = on_command(cmd='催图', aliases={'ct'}, rule=rule)


@urge_for_pictures.handle()
async def handle_function(bot: Bot, event: Event):
    message = Message(
        [
            MessageSegment.at(3267675260),
            MessageSegment.text("催图催图催图!!!"),
        ]
    )
    await urge_for_pictures.send(message)
    markdown = {
        "type": "forward",
        "data": {
            "id": "Kv4wYykAJ+JYf3vgTZsEFjbr4c04xUlXDtRPlH7L0Xb6z8PqlE/1rA0qaWlocU/8"
        }
    }
    await send_markdown(bot=bot, event=event, markdown=markdown)


# nonebot_plugin_multincm 音乐插件
# 唱歌
sing = on_command(cmd='唱歌', rule=rule)

sing_audio_list = []

files = get_all_files('/work/Python/chat-qq-bot/plugins/chobits/audio')
for file in files:
    sing_audio_list.append({'url': f'file:///work/Python/chat-qq-bot/plugins/chobits/audio/{file}'})


@sing.handle()
async def handle_function(bot: Bot, event: Event):
    audio_info = random.choice(sing_audio_list)
    print(audio_info['url'])
    await sing.finish(MessageSegment.record(audio_info['url']))


# 呼叫全体
call_everyone = on_command(cmd='呼叫全体', rule=rule)


@call_everyone.handle()
async def handle_function(bot: Bot, event: Event):
    qq = event.user_id
    if qq not in ['3218366812']:
        await call_everyone.finish(MessageSegment.at(0))
    else:
        message = Message(
            [
                MessageSegment.reply(event.message_id),
                MessageSegment.at(qq),
                MessageSegment.text("你没这个权限,你不准@全体成员!!!"),
            ]
        )
        await call_everyone.finish(message)


# code
code = on_command('code')


@code.handle()
async def handle_json(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("code_str", args)


@code.got("code_str", prompt="请输入 Python 代码")
async def got_markdown(event: Event, bot: Bot, code_str: str = ArgPlainText()):
    qq = event.get_user_id()
    # 获取字符串长度
    length = len(code_str)
    if qq not in ['3218366812', '2251797539']:
        await code.finish("你没有权限使用这个功能，请联系阿离的主人吧~")

    if length > 66:
        await code.finish("代码太长啦，请精简一下再试试吧~")
    print(code_str)
    # 创建一个 StringIO 对象来捕获输出
    output = io.StringIO()
    # 临时重定向标准输出
    sys.stdout = output
    # 执行代码
    exec(code_str)
    # 恢复标准输出
    sys.stdout = sys.__stdout__
    result_str = output.getvalue().strip()
    info_str = f"""
代码: 

{code_str}

输出: 

{result_str}

"""
    message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text(info_str)
        ]
    )
    await code.finish(message=message)


# 复读机
repeater = on_command('复读机')


@repeater.handle()
async def handle_json(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("repeater_str", args)


@repeater.got("repeater_str", prompt="请输入需要复读的消息")
async def got_markdown(event: Event, bot: Bot, repeater_str: str = ArgPlainText()):
    qq = event.get_user_id()
    message = Message(
        [
            MessageSegment.text(repeater_str),
        ]
    )
    if event.sub_type == 'normal':
        await repeater.finish(message)
    else:
        await repeater.finish(message)


# 设置头衔
group_special_title = on_command(cmd='设置头衔', aliases={'头衔'}, rule=rule)


@group_special_title.handle()
async def handle_group_ban(bot: Bot, event: Event):
    message = event.get_message()
    qq = message["at"][0].data["qq"]
    special_title = event.get_plaintext()
    print(qq)
    # 去除空字符串
    special_title = special_title.replace("设置", "")
    special_title = special_title.replace("头衔", "")
    special_title = special_title.replace(" ", "")
    print(special_title)
    if event.sub_type == 'normal':
        group = event.group_id
        await bot.call_api("set_group_special_title", group_id=group, user_id=qq, special_title=special_title)
        await group_special_title.finish("设置成功~")


# 回应消息
echo = on_command(cmd='回应消息', aliases={'回应'}, rule=rule)


@echo.handle()
async def handle_echo(bot: Bot, event: Event):
    # 获取回复消息的 ID
    # 检查是否有回复消息 ID
    if event.message_id:
        # await bot.call_api(api="set_msg_emoji_like", group_id=event.group_id, message_id=event.message_id, emoji_id='66')
        await bot.call_api(api="send_msg", message_type='group', group_id=event.group_id, message={
            "type": "image",
            "data": {
                "summary": "其实,我喜欢你很久了~",
                "type": "flash",
                "subType": 0,
                "file": "file:///work/Python/chat-qq-bot/plugins/chobits/image/F1142B28B89D8895F6B7464C490A1921.jpg"
            }
        })
        # await bot.call_api(api="set_group_reaction", group_id=event.group_id, message_id=event.message_id, code='9')
        # message = Message(
        #     [
        #         MessageSegment.image("file:///work/Python/chat-qq-bot/plugins/chobits/image/73E15FE56632C556C2FB8E9D99C2E1C3.jpg"),
        #     ]
        # )
        # await echo.send(message)
        # 使用 Message 对象的 echo 方法引用原始消息并回复
        # 这里的 message 参数是用户发送的原始消息，可以是 Message 对象或者消息 ID
        # 由于示例中没有具体的 Message 对象，这里使用 event.message 作为示例
        message = Message(
            [
                MessageSegment.reply(event.message_id),
                MessageSegment.text("回应完成~"),
            ]
        )
        # 将事件消息转换为 Message 对象
        await echo.finish(message)
    else:
        await echo.finish('没有找到回复消息 ID。')


# 图片地址
path = on_command('图片地址', rule=rule)


@path.got("path", prompt="请输入图片")
async def debug_got(event: GroupMessageEvent):
    url = event.get_message()
    for i in url:
        if i.type == "image":
            await path.finish(i.data["url"], reply_message=True)

        elif i.type == "mface":
            await path.finish(i.data["url"], reply_message=True)


# 撅
stick_up = on_regex(r'撅', rule=to_me())


@stick_up.handle()
async def handle_stick_up(bot: Bot, event: Event):
    message = Message(
        [
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.get_user_id()),
            MessageSegment.text("不可以!,变态!!"),
        ]
    )
    await stick_up.finish(message)


# test
test = on_command('test', rule=rule)


@test.handle()
async def handle_test(bot: Bot, event: Event):
    qq_text = """
551393530
2401128923
2944307407
"""
    qq_list = qq_text.split("\n")
    message_list = [MessageSegment.at(int(i)) for i in qq_list if i.isdigit()]
    message = Message(message_list)
    await test.finish(message)
    # qq = event.get_user_id()
    # name = await bot.get_group_member_info(group_id=event.group_id, user_id=int(qq))
    # # data = MessageSegment.node_custom(
    # #     user_id=int(qq), nickname=name["nickname"], content=Message(MessageSegment.text("测试回复"))
    # # )
    #
    # data = Message(
    #     [
    #         MessageSegment.node_custom(user_id=int(qq), nickname=name["nickname"], content=MessageSegment.text("测试回复")),
    #         MessageSegment.node_custom(user_id=int(qq), nickname=name["nickname"], content=MessageSegment.text("测试回复")),
    #         MessageSegment.node_custom(user_id=int(qq), nickname=name["nickname"], content=MessageSegment.text("测试回复")),
    #     ]
    # )
    # print(data)
    # res_id = await bot.call_api("send_forward_msg", messages=data)
    # await bot.send_group_msg(group_id=event.group_id, message=Message(MessageSegment.forward(res_id)))
    # await test.finish("测试成功")


# 自毁
self_destruct = on_command(cmd='自毁', rule=rule)


@self_destruct.handle()
async def handle_self_destruct(bot: Bot, event: Event):
    qq = event.get_user_id()
    group = event.group_id
    if qq == '3218366812':
        await self_destruct.send("正在自毁...")
        await self_destruct.send("再见了各位(呜呜呜)...")
        await self_destruct.send(MessageSegment.image("file:///work/Python/chat-qq-bot/plugins/chobits/image/982EAC0E63F48AA524AFEAAB4A0454FB.gif"))
        await bot.set_group_leave(group_id=event.group_id)
    else:
        await bot.set_group_ban(group_id=group, user_id=int(qq), duration=60)
        await self_destruct.finish("才不要自毁嘞,哼~")


# 自动同意邀请入群
def group_invite_rule(event: Event):
    flag = isinstance(event, GroupRequestEvent)
    print(flag)
    if flag and event.sub_type == 'invite':
        flag = True
        print(event.sub_type)
    return flag


invite_accept = on_request(rule=group_invite_rule)


@invite_accept.handle()
async def invite_accept_handle(bot: Bot, event: GroupRequestEvent):
    print("自动同意邀请入群")
    print(f"{event.user_id}邀请我入群,我已同意")
    message = Message(
        [
            MessageSegment.at(user_id=3218366812),
            MessageSegment.image(f"https://q1.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=640"),
            MessageSegment.text(f"{event.user_id} 邀请阿离入群 {event.group_id}"),
        ]
    )
    await bot.send_group_msg(group_id=1006740933, message=message)
    await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)


# 遥控自毁
telecontrol_self_destruct = on_command('遥控自毁', rule=rule)


@telecontrol_self_destruct.handle()
async def handle_json(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("group", args)


@telecontrol_self_destruct.got("group", prompt="请输入群号")
async def got_markdown(event: Event, bot: Bot, group: str = ArgPlainText()):
    qq = event.get_user_id()
    if qq == '3218366812':
        await telecontrol_self_destruct.send("正在遥控自毁中...")
        await bot.send_group_msg(group_id=int(group), message="正在遥控自毁中...")
        await bot.send_group_msg(group_id=int(group), message=MessageSegment.image("file:///work/Python/chat-qq-bot/plugins/chobits/image/982EAC0E63F48AA524AFEAAB4A0454FB.gif"))
        await bot.set_group_leave(group_id=int(group))
        await telecontrol_self_destruct.finish("遥控自毁成功~")
    else:
        await telecontrol_self_destruct.finish("才不要自毁嘞,哼~")


# 工作时间
work_time = on_command(cmd='工作时间', rule=rule)


@work_time.handle()
async def handle_function(bot: Bot, event: Event):
    message = Message(
        [
            MessageSegment.text("""
工作时间: 早八点半到晚六点半（周一至周六）
小声哔哔: 其实这是主人的工作时间
""")
        ]
    )
    await work_time.finish(message)


# keywords = {'三角洲', '威龙', '摸金'}
#
# e = on_keyword(keywords, priority=9, block=True)
#
#
# @e.handle()
# async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
#     msg = event.message
#     mid = event.message_id
#     uid = event.user_id
#     gid = event.group_id
#
#     # 检查事件发生的群组是否是您的目标群组之一
#     if gid in TARGET_GROUP_IDS1:
#         try:
#             await bot.set_group_ban(group_id=gid, user_id=uid, duration=300)
#             await asyncio.sleep(random.random())
#             await bot.delete_msg(message_id=mid)
#             await bot.send(event, MessageSegment.text("你怎么不说话了 是因为不喜欢吗？"), at_sender=True)
#             await asyncio.sleep(random.random())
#             await bot.send(event, MessageSegment.image(r"E:\jpg\禁言卡组\说话啊.jpg"))
#         except:
#             logger.warning("撤回失败，可能是bot权限不够导致")
#         else:
#             recently_banned[(gid, uid)] = time.time()

# 信息伪造
fake_info = on_command('群主牛逼660948621', rule=rule)


@fake_info.handle()
async def fake_info_handle(bot: Bot, event: Event):
    qq = event.get_user_id()
    name = await bot.get_group_member_info(group_id=event.group_id, user_id=int(qq))
    data = Message(
        [
            MessageSegment.node_custom(user_id=int(qq), nickname=name["nickname"], content=MessageSegment.text("群主牛逼")),
            MessageSegment.node_custom(user_id=int(qq), nickname=name["nickname"], content=MessageSegment.text("群主牛逼")),
            MessageSegment.node_custom(user_id=int(qq), nickname=name["nickname"], content=MessageSegment.text("群主牛逼")),
        ]
    )
    print(data)
    res_id = await bot.call_api("send_forward_msg", messages=data)
    await bot.send_group_msg(group_id=event.group_id, message=Message(MessageSegment.forward(res_id)))


async def hello(request: Request) -> Response:
    console_adapter = nonebot.get_adapter(Adapter)
    bots = console_adapter.bots
    message = """【服务通知】
您好，您于2024年10月7日22:17购买的“如果能够回到国庆前一天就好了”服务现已生效，感谢您对本公司的支持，期待下次能为您带来更好的服务。
Ciallo～(∠・ω< )⌒☆
"""
    await bots['2944307407'].send_group_msg(group_id=881971669, message=message)
    await bots['2944307407'].send_group_msg(group_id=115082089, message=message)
    await bots['2944307407'].send_group_msg(group_id=166891314, message=message)
    await bots['2944307407'].send_group_msg(group_id=905607644, message=message)
    await bots['2944307407'].send_group_msg(group_id=1006740933, message=message)
    await bots['2944307407'].send_group_msg(group_id=927631582, message=message)
    await bots['2944307407'].send_group_msg(group_id=606049581, message=message)
    await bots['2944307407'].send_group_msg(group_id=962238411, message=message)
    await bots['2944307407'].send_group_msg(group_id=660948621, message=message)
    await bots['2944307407'].send_group_msg(group_id=1012614168, message=message)
    await bots['2944307407'].send_group_msg(group_id=463707499, message=message)
    await bots['2944307407'].send_group_msg(group_id=963870882, message=message)
    await bots['2944307407'].send_group_msg(group_id=863511589, message=message)
    await bots['2944307407'].send_group_msg(group_id=857433826, message=message)
    await bots['2944307407'].send_group_msg(group_id=417192938, message=message)
    await bots['2944307407'].send_group_msg(group_id=431553197, message=message)
    print(request)
    return Response(200, content="Hello, world!")


if isinstance((driver := get_driver()), ASGIMixin):
    driver.setup_http_server(
        HTTPServerSetup(
            path=URL("/hello"),
            method="GET",
            name="hello",
            handle_func=hello,
        )
    )

# 火车
train = on_command(cmd='火车', rule=rule)


@train.handle()
async def handle_function(bot: Bot, event: Event):
    message = Message(
        [
            MessageSegment.face(id_=419),
            MessageSegment.text("/火车"),
        ]
    )
    await train.finish(message)


# 发布公告
publish_notice = on_command(cmd='发布公告', rule=rule)


@publish_notice.handle()
async def handle_publish_notice(bot: Bot, event: Event):
    content = event.get_plaintext()
    content = content.replace("发布公告", "")
    content = content.replace(" ", "")
    await bot.call_api("_send_group_notice", group_id=event.group_id, content=content)
