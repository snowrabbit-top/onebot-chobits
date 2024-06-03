# weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)
# @weather.handle()
# async def handle_function():
#     await weather.finish("还行吧~")

# message = on_keyword(["雪兔"])
#
# @message.handle()
# async def handle_function():
#     msg = requests.get('https://api.52vmy.cn/api/wl/yan/du?type=text')
#     print(msg.text)
#     await message.finish(msg.text)


# if qq in communicate:
#     url = "http://127.0.0.1:8000/chat/completions"
#     data = {"messages": [{"role": "user", "content": str(message)}]}
#     headers = {"Content-Type": "application/json"}
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     msg = response.json()['choices'][0]['message']['content']
#     print(msg)
#     await dialogue.finish(msg)
#
# print(msg)
# await dialogue.finish(msg)
# if qq == '1873372030':
#     await dialogue.finish(message)
#     # 土味情话
#     # msg = requests.get('https://api.1314.cool/words/api.php')
#     # if msg.status_code == 200:
#     #     pattern = re.compile(r'<[^>]+>', re.S)
#     #     result = pattern.sub("\r\n", msg.text)
#     #     await dialogue.finish(result)
# if qq == '1851991319':
#     # 土味情话
#     msg = requests.get('https://api.1314.cool/words/api.php')
#     if msg.status_code == 200:
#         pattern = re.compile(r'<[^>]+>', re.S)
#         result = pattern.sub("\r\n", msg.text)
#         await dialogue.finish(result)
# if qq == '1876673920':
#     # 土味情话
#     msg = requests.get('https://api.1314.cool/words/api.php')
#     if msg.status_code == 200:
#         pattern = re.compile(r'<[^>]+>', re.S)
#         result = pattern.sub("\r\n", msg.text)
#         await dialogue.finish(result)


# dialogue = on_regex(".*", rule=to_me())
#
# @dialogue.handle()
# async def handle_dialogue(event: Event, bot: Bot):
#     qq = event.get_user_id()
#     print(qq)
#     message = event.get_message()
#     print(message)
#     session_id = event.get_session_id()
#     print(session_id)
#
#     # # 毒鸡汤
#     msg = requests.get('http://api.wer.plus/api/djt')
#     # 名人名言
#     # msg = requests.get('https://api.52vmy.cn/api/wl/yan/yiyan')
#     if msg.status_code == 200:
#         print(msg.json()['data']['comment'])
#         await chat(dialogue, bot, message, qq, session_id)


# image_data = Message(
#     [
#         MessageSegment.image("https://img.xjh.me/random_img.php?return=302&ranmod=" + str(random.random())),
#         MessageSegment.image("https://img.xjh.me/random_img.php?return=302&ranmod=" + str(random.random())),
#         MessageSegment.image("https://img.xjh.me/random_img.php?return=302&ranmod=" + str(random.random())),
#     ]
# )
# await image.finish(image_data)
# await image.send(MessageSegment.image("https://img.xjh.me/random_img.php?return=302&ranmod=" + str(random.random())))
# await image.send(MessageSegment.image("https://img.xjh.me/random_img.php?return=302&ranmod=" + str(random.random())))
# await image.send(MessageSegment.image("https://img.xjh.me/random_img.php?return=302&ranmod=" + str(random.random())))

# test_resid = on_command("测试resid")
#
# @test_resid.handle()
# async def handle_function(matcher: Matcher, args: Message = CommandArg()):
#     if args.extract_plain_text():
#         matcher.set_arg("resid", args)
#
# @test_resid.got("resid", prompt="请输入地名")
# async def got_resid(resid: str = ArgPlainText()):
#     await test_resid.finish(f"今天{resid}的天气是...")
# import re
# from playwright.sync_api import Page, expect

# from openai import OpenAI
#
# client = OpenAI(
#     # 输入转发API Key
#     api_key="sk-Xc2o4IyBnmqiJhPNPHJTbKVttx2bxW7cvRG6qfmH2WWZ4FMC",
#     base_url="https://api.chatanywhere.com.cn/v1"
# )
#
# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo-16k-0613",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "你是谁!"}
#     ],
#     logprobs=True,
#     stream=False  # 是否开启流式输出
# )
# def ChatCompletionMessage(content='我是一个可爱的助手，可以回答你的问题并提供帮助。有什么我可以帮助你的吗？', role='assistant', function_call=None, tool_calls=None):
#     print(content)

