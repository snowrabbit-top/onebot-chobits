import json
import uuid
from plugins.chobits.white_list_qq import white_list_qq

"""
render_data
按钮渲染
"""


class ButtonRender:
    """按钮文本"""
    label: str
    """被点击时的文本"""
    visited_label: str
    """
    按钮样式
    0 灰色线框
    1 蓝色线框
    """
    style: int

    """初始化"""

    def __init__(
            self,
            label: str = '按钮',
            visited_label: str = '按钮',
            style: int = 1
    ):
        self.label = label
        self.visited_label = visited_label
        self.style = style


"""
permission
按钮权限
"""


class ButtonPermission:
    """
    操作权限
    0 指定用户可操作
    1 仅管理者可操作
    2 所有人可操作
    3 指定身份组可操作（仅频道可用）
    """
    type: int
    """有权限的用户 id 的列表"""
    specify_role_ids: [str]
    """有权限的身份组 id 的列表（仅频道可用）"""
    specify_user_ids: [str]

    """初始化"""

    def __init__(
            self,
            type: int = 2,
            specify_role_ids: [str] = None,
            specify_user_ids: [str] = None
    ):
        self.type = type
        self.specify_role_ids = specify_role_ids
        self.specify_user_ids = specify_user_ids
        self.type = 0
        self.specify_user_ids = white_list_qq


"""
action
按钮动作
"""


class ButtonAction:
    """
    按钮动作
    设置 0 跳转按钮：http 或 小程序 客户端识别 scheme
        [/回车指令](mqqapi://aio/inlinecmd?command={urlencode(/回车指令)}&reply=false&enter=true)
        [/参数指令](mqqapi://aio/inlinecmd?command={urlencode(/参数指令（带引用）)&reply=true&enter=false)
        [@雪兔1](mqqapi://im/chat?chat_type=wpa&uin=3218366812&version=1&src_type=web&web_src=qq.com)
        [@雪兔2](mqq://im/chat?chat_type=wpa&version=1&src_type=web&uin=3218366812)
        [打开相机](mqqapi://videostory/takevideo?src_type=internal&version=1&from=mainCamera&uin=&appid=406&widgetid=&shareto=1)
    设置 1 回调按钮：回调后台接口, data 传给后台
    设置 2 指令按钮：自动在输入框插入 @bot data
    """
    type: str
    """权限"""
    permission: dict
    """按钮数据"""
    data: str
    """回复消息"""
    reply: bool
    """是否进入会话"""
    enter: bool
    """锚点"""
    anchor: int
    """点击次数限制"""
    click_limit: int
    """是否显示 @机器人"""
    at_bot_show_channel_list: bool
    """不支持时的提示"""
    unsupport_tips: str

    """初始化"""

    def __init__(
            self,
            type: str = '2',
            permission: ButtonPermission = ButtonPermission(),
            data: str = '按钮数据',
            reply: bool = False,
            enter: bool = False,
            anchor: int = 0,
            unsupport_tips: str = '您当前客户端不支持该功能',
            click_limit: int = None,
            at_bot_show_channel_list: bool = False
    ):
        self.type = type
        self.permission = permission.__dict__
        self.data = data
        self.reply = reply
        self.enter = enter
        self.anchor = anchor
        self.click_limit = click_limit
        self.at_bot_show_channel_list = at_bot_show_channel_list
        self.unsupport_tips = unsupport_tips


"""按钮"""


class Button:
    """按钮 id"""
    id: str
    """渲染数据"""
    render_data: dict
    """按钮动作"""
    action: dict

    """初始化"""

    def __init__(
            self,
            id: str = str(uuid.uuid1()),
            render_data: ButtonRender = ButtonRender(),
            action: ButtonAction = ButtonAction()
    ):
        self.id = id
        self.render_data = render_data.__dict__
        self.action = action.__dict__

    """
    按钮行
    数组组装变成按钮行
    """

    @staticmethod
    def row(
            buttons: []
    ) -> dict:
        button_row: dict = {
            'buttons': []
        }
        if len(buttons) >= 5:
            buttons = buttons[:5]
        for button in buttons:
            button_row['buttons'].append(button)
        return button_row

    """按钮组"""

    @staticmethod
    def group(group: []) -> []:
        if len(group) >= 5:
            group = group[:5]
        return group

    """处理按钮组"""

    @staticmethod
    def handle(config):
        button_group = []
        for row in config:
            button_row = {'buttons': []}
            for button in row:
                button_row['buttons'].append(
                    Button(
                        render_data=ButtonRender(
                            label=button['name'],
                            visited_label=button['visited_label'],
                        ),
                        action=ButtonAction(
                            type=button['type'],
                            permission=ButtonPermission(),
                            data=button['data'],
                            enter=button['enter'],
                        )
                    ).__dict__
                )
            button_group.append(button_row)
        return button_group


"""封装JSON序列化对象"""


class ButtonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Button):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
