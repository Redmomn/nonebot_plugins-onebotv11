from nonebot import on_message,on_regex
from nonebot.adapters.onebot.v11 import Bot,Message,MessageEvent,permission,Event,GroupMessageEvent
from nonebot.permission import SUPERUSER
import random

# async def IsAdmin():
#     out = permission.GROUP_OWNER | permission.GROUP_ADMIN | SUPERUSER
#     return out

IsAdmin = permission.GROUP_OWNER | permission.GROUP_ADMIN | SUPERUSER

ban = on_regex('牛牛禁言(他|她|它)',permission=IsAdmin,priority=2,block=True)

@ban.handle()
async def _(event:GroupMessageEvent,bot:Bot):
    mid = event.message_id
    gid = event.group_id
    response = await bot.get_msg(message_id=mid)
    msg = response['message']
    count = 0
    for msg_section in msg:
        if msg_section['type'] == 'at':
            if msg_section['data']['qq'] == 'all':
                count = -100
                await ban.finish('不可以禁言全体成员哦')
            else:
                count += 1
                banner_id = int(msg_section['data']['qq'])
                await bot.set_group_ban(group_id=gid,user_id=banner_id,duration=random.randint(60*1,60*10))
    if count == 0:
        await ban.finish('你好像还没有指定要禁言谁哦')
    elif count >= 1:
        return
    
unban = on_regex('牛牛取消禁言',permission=IsAdmin,priority=2,block=True)

@unban.handle()
async def _(event:GroupMessageEvent,bot:Bot):
    mid = event.message_id
    gid = event.group_id
    response = await bot.get_msg(message_id=mid)
    msg = response['message']
    count = 0
    for msg_section in msg:
        if msg_section['type'] == 'at':
            if msg_section['data']['qq'] == 'all':
                count = -100
                await ban.finish('不可以取消禁言全体成员哦')
            else:
                count += 1
                banner_id = int(msg_section['data']['qq'])
                await bot.set_group_ban(group_id=gid,user_id=banner_id,duration=0)
    if count == 0:
        await ban.finish('你好像还没有指定要取消禁言谁哦')
    elif count >= 1:
        await unban.finish('已取消禁言')