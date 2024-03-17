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

from openai import OpenAI

client = OpenAI(
    # 输入转发API Key
    api_key="sk-Xc2o4IyBnmqiJhPNPHJTbKVttx2bxW7cvRG6qfmH2WWZ4FMC",
    base_url="https://api.chatanywhere.com.cn/v1"
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-16k-0613",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁!"}
    ],
    logprobs=True,
    stream=False  # 是否开启流式输出
)
def ChatCompletionMessage(content='我是一个可爱的助手，可以回答你的问题并提供帮助。有什么我可以帮助你的吗？', role='assistant', function_call=None, tool_calls=None):
    print(content)

# completion.choices[0].message
# 非流式输出获取结果
print(completion.choices[0].message)
# print(completion.choices[0].message)
# 流式输出获取结果
# for chunk in completion:
#     print(chunk.choices[0].delta)