# completion.choices[0].message
# 非流式输出获取结果
# print(completion.choices[0].message)
# print(completion.choices[0].message)
# 流式输出获取结果
# for chunk in completion:
#     print(chunk.choices[0].delta)


# from nonebot import on_message
# from nonebot.adapters.onebot.v11 import GroupMessageEvent
# from nonebot.log import logger
#
# test = on_message()
#
#
# @test.handle()
# async def _(event: GroupMessageEvent):
#     msg = event.get_message()["image"]
#     if not msg:
#         await test.finish()
#
#     for m in msg:
#         url = m.data["url"]
#         logger.warning(url)
#         await test.send(url)

# from urllib.parse import urlparse, parse_qs, urlencode
#
#
# def read_url_params(url):
#     parsed_url = urlparse(url)
#     query_params = parse_qs(parsed_url.query)
#     return query_params
#
# prefix = 'https://multimedia.nt.qq.com.cn/download?'
#
# url = 'https://gchat.qpic.cn/gchatpic_new/0/0-0-BF0A3B0DF2ABB8E35B8FA003BA8D66E4/0?term=255&is_origin=1'
# url = 'https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=CgozMjk2MTMyNjUxEhRTAZKAkFjjKHEUOtB4d6UO1j_ZChjDrzAg_woo6rSb3fnAhQNQgL2jAQ&rkey=CAQSMAHI95K-N4ecKZXkdJIepah0nADybfxMf1hcXhFjeAW7HlwYH6PwaRKTMAW7sSiL1w&spec=0'
#
# params = read_url_params(url)
#
# info = {}
# print(params)
# for key, value in params.items():
#     print(key, value[0])
#     info[key] = value[0]
#
# # 假设我们有一个字典，我们想要将它转换为URL参数
# params_dict = {
#     'param1': 'value1',
#     'param2': 'value2',
#     'param3': ['list', 'of', 'values']
# }
#
# # 使用urlencode函数将字典转换为URL编码的查询字符串
# url_params = urlencode(info)
#
# # 输出URL参数
# print(url_params)
# if prefix+url_params == url:
#     print('ok')

import hashlib
#
# def calculate_md5(file_path):
#     # 创建一个md5对象
#     md5 = hashlib.md5()
#
#     # 打开文件，读取并更新md5对象
#     with open(file_path, 'rb') as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             md5.update(chunk)
#
#     # 返回十六进制的md5哈希值
#     return md5.hexdigest()
#
# # 使用函数计算文件的md5
# file_path = '/home/chobits/Pictures/0.jpeg'  # 替换为您的文件路径
# md5_hash = calculate_md5(file_path)
# print(f"The MD5 hash of the file is: {md5_hash.upper()}")
import re
import random
#
# html_tag = '[CQ:image,file=ee0b5513a74ff433738d9143554fc0cd.image,subType=0,url=https://gchat.qpic.cn/gchatpic_new/1/0-0-EE0B5513A74FF433738D9143554FC0CD/0?term=2]'
# # 使用正则表达式匹配URL
# match = re.search(r'url=(https?://[^\s]+)]', html_tag)
#
# if match:
#     url = match.group(1)
#     print(f"提取的URL是: {url}")
# else:
#     print("没有找到URL。")
#
# url = "https://gchat.qpic.cn/gchatpic_new/1/0-0-EE0B5513A74FF433738D9143554FC0CD/0?term=2"
#
# # 找到起始和结束位置的索引
# start_index = url.find("/0-0-") + len("/0-0-")  # len函数获取"/0-0-"的长度
# end_index = url.find("/0?")
# # 截取字符串
# extracted_string = url[start_index:end_index] if end_index != -1 else url[start_index:]
#
# print(f"截取的字符串是: {extracted_string}")

# # 假设这是你的列表
# my_list = ['apple', 'banana', 'cherry', 'date', 'fig']
#
# # 随机选择一个元素
# random_item = random.choice(my_list)
# # 删除原列表中的随机选中元素
# my_list.remove(random_item)
#
# print(f"随机选中的元素是: {random_item}")
# print("更新后的列表是:", my_list)
# -*- coding: UTF-8 -*-
import sys
import re