# 适配器
import json

from nonebot.adapters import Event, Message
# 规则
from nonebot.rule import Rule, to_me
# 框架规则
from nonebot import on_command
# 通讯协议
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
# QQ白名单
from .white_list_qq import white_list_qq
# 群白名单
from .white_list_group import white_list_group
# 处理 Markdown
from .handle_markdown import menu as handle_markdown_menu, get_send_markdown_message
# httpx
import httpx
# 事件响应器
from nonebot.matcher import Matcher
# 参数
from nonebot.params import CommandArg, ArgPlainText
# 聊天机器人
from .chat import chat

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

# 点赞
like = on_command('点赞', rule=rule)

@like.handle()
async def handle_test(event: Event, bot: Bot):
    qq = event.get_user_id()
    for i in range(20):
        await bot.send_like(user_id=int(qq), times=1)
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
    print(json)
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

# 对话
dialogue = on_command('对话', rule=rule)

@dialogue.handle()
async def handle_dialogue(bot: Bot, event: Event):
    qq = event.get_user_id()
    message = event.get_message()
    string = str(message).replace('对话 ', '')
    markdown = await chat(bot=bot, message=string, qq=qq)
    await send_markdown(bot, event, markdown)

# 召唤喵天依~
mew = on_command('召唤喵天依~', rule=rule)

@mew.handle()
async def handle_mew():
    await mew.send(MessageSegment.image("https://gchat.qpic.cn/gchatpic_new/3218366812/894446744-3002314434-911255CF765722233E60FF1FAFDD593C/0"))
    await mew.send("喵天依应召而来~")
    await mew.finish()

# 获取信息
info = on_command('获取信息', rule=rule)

@info.handle()
async def handle_info(bot: Bot, event: Event):
    qq = event.get_user_id()
    # member = await bot.get_stranger_info(user_id=int(qq))
    member = await bot.get_group_member_info(group_id=event.group_id, user_id=int(qq))
    print(member)
    data = Message(
        [
            MessageSegment.image(f"https://q1.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640"),
            MessageSegment.at(qq),
        ]
    )
    await info.finish(data)
