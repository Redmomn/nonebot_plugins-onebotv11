from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot,GroupMessageEvent

special_t=on_command('头衔',priority=1)

@special_t.handle()
async def _(bot:Bot,event:GroupMessageEvent):
    uid = event.get_user_id()
    gid = event.group_id
    msg = event.get_plaintext().strip('.头衔').strip()
    try:
        await bot.set_group_special_title(group_id=gid,user_id=uid,special_title=msg,duration=-1)
    except Exception:
        await special_t.finish('修改失败')
    else:
        await special_t.finish('修改成功')