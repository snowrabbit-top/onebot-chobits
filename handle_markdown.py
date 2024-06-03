from plugins.chobits import Button
from plugins.chobits import button_list
from plugins.chobits import Markdown

# 开发功能
develop = Button.Button.handle(button_list.develop)
# 普通功能
ordinary = Button.Button.handle(button_list.ordinary)


# 获取 markdown 文本
async def get_markdown_message(markdown, keyboard=None):
    # 默认 Markdown
    messages = Markdown.Markdown(markdown, keyboard).body
    return messages


# 获取发送 markdown 信息
async def get_send_markdown_message(bot, markdown, keyword=None):
    messages = await get_markdown_message(markdown, keyword)
    res_id = await bot.call_api("send_forward_msg", messages=messages)
    markdown = {
        "type": "longmsg",
        "data": {
            "id": res_id
        }
    }
    return markdown


# 功能
async def menu(bot):
    markdown = ""
    markdown += "[🔗@3218366812](mqqapi://card/show_pslcard?src_type=internal&version=1&uin=3218366812&crad_type=friend&source=qrcode)"
    markdown += "\r\n"
    markdown += "# **普通功能如下:** "
    markdown += "\r\n"
    keyword = ordinary
    # 构造发送 markdown 信息
    markdown = await get_send_markdown_message(bot, markdown, keyword)
    return markdown


# 功能
async def develop_menu(bot):
    markdown = ""
    markdown += "# **开发功能如下:** "
    markdown += "\r\n"
    keyword = develop
    # 构造发送 markdown 信息
    markdown = await get_send_markdown_message(bot, markdown, keyword)
    return markdown


# gpt
async def gpt(bot, gpt, message, qq, nickname):
    markdown = ""
    markdown += "# @" + nickname + "\n"
    markdown += f"![avatar #170px #170px](https://q1.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640)\n"
    markdown += "----\n"
    markdown += "``` \n"
    markdown += str(message) + "\n"
    markdown += "``` \n"
    markdown += "----\n"
    markdown += gpt + "\n\n"
    # 构造发送 markdown 信息
    markdown = await get_send_markdown_message(bot, markdown)
    return markdown


# 偷流量大户
async def glutton(bot, qq):
    markdown = ""
    for i in range(100):
        markdown += f"![text #1px #1x](https://api.likepoems.com/img/pc/?qq={qq}&random={i})"

    # 构造发送 markdown 信息
    markdown = await get_send_markdown_message(bot, markdown)
    return markdown
