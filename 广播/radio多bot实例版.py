from nonebot.rule import ArgumentParser
from nonebot import on_shell_command,on_fullmatch,on_command
import nonebot,re
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
send_msg_argument.add_argument('--bot',type=str,dest='bot_id',required=False,help='使用的bot id')

radio_msg_argument = ArgumentParser()
radio_msg_argument.add_argument('radio_msg',type=str)
radio_msg_argument.add_argument('--bot',type=str,dest='bot_id',required=False,help='使用的bot id')

get_ingroup_list_argument = ArgumentParser()
get_ingroup_list_argument.add_argument('--bot',type=str,dest='bot_id',required=False,help='使用的bot id')

sendmsg = on_shell_command('msg',parser=send_msg_argument,block=True,priority=1,permission=SUPERUSER)
radiomsg = on_shell_command('all',priority=1,parser=radio_msg_argument,block=True,permission=SUPERUSER)
get_ingroup_list = on_shell_command('get_group',parser=get_ingroup_list_argument,permission=SUPERUSER)
help = on_command('help',permission=SUPERUSER,block=False)
get_all_bot = on_shell_command('all_bot',permission=SUPERUSER,block=True)



# 发消息
@sendmsg.handle()
async def send_msg(bot:Bot,event:Event,state:T_State):
    args = cast(Namespace,state["_args"])
    if args.group_id == None:
        gid = event.group_id
    else:
        gid = args.group_id
    if args.bot_id == None:
        pass
    else:
        bot_id:str = args.bot_id
        bots = nonebot.get_bots()
        if bot_id in bots:
            bot = nonebot.get_bot(bot_id)
        else:
            await sendmsg.finish("此bot不存在")
    replacement = "[CQ:at,qq=\g<1>]"
    msg = re.sub(r"&#91;@(\d+)&#93;",replacement,args.msg)
    try:
        await bot.send_group_msg(group_id=gid,message=msg)
    except:
        await sendmsg.finish("发送失败：群聊不存在")

# 广播
@radiomsg.handle()
async def radio_msg(bot:Bot,event:Event,state:T_State):
    args = cast(Namespace,state["_args"])
    if args.bot_id == None:
        pass
    else:
        bot_id:str = args.bot_id
        bots = nonebot.get_bots()
        if bot_id in bots:
            bot = nonebot.get_bot(bot_id)
        else:
            await sendmsg.finish("此bot不存在")
    msg = "以下为广播内容：\n" + args.radio_msg
    group_info_list = await bot.get_group_list()
    group_list = []
    for group_info in group_info_list:
        group_list.append(group_info['group_id'])
    for group_id in group_list:
        titi = len(group_list)
        fatal_list = []
        try:
            await bot.send_group_msg(group_id=group_id,message=msg)
        except:
            titi -= 1
            fatal_list.append(group_id)
    logger.info(f'已向{len(group_list)}个群发送广播，广播内容：{args.radio_msg}，广播群列表：\n{group_list}')
    if fatal_list == []:
        await radiomsg.finish(f'发送成功，已广播{titi}个群')
    else:
        await radiomsg.finish(f'已广播{titi}个群，发送失败群列表：\n{str(fatal_list)}')
    
@get_ingroup_list.handle()
async def get_addgroup_info(bot:Bot,event:Event,state:T_State):
    args = cast(Namespace,state["_args"])
    if args.bot_id == None:
        pass
    else:
        bot_id:str = args.bot_id
        bots = nonebot.get_bots()
        if bot_id in bots:
            bot = nonebot.get_bot(bot_id)
        else:
            await sendmsg.finish("此bot不存在")
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

# 获取所有bot实例
@get_all_bot.handle()
async def _(bot:Bot,event:Event):
    bots = nonebot.get_bots()
    msg = '以下是正在运行的bot实例'
    for key in bots:
        bot_type = bots[key].type
        self_id = bots[key].self_id
        msg += f"""
        bot id: {self_id}
        协议：{bot_type}"""
    await get_all_bot.finish(msg)

@help.handle()
async def hhelp(bot:Bot,event:Event):
    msg = """使用帮助：
需使用命令起始符
    all_bot：获取所有正在运行的bot id
    msg：向群内发送消息
        可选参数：
        --g 指定要发送的群号
        --bot 指定使用发送的bot实例
    all：向所有群发送群广播
        --bot 指定使用发送的bot实例
    get_group：获取所有已加入群信息
        --bot 指定使用发送的bot实例"""
    await help.finish(msg)