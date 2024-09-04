import base64
import json
import random
from time import sleep
import os
from typing import Dict

import nonebot
# 规则
from nonebot.rule import Rule, to_me
# 框架规则
from nonebot import on_command, require, on_notice
# 通讯协议
from nonebot.adapters.onebot.v11 import Event, Bot, Message, MessageSegment, Adapter, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent, PokeNotifyEvent
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

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler


# 好友白名单
async def is_qq_white_list(event: Event) -> bool:
    if event.get_user_id() in ['319203727', '3077334686', '3192299626']:
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
rule = Rule(is_qq_white_list, is_group_white_list)


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
1. 随机图片
2. 随机视频
3. 铁锈指令
4. 猜数字
5. 戳
6. 召唤喵天依~
7. 招魂
8. 今日占卜
9. 纸片人老婆征集(待定,我没鸽!)

注: 想要加的有趣功能可以和雪兔提哦~"""),
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
async def handle_test(event: Event, bot: Bot):
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
    if event.group_id == '115082089':
        image_list = obscene_image_list
    image_info = random.choice(image_list)
    url = image_info['url']
    await image.finish(MessageSegment.image(url))


# 戳
group_poke = on_command('戳', rule=rule)


@group_poke.handle()
async def handle_group_poke(event: Event, bot: Bot):
    group = event.group_id
    if event.get_message()["at"][0].data["qq"]:
        qq = event.get_message()["at"][0].data["qq"]
    else:
        qq = event.get_user_id()
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
        await menu.finish(poke_message)
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
        await menu.finish(data)
    else:
        await menu.finish(data)


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
user_ban = on_command('单人禁言', rule=ban_rule)


@user_ban.handle()
async def handle_group_ban(bot: Bot, event: Event):
    message = event.get_message()
    qq = message["at"][0].data["qq"]
    if event.sub_type == 'normal':
        group = event.group_id
        await bot.set_group_ban(group_id=group, user_id=int(qq), duration=10)
        await user_ban.finish("禁言成功~")


# 召唤喵天依~
mew = on_command('召唤喵天依~', rule=rule)


@mew.handle()
async def handle_mew():
    await mew.send(MessageSegment.image("/work/PHP/phpinfo/Image/Download/download.jpeg"))
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
.afk如果房主在30秒内不说话，则将房主权限给你
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
    await video.send(MessageSegment.video(url))
    await video.finish(MessageSegment.at(qq))


# 测试大图
video = on_command('测试大图', rule=rule)


@video.handle()
async def handle_video(event: Event, bot: Bot):
    qq = event.get_user_id()
    await video.send(MessageSegment.image("/mnt/e/Pictures/mobile/湊の乙女_torino_原寸.png"))
    # with open("/mnt/e/Pictures/mobile/湊の乙女_torino_原寸.png", "rb") as file:
    #     # 读取文件内容
    #     data = file.read()
    #     # 使用base64编码
    #     encoded_data = base64.b64encode(data)
    #     print(encoded_data)
    #     # 将编码后的数据转换为字符串
    #     encoded_str = encoded_data.decode('utf-8')
    #     await video.send(MessageSegment.image("base64://"+encoded_str))
    await video.finish(MessageSegment.at(qq))


# 勇敢的心
video = on_command('勇敢的心', rule=rule)


@video.handle()
async def handle_video(event: Event, bot: Bot):
    qq = event.get_user_id()
    # await video.send(MessageSegment.record("/mnt/e/Work/PHP/my/SnowRabbit/storage/app/public/music/ud7qo-txck6.wav"))
    await video.send(MessageSegment.record("https://webfs.hw.kugou.com/202404201515/9fd67d5b3a78dbfdc174ae2672643399/v2/b9a974e272f36cead2b2e693121fcd82/G366/M00/0C/28/TpUEAGVLZMCAKV05AEICsH8LxvM801.mp3"))
    await video.finish(MessageSegment.at(qq))


# 复读机
repeater = on_command('复读机', rule=rule)


@repeater.handle()
async def handle_repeater(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("repeater", args)


@repeater.got("repeater", prompt="请输入需要复读的消息")
async def got_repeater(event: Event, bot: Bot, message: str = ArgPlainText()):
    message = MessageSegment.text(message)
    await send_markdown(bot=bot, event=event, markdown=message)


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
    elif qq == '2185765317':
        message = Message(
            [
                MessageSegment.at(qq),
                MessageSegment.text(f' 你是'),
                MessageSegment.at(3218366812),
                MessageSegment.text(f' 的妹妹哦~'),
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
@scheduler.scheduled_job('interval', seconds=9 * 60)
async def my_hourly_task():
    console_adapter = nonebot.get_adapter(Adapter)
    bots = console_adapter.bots
    wink_list = ["Ciallo～(∠・ω< )⌒★!", "Ciallo～(∠・ω<)⌒⚡!", "Ciallo～(∠・ω<)⌒♥!", "Ciallo～(ゝ∀･)⌒☆!"]
    wink = random.choice(wink_list)
    await bots['2944307407'].send_group_msg(group_id=881971669, message=wink)
    await bots['2944307407'].send_group_msg(group_id=115082089, message=wink)
    await bots['2944307407'].send_group_msg(group_id=166891314, message=wink)


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
    print("每小时的第一秒执行任务")


guess_number = on_command('猜数字', rule=rule)
target_number = 0


@guess_number.handle()
async def handle_function(args: Message = CommandArg()):
    global target_number
    target_number = random.randint(1, 100)
    await guess_number.send(f"猜猜我想的是哪个数字呢（1-100）？")


@guess_number.got("number", prompt="请输入你猜想的数字嘛~")
async def got_location(number: str = ArgPlainText()):
    global target_number
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
    if qq == "3218366812" or qq == "3357290752" or qq == "1553712360" or qq == "271702375":
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
    poke_message = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text("你坏，不许戳我!")
        ]
    )
    await eighteen_group_poke.finish(poke_message)
