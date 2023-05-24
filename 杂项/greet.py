from nonebot import on_command, on_notice
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Message,MessageSegment, GroupMessageEvent, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent
from nonebot import on_notice

welcom = on_notice()

# # 群友入群
# @welcom.handle()  # 监听 welcom
# async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
#     userid = event.get_user_id()  # 获取新成员的id
#     msg = '博士，欢迎加入这盛大的庆典！我是来自米诺斯的祭司帕拉斯......要来一杯美酒么？'
#     msg = MessageSegment.at(userid) + Message(msg)
#     await welcom.finish(msg)  # 发送消息


# 群友退群
@welcom.handle()  # 监听 welcom
async def h_r(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):
    userid = event.get_user_id()  # 获取成员的id
    msg = f'选择了离开...'
    msg = MessageSegment.at(userid) + Message(msg)
    await welcom.finish(msg)  # 发送消息
