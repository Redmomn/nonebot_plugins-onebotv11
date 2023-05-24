from nonebot.rule import ArgumentParser
from nonebot import on_shell_command,on_fullmatch
from argparse import Namespace
from nonebot.adapters.onebot.v11 import Bot,GroupMessageEvent,PrivateMessageEvent,Event
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from typing import cast
from nonebot import logger
logger.add("logs",level='WARNING',rotation="1 week")

send_msg_argument = ArgumentParser()

send_msg_argument.add_argument('msg',type=str,help='要发送的消息')
send_msg_argument.add_argument('--g',type=int,dest='group_id',required=False,help='发送的群号')

sendmsg = on_shell_command('msg',parser=send_msg_argument,block=True,priority=1,permission=SUPERUSER)

radio_msg_argument = ArgumentParser()
radio_msg_argument.add_argument('radio_msg',type=str)
radiomsg = on_shell_command('all',priority=1,parser=radio_msg_argument,block=True,permission=SUPERUSER)

get_ingroup_list = on_fullmatch('获取加群信息',permission=SUPERUSER,priority=1,block=True)

@sendmsg.handle()
async def send_msg(bot:Bot,event:Event,state:T_State):
    args = cast(Namespace,state["_args"])
    if args.group_id == None:
        gid = event.group_id
    else:
        gid = args.group_id
    await bot.send_group_msg(group_id=gid,message=args.msg)
    
@radiomsg.handle()
async def radio_msg(bot:Bot,event:Event,state:T_State):
    args = cast(Namespace,state["_args"])
    msg = "以下为广播内容：\n" + args.radio_msg
    group_info_list = await bot.get_group_list()
    group_list = []
    for group_info in group_info_list:
        group_list.append(group_info['group_id'])
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id,message=msg)
    logger.warning(f'已向{len(group_list)}个群发送广播，广播内容：{args.radio_msg}，广播群列表：\n{group_list}')
    await radiomsg.finish(f'发送成功，已广播{len(group_list)}个群')
    
@get_ingroup_list.handle()
async def get_addgroup_info(bot:Bot,event:Event):
    group_info_list = await bot.get_group_list()
    msg = '以下是加入的群的信息'
    for group_info in group_info_list:
        msg += f"""
        {group_info['group_name']}
            群号：{group_info['group_id']}
            群等级：{group_info['group_level']}
            群成员数：{group_info['member_count']}
            群最大成员数：{group_info['max_member_count']}
        """
    await get_ingroup_list.finish(message=msg)
