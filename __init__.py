import base64
import json
import random
from time import sleep

# 适配器
from nonebot.adapters import Event, Message
# 规则
from nonebot.rule import Rule, to_me
# 框架规则
from nonebot import on_command
# 通讯协议
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
# QQ白名单
from awesome_bot.plugins.chobits.white_list_qq import white_list_qq
# 群白名单
from awesome_bot.plugins.chobits.white_list_group import white_list_group
# 处理 Markdown
from awesome_bot.plugins.chobits.handle_markdown import menu as handle_markdown_menu, get_send_markdown_message, develop_menu as handle_markdown_develop_menu
# httpx
import httpx
# 事件响应器
from nonebot.matcher import Matcher
# 参数
from nonebot.params import CommandArg, ArgPlainText
# 聊天机器人
from awesome_bot.plugins.chobits.chat import chat

# 好友白名单
async def is_qq_white_list(event: Event) -> bool:
    return event.get_user_id() in white_list_qq

# 群白名单
async def is_group_white_list(event: Event) -> bool:
    if event.sub_type == 'normal':
        return str(event.group_id) in white_list_group
    else:
        return True

# 规则权限
rule = Rule(is_qq_white_list, is_group_white_list)

# 发送 Markdown
async def send_markdown(bot, event, markdown):
    qq = event.get_user_id()
    if event.sub_type == 'normal':
        await bot.send_group_msg(group_id=event.group_id, message=markdown)
        await menu.finish(MessageSegment.at(qq))
    else:
        await bot.send_private_msg(user_id=int(qq), message=markdown)
        await menu.finish()

# 菜单
menu = on_command('菜单', rule=rule)

@menu.handle()
async def handle_menu(bot: Bot, event: Event):
    markdown = await handle_markdown_menu(bot=bot)
    await send_markdown(bot=bot, event=event, markdown=markdown)

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

# 随机图片
image = on_command('随机图片', rule=rule)

@image.handle()
async def handle_image(event: Event):
    message = event.get_message()
    string = str(message).replace('随机图片', '')
    # 字符串去掉 图片 这两个字
    length = int(string) if string != '' else 0
    if length < 1:
        length = 0
    elif length >= 3:
        length = 2
    else:
        length -= 1
    # 图片
    for i in range(length):
        await image.send(MessageSegment.image("https://img.xjh.me/random_img.php?return=302"))
    await image.finish(MessageSegment.image("https://img.xjh.me/random_img.php?return=302"))

# 毒鸡汤
poisonous = on_command('毒鸡汤', rule=rule)

@poisonous.handle()
async def handle_poisonous():
    # 创建一个异步client
    async with httpx.AsyncClient() as client:
        message = await client.get('https://api.wer.plus/api/djt', timeout=None)
        if message.status_code == 200:
            await image.finish(message.json()['data']['comment'])

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
            MessageSegment.json('{"app":"com.tencent.imagetextbot","config":{"autosize":1,"ctime":1710228958,"token":"9b4a4df03888800526c55924d51024b1"},"meta":{"robot":{"cover":"https:\/\/api.mrgnb.cn\/api\/tz.php?url=https:\/\/api.likepoems.com\/img\/pc\/","jump_url":"","subtitle":"","title":""}},"prompt":"\u52a8\u753b\u8868\u60c5","ver":"1.0.0.14","view":"index"}'),
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
            MessageSegment.json('{"app":"com.tencent.imagetextbot","config":{"autosize":1,"ctime":1710231632,"token":"ea4fa7feefea09749a8b81c16b71789b"},"meta":{"robot":{"cover":"https:\/\/api.mrgnb.cn\/api\/tz.php?url=https:\/\/gchat.qpic.cn\/offpic_new\/3218366812\/\/3218366812-1260311223-6FA5EE584CFE32B0D7C2383FEB36A5B4\/0","jump_url":"","subtitle":"","title":""}},"prompt":"\u52a8\u753b\u8868\u60c5","ver":"1.0.0.14","view":"index"}'),
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
            MessageSegment.json('{"app":"com.tencent.imagetextbot","config":{"autosize":1,"ctime":1710677816,"token":"c29d7804384eb855dcc4269df748537f"},"meta":{"robot":{"cover":"https:\/\/api.mrgnb.cn\/api\/tz.php?url=https:\/\/api.kaitomoe.org\/lgrbanner.php","jump_url":"","subtitle":"","title":""}},"prompt":"[Lagrange.Core]","ver":"1.0.0.14","view":"index"}'),
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
group_ban = on_command('全群禁言', rule=rule)

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
user_ban = on_command('单人禁言', rule=rule)

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
    await mew.send(MessageSegment.image("https://gchat.qpic.cn/gchatpic_new/3218366812/894446744-3002314434-911255CF765722233E60FF1FAFDD593C/0"))
    await mew.send("喵天依应召而来~")
    await mew.finish()

# 随机视频
video = on_command('随机视频', rule=rule)

@video.handle()
async def handle_video(event: Event, bot: Bot):
    qq = event.get_user_id()
    await video.send(MessageSegment.video("https://www.yujn.cn/api/heisis.php"))
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
    await video.send(MessageSegment.record("https://s17.aconvert.com/convert/p3r68-cdx67/ud7qo-txck6.wav"))
    await video.finish(MessageSegment.at(qq))

# 嘤嘤嘤
yingyingying = on_command('嘤嘤嘤', rule=rule)

@yingyingying.handle()
async def handle_yingyingying(event: Event):
    qq = event.get_user_id()
    data = Message(
        [
            MessageSegment.at(qq),
            MessageSegment.text("我一拳一个嘤嘤怪~"),
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
            MessageSegment.text("我一拳一个呜呜怪~"),
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
