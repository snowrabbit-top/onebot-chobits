import json

# 获取 markdown 文本
async def get_markdown_message(markdown, keyboard=None):
    # 默认 Markdown
    messages = [
        {
            "type": "node",
            "data": {
                "name": "匿名用户",
                "uin": "10000000",
                "content": [
                    {
                        "type": "markdown",
                        "data": {
                            "content": json.dumps(
                                {
                                    "content": markdown
                                }
                            )
                        }
                    }
                ]
            }
        }
    ]
    # 判断是否有 keyboard
    if keyboard:
        # 添加 按钮
        messages[0]["data"]["content"].append(
            {
                "type": "keyboard",
                "data": {
                    "content": {
                        "rows": keyboard
                    }
                }
            }
        )
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
    markdown += "# **功能如下:** "
    markdown += "\r\n"
    index = 0
    keyword = [
        {
            "buttons": [
                {
                    'id': str(++index),
                    'render_data': {
                        'label': '点赞',
                        'visited_label': '点赞',
                        'style': 0
                    },
                    'action': {
                        'type': 2,
                        'permission': {
                            'type': 2,
                            'specify_role_ids': None,
                            'specify_user_ids': None
                        },
                        'data': '点赞',
                        'reply': None,
                        'enter': True,
                        'anchor': None,
                        'unsupport_tips': '您的客户端不支持此操作',
                        'click_limit': None,
                        'at_bot_show_channel_list': False
                    }
                }
            ]
        },
        {
            "buttons": [
                {
                    'id': str(++index),
                    'render_data': {
                        'label': '随机图片',
                        'visited_label': '随机图片',
                        'style': 0
                    },
                    'action': {
                        'type': 2,
                        'permission': {
                            'type': 2,
                            'specify_role_ids': None,
                            'specify_user_ids': None
                        },
                        'data': '随机图片',
                        'reply': None,
                        'enter': True,
                        'anchor': None,
                        'unsupport_tips': '您的客户端不支持此操作',
                        'click_limit': None,
                        'at_bot_show_channel_list': False
                    }
                },
                {
                    'id': str(++index),
                    'render_data': {
                        'label': '毒鸡汤',
                        'visited_label': '毒鸡汤',
                        'style': 0
                    },
                    'action': {
                        'type': 2,
                        'permission': {
                            'type': 2,
                            'specify_role_ids': None,
                            'specify_user_ids': None
                        },
                        'data': '毒鸡汤',
                        'reply': None,
                        'enter': True,
                        'anchor': None,
                        'unsupport_tips': '您的客户端不支持此操作',
                        'click_limit': None,
                        'at_bot_show_channel_list': False
                    }
                }
            ]
        },
        {
            "buttons": [
                {
                    'id': str(++index),
                    'render_data': {
                        'label': '测试resid',
                        'visited_label': '测试resid',
                        'style': 0
                    },
                    'action': {
                        'type': 2,
                        'permission': {
                            'type': 2,
                            'specify_role_ids': None,
                            'specify_user_ids': None
                        },
                        'data': '测试resid',
                        'reply': None,
                        'enter': True,
                        'anchor': None,
                        'unsupport_tips': '您的客户端不支持此操作',
                        'click_limit': None,
                        'at_bot_show_channel_list': False
                    }
                },
                {
                    'id': str(++index),
                    'render_data': {
                        'label': '测试Markdown',
                        'visited_label': '测试Markdown',
                        'style': 0
                    },
                    'action': {
                        'type': 2,
                        'permission': {
                            'type': 2,
                            'specify_role_ids': None,
                            'specify_user_ids': None
                        },
                        'data': '测试Markdown',
                        'reply': None,
                        'enter': True,
                        'anchor': None,
                        'unsupport_tips': '您的客户端不支持此操作',
                        'click_limit': None,
                        'at_bot_show_channel_list': False
                    }
                }
            ]
        },
        {
            "buttons": [
                {
                    'id': str(++index),
                    'render_data': {
                        'label': '测试JSON',
                        'visited_label': '测试JSON',
                        'style': 0
                    },
                    'action': {
                        'type': 2,
                        'permission': {
                            'type': 2,
                            'specify_role_ids': None,
                            'specify_user_ids': None
                        },
                        'data': '测试JSON',
                        'reply': None,
                        'enter': True,
                        'anchor': None,
                        'unsupport_tips': '您的客户端不支持此操作',
                        'click_limit': None,
                        'at_bot_show_channel_list': False
                    }
                }
            ]
        },
        {
            "buttons": [
                {
                    'id': str(++index),
                    'render_data': {
                        'label': '对话',
                        'visited_label': '对话',
                        'style': 0
                    },
                    'action': {
                        'type': 2,
                        'permission': {
                            'type': 2,
                            'specify_role_ids': None,
                            'specify_user_ids': None
                        },
                        'data': '对话 ',
                        'reply': None,
                        'enter': None,
                        'anchor': None,
                        'unsupport_tips': '您的客户端不支持此操作',
                        'click_limit': None,
                        'at_bot_show_channel_list': False
                    }
                }
            ]
        }
    ]
    # 构造发送 markdown 信息
    markdown = await get_send_markdown_message(bot, markdown, keyword)
    return markdown

# gpt
async def gpt(bot, gpt, message, qq):
    markdown = ""
    markdown += "# @" + qq + "\n"
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