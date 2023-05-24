from nonebot import on_keyword,on_fullmatch,on_regex
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent,Event,Bot

#规则函数，仅限群聊使用
def _checker(event:GroupMessageEvent):
    return event.message_type=='group'
'''
使用新的屏蔽插件
'''
# #屏蔽机器人指令
# ban_cmd_set = {'标识码','来自服务器','qd=','zc=','cx=','cj=','dt=','sd=','get=','gm=','list=','qx=','gz=','cz=','lb=','qz=','help=','cjlb=','ch=','sz=','jq=','ty=','bty=','start=','close=','ban=','kick=','fwq=','zw=','set=','admin=','remove=','sys=','ql=','dt=','hmd=','bmd=','jt=','yd=','yc=','gx='}
# BFV_command = on_keyword(ban_cmd_set,priority=2,block=True)

# @BFV_command.handle()
# async def _():
#     return

#群号对应的机器人查询前缀 例如 2cx=xxx
cmd_dict = {743375820:'2',284274759:'6'}
#屏蔽自助查询
pbhelp = on_keyword({'被踢','踢我','屏蔽我','被屏蔽','把我踢了','被禁'},rule=_checker,block=True,priority=2)

@pbhelp.handle()
async def _(event:GroupMessageEvent,bot:Bot):
    userid = event.user_id
    groupid = event.group_id
    userdata = await bot.get_group_member_info(user_id=userid,group_id=groupid)
    try:
        nickname = userdata['card']
    except Exception:
        nickname = userdata['nickname']
    msg = f'pb={nickname}'
    try :
        if groupid in cmd_dict.keys():
            msg = f'{cmd_dict[groupid]}pb={nickname}'
    except Exception:
        pass
    await pbhelp.finish(Message(msg))
   
#牛牛查询
pallascx = on_regex('牛牛查询(成就|状态)',block=True,priority=2)

@pallascx.handle()
async def _(event:GroupMessageEvent,bot:Bot):
    userid = event.user_id
    groupid = event.group_id
    userdata = await bot.get_group_member_info(user_id=userid,group_id=groupid,no_cache=True)
    try:
        nickname = userdata['card']
    except Exception:
        nickname = userdata['nickname']
    msg = f'cx={nickname}'
    try :
        if groupid in cmd_dict.keys():
            msg = f'{cmd_dict[groupid]}cx={nickname}'
    except Exception:
        pass
    await pbhelp.finish(Message(msg))
    
#辅助举报
jubaohelp = on_keyword({'举报规范'},rule=_checker,block=False,priority=2)

@jubaohelp.handle()
async def _():
    await jubaohelp.finish(Message('举报违规需要提供相关证据，请填写服务器序号(几服)、ID、状况描述、并上传证据后艾特管理'))
