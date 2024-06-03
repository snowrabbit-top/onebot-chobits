import json

"""Markdown"""


class Markdown:
    """Markdown 内容"""
    messages: str
    """keyboard 按钮组"""
    keyboard: []
    """信息体"""
    body: [dict]

    """初始化"""

    def __init__(
            self,
            messages: str = '',
            keyboard=None
    ):
        self.messages = messages
        self.keyboard = keyboard
        self.set_markdown()

    """
    设置 markdown 内容
    """

    def set_markdown(self):
        self.body = [
            {
                "type": "node",
                "data": {
                    "name": "匿名用户",
                    "uin": "10000000",
                    "content": [
                        {
                            "type": "at",
                            "data": {
                                "qq": '2944307407',
                                "name": '机器人@了阿离'
                            }
                        },
                        {
                            "type": "markdown",
                            "data": {
                                "content": json.dumps(
                                    {
                                        "content": self.messages
                                    }
                                )
                            }
                        }
                    ]
                }
            }
        ]
        """判断是否有 keyboard"""
        if self.keyboard:
            # 添加 按钮
            self.body[0]["data"]["content"].append(
                {
                    "type": "keyboard",
                    "data": {
                        "content": {
                            "rows": self.keyboard
                        }
                    }
                }
            )
