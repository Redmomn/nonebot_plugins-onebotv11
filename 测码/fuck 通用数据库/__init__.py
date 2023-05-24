from nonebot import logger,on_regex,on_message,on_fullmatch,on_startswith
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot,GroupMessageEvent,Message,MessageSegment
import sqlite3
import os,pathlib
import random


#响应器
#测别人的码
fuck_other = on_startswith('测你码')

#rg = on_message(priority=1)
#索要码
get_fuck = on_fullmatch('测码')

#查数据
get_info = on_fullmatch('我的码')

#ac插件
from nonebot import require
require('nonebot_plugin_access_control')
from nonebot_plugin_access_control.service import create_plugin_service
ex_service = create_plugin_service('nonebot_plugin_fuck')

get_fuck_subservice = ex_service.create_subservice('get_fuck')
get_fuck_subservice.patch_matcher(get_fuck)

fuck_other_subservice = ex_service.create_subservice('fuck_other')
fuck_other_subservice.patch_matcher(fuck_other)

get_info_subservice = ex_service.create_subservice('get_info')
get_info_subservice.patch_matcher(get_info)



#测码获取禁言码的概率
fuck_get_fuckcard_probability = 0.24
#获取反制码
fuck_get_countercard_probability = 0.12
#测别人码成功的概率，仅限对面没反制码
fuck_to_other_probability = 1
#被反制的概率
be_countered_probability = 0.7
#偷管理员码
steal_admin_card_probability = 0.1


if os.path.exists('./data/fuck/db'):
    if os.path.isfile('./data/fuck/db/card_information.db'):
        pass
    else:
        try:
            logger.info('数据库不存在，即将创建数据库')
            file = open(file='./data/fuck/db/card_information.db',mode='w')
            file.close()
            logger.info('数据库创建成功')
        except Exception:
            logger.warning('数据库创建失败，请检查文件夹读写权限')
            raise Exception

else:
    logger.debug('数据库路径不存在，即将创建数据库目录')
    try:
        os.makedirs('./data/fuck/db')
    except Exception:
        logger.warning('数据库目录创建失败，请检查文件夹读写权限')
        raise Exception
    if os.path.isfile('./data/fuck/db/card_information.db'):
        pass
    else:
        try:
            logger.info('数据库不存在，即将创建数据库')
            file = open(file='./data/fuck/db/card_information.db',mode='w')
            file.close()
            logger.info('数据库创建成功')
        except Exception:
            logger.warning('数据库创建失败，请检查文件夹读写权限')
            raise Exception


client = sqlite3.connect('./data/fuck/db/card_information.db')
database = client.cursor()

class fffffuckkkkk(object):
    def __init__(self,group_id:int,user_id:int,to_user_id:int = None) -> None:
        self.group_id = group_id
        self.user_id = user_id
        self.to_user_id = to_user_id
        pass
    
    #好像没用
    async def database_exist(self) -> bool :
        response = database.execute(f'''
                        SELECT count(*) 
                        FROM sqlite_master 
                        WHERE type='table' 
                        AND name = 'general_database';
                        ''')
        if response[0] == 1: #存在表则返回1
            return True
        else:
            return False

    #创建表
    async def create_tables(self):
        database.execute(f'''
                        CREATE TABLE general_database(QID INT PRIMARY KEY NOT NULL,
                        禁言码 INT NOT NULL,
                        反制码 INT NOT NULL,
                        测别人码次数 INT NOT NULL,
                        被禁言次数 INT NOT NULL,
                        反制别人次数 INT NOT NULL,
                        被反制次数 INT NOT NULL);
                        ''')

    #查询数据
    async def select_data(self,qid:int) -> dict :
        try:
            #查找用户的所有数据
            response = database.execute(f'''
                                        SELECT * FROM general_database WHERE QID={qid};
                                        ''')
        except sqlite3.OperationalError:                    #表不存在
            await self.create_tables()
            response = database.execute(f'''
                                        SELECT * FROM general_database WHERE QID={qid};
                                        ''')
        data = response.fetchall()
        #数据为空，用户不存在此表中
        if data == []:
            await self.insert_database(qid=qid)
            response = database.execute(f'''
                                        SELECT * FROM general_database WHERE QID={qid};
                                        ''')
            data = response.fetchall()
            data_a = data[0]
            re = {}
            re['QID'] = data_a[0]
            re['FUCK_CARD'] = data_a[1]
            re['COUNTER_CARD'] = data_a[2]
            re['FUCK'] = data_a[3]
            re['BE_FUCKED'] = data_a[4]
            re['COUNTER'] = data_a[5]
            re['BE_COUNTERED'] = data_a[6]
            return re
        else:
            data_a = data[0]
            re = {}
            re['QID'] = int(data_a[0])
            re['FUCK_CARD'] = int(data_a[1])
            re['COUNTER_CARD'] = int(data_a[2])
            re['FUCK'] = int(data_a[3])
            re['BE_FUCKED'] = int(data_a[4])
            re['COUNTER'] = int(data_a[5])
            re['BE_COUNTERED'] = int(data_a[6])
            return re
            
    #表里不存在的用户，插入数据，全部置零
    async def insert_database(self,qid:int):
        '''
        数据库插入数据
        参数:
            qid(int):QQ
        '''
        database.execute(f'''
                        INSERT INTO general_database VALUES ({qid},0,0,0,0,0,0);
                        ''')
        #提交更改
        client.commit()

    async def update_database(self,qid:int,key:str,value:int|str):
        database.execute(f'''
                        UPDATE general_database 
                        SET {key}={value} 
                        WHERE QID={qid};
                        ''')
        client.commit()
        
    async def update_yyyy(self,qid:int,data:dict):
        await self.update_database(qid=qid,key='禁言码',value=data['FUCK_CARD'])
        await self.update_database(qid=qid,key='反制码',value=data['COUNTER_CARD'])
        
    #测码！
    async def fuckk(self) -> int|str:
        '''
        直接开测，无需传参
        返回值
            0:给一张禁言码
            1:给一张反制码
            寄:就是寄了
        '''
        user_data = await self.select_data(qid=self.user_id)
        fuckpppp = random.randint(0,1)
        if get_ture_or_false(fuckpppp):
            if fuckpppp == 0:
                #给一张禁言码
                user_data['FUCK_CARD'] += 1
            else:
                #给一张反制码
                user_data['COUNTER_CARD'] += 1
            await self.update_yyyy(qid=self.user_id,data=user_data)
            return fuckpppp
        else:
            #寄
            return '寄'
                
    
    #一键测别人的码
    async def cenima(self,is_admin:bool = False) -> int|dict:
        '''
        传入被测人是否管理员，返回测码结果
            非管理员事件:
                0:测码失败，原因：没码
                1:测码成功
                2:被反制
                3:测码失败,没测到
            管理员事件:
                0:测码失败，原因：没码
                其他情况: 返回dict
                {'stat':1~4, #4是偷管理员的码
                'steal_card':FUCK_CARD or COUNTER_CARD,
                'quantity':0~5
                }
        '''
        user_data = await self.select_data(qid=self.user_id)
        to_user_data = await self.select_data(qid=self.to_user_id)
        if user_data['FUCK_CARD'] == 0:
            return 0
        else:
            #被测人是否管理员
            if not is_admin:
                #不是管理员
                #是否测码
                if get_ture_or_false(2):
                    #开始测码！！！
                    #禁言码数量减一
                    user_data['FUCK_CARD'] -= 1
                    #是否有反制码
                    if to_user_data['COUNTER_CARD'] != 0:
                        #有反制码
                        #是否反制
                        if get_ture_or_false(3):
                            #被反制
                            #被测码者反制码减一
                            to_user_data['COUNTER_CARD'] -= 1
                            stat = 2
                        else:
                            #反制失败
                            #测码成功
                            stat = 1
                    else:
                        #没有反制码
                        #测码成功
                        stat = 1
                else:
                    #不测码
                    stat = 3
                await self.update_yyyy(qid=self.user_id,data=user_data)
                await self.update_yyyy(qid=self.to_user_id,data=to_user_data)
                return stat
            elif is_admin:
                #是管理员
                return_data = {
                    'stat':0,
                    'steal_card':0,
                    'quantity':0
                }
                #是否测码
                if get_ture_or_false(2):
                    #开始测码！！！
                    #禁言码数量减一
                    user_data['FUCK_CARD'] -= 1
                    #是否有反制码
                    if to_user_data['COUNTER_CARD'] != 0:
                        #有反制码
                        #是否反制
                        if get_ture_or_false(3):
                            #被反制
                            #被测码者反制码减一
                            to_user_data['COUNTER_CARD'] -= 1
                            return_data['stat'] = 2
                        else:
                            #反制失败
                            #测码成功
                            #是否偷管理员的码
                            if get_ture_or_false(4):
                                #偷码！！！
                                return_data['stat'] = 4
                                if (random.randint(0,1)) == 0:
                                    #偷禁言码
                                    num = random.randint(1,5)
                                    to_user_data['FUCK_CARD'] -= num
                                    if to_user_data['FUCK_CARD'] < 0:
                                        num = to_user_data['FUCK_CARD'] + num
                                        to_user_data['FUCK_CARD'] = 0
                                    return_data['steal_card'] = 'FUCK_CARD'
                                    return_data['quantity'] = num
                                else:
                                    #偷反制码
                                    num = random.randint(1,5)
                                    to_user_data['COUNTER_CARD'] -= num
                                    if to_user_data['COUNTER_CARD'] < 0 :
                                        num = to_user_data['COUNTER_CARD'] + num
                                        to_user_data['COUNTER_CARD'] = 0
                                    return_data['steal_card'] = 'COUNTER_CARD'
                                    return_data['quantity'] = num
                            else:
                                #偷不到，算了
                                #直接开测！
                                return_data['stat'] = 1
                    else:
                        #没有反制码
                        #测码成功
                        #是否偷管理员的码
                        if get_ture_or_false(md=4):
                            #偷码！！！
                            return_data['stat'] = 4
                            if (random.randint(0,1)) == 0:
                                #偷禁言码
                                num = random.randint(1,5)
                                to_user_data['FUCK_CARD'] -= num
                                if to_user_data['FUCK_CARD'] < 0:
                                    num = to_user_data['FUCK_CARD'] + num
                                    to_user_data['FUCK_CARD'] = 0
                                return_data['steal_card'] = 'FUCK_CARD'
                                return_data['quantity'] = num
                            else:
                                #偷反制码
                                num = random.randint(1,5)
                                to_user_data['COUNTER_CARD'] -= num
                                if to_user_data['COUNTER_CARD'] < 0 :
                                    num = to_user_data['COUNTER_CARD'] + num
                                    to_user_data['COUNTER_CARD'] = 0
                                return_data['steal_card'] = 'COUNTER_CARD'
                                return_data['quantity'] = num
                        else:
                            #偷不到，算了
                            #直接开测！
                            return_data['stat'] = 1
                else:
                    #不测码
                    return_data['stat'] = 3
                await self.update_yyyy(qid=self.user_id,data=user_data)
                await self.update_yyyy(qid=self.to_user_id,data=to_user_data)
                return return_data
            else:
                return '寄'



async def get_at(event: GroupMessageEvent) -> str:
    """获取at的qq号, 不存在则返回寄, 类型为str"""
    msg = event.get_message()
    for msg_seg in msg:
        if msg_seg.type == "at":
            if msg_seg.data["qq"] == "all":
                return "寄"
            return str(msg_seg.data["qq"])
    return "寄"

def get_ture_or_false(md:int) -> bool:
    '''
    md:各种测码 0是获取禁言码 1是获取反制码 2是测别人码 3是反制 4是偷管理员的码
    '''
    if (md == 0) or (md == 1):
        return (fuck_get_fuckcard_probability + fuck_get_countercard_probability >= random.random())
    # elif md == 1:
    #     return (fuck_get_countercard_probability >= random.random())
    elif md == 2:
        return (fuck_to_other_probability >= random.random())
    elif md == 3:
        return (be_countered_probability >= random.random())
    elif md == 4:
        return (steal_admin_card_probability >= random.random())




@get_info.handle()
async def gettt(event:GroupMessageEvent,bot:Bot):
    gid = event.group_id
    qid = event.user_id
    fuck_ep = fffffuckkkkk(group_id=gid,user_id=qid)
    data = await fuck_ep.select_data(qid=qid)
    fuck_card = data['FUCK_CARD']
    counter_card = data['COUNTER_CARD']
    if (fuck_card == 0) and (counter_card == 0):
        msg = MessageSegment.at(user_id=qid)+'\n你没码'
    else:
        msg = MessageSegment.at(user_id=qid)+f'\n禁言码：{fuck_card}\n反制码：{counter_card}'
    await get_info.finish(message=msg)

@get_fuck.handle()
async def _(event:GroupMessageEvent,bot:Bot):
    qid = event.user_id
    gid = event.group_id
    #实例化，传参
    fuck_ep = fffffuckkkkk(group_id=gid,user_id=qid)
    member_info = await bot.get_group_member_info(group_id=gid,user_id=qid,no_cache=True)
    #普通成员
    if member_info['role'] == 'member':
        response = await fuck_ep.fuckk()
        if response == '寄':
            try:
                await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
            except Exception:
                await get_fuck.finish("权限不足，无法禁言")
            img_filepath = os.path.abspath(path=f'./data/fuck/img/{random.randint(2,4)}.jpg').replace('\\','\\\\')
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+MessageSegment.image(file=f'file:///{img_filepath}',cache=False)))
        elif response == 0:
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'恭喜你获得一张禁言码，你可以去测别人的码了'))
        elif response == 1:
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'恭喜你获得一张反制码'))
    #管理员
    elif member_info['role'] == 'admin':
        response = await fuck_ep.fuckk()
        if response == '寄':
            try:
                await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
            except Exception:
                await get_fuck.finish("权限不足，无法禁言")
            img_filepath = os.path.abspath(path=f'./data/fuck/img/{random.randint(2,4)}.jpg').replace('\\','\\\\')
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+MessageSegment.image(file=f'file:///{img_filepath}',cache=False)))
        elif response == 0:
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'恭喜你获得一张禁言码，你可以去测别人的码了'))
        elif response == 1:
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'恭喜你获得一张反制码'))
    #群主
    elif member_info['role'] == 'owner':
        response = await fuck_ep.fuckk()
        if response == '寄':
            try:
                await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
            except Exception:
                await get_fuck.finish("权限不足，无法禁言")
            img_filepath = os.path.abspath(path=f'./data/fuck/img/{random.randint(2,4)}.jpg').replace('\\','\\\\')
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+MessageSegment.image(file=f'file:///{img_filepath}',cache=False)))
        elif response == 0:
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'恭喜你获得一张禁言码，你可以去测别人的码了'))
        elif response == 1:
            await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'恭喜你获得一张反制码'))

@fuck_other.handle()
async def fuck_to_other(event:GroupMessageEvent,bot:Bot):
    qid = event.user_id
    gid = event.group_id
    if event.to_me:
        img_filepath = os.path.abspath(path='./data/fuck/img/100.jpg').replace('\\','\\\\')
        try:
                await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
        except Exception:
            await fuck_other.finish("权限不足，无法禁言")
        await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+MessageSegment.image(file=f'file:///{img_filepath}',cache=False)))
        return 0
    to_qid = await get_at(event)
    if to_qid == '寄':
        await bot.send_group_msg(group_id=gid,message='小笨蛋，会不会用机器人')
    else:
        member_info = await bot.get_group_member_info(group_id=gid,user_id=qid,no_cache=True)
        fuck_ep = fffffuckkkkk(group_id=gid,user_id=qid,to_user_id=to_qid)
        #被测的是普通成员
        if member_info['role'] == 'member':
            response = await fuck_ep.cenima(is_admin=False)
            if response == 0:
                #没码，不能测码
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'测码失败，你没码'))
            elif response == 1:
                #测到了
                try:
                    await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
                except Exception:
                    await fuck_other.finish("权限不足，无法禁言")
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=to_qid)+'你被'+MessageSegment.at(user_id=qid)+'测了'))
            elif response == 2:
                #被反制了
                try:
                    await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
                except Exception:
                    await fuck_other.finish("权限不足，无法禁言")
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'对方反制了你的码'))
            elif response == 3:
                #没测到
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'你太短了测不到'))
        #群主和管理员
        else:
            response = await fuck_ep.cenima(is_admin=True)
            if response == 0:
                #没码，不能测码
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'测码失败，你没码'))
            elif response['stat'] == 1:
                #测到了
                try:
                    await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
                except Exception:
                    await fuck_other.finish("权限不足，无法禁言")
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=to_qid)+'你被'+MessageSegment.at(user_id=qid)+'测了'))
            elif response['stat'] == 2:
                #被反制了
                try:
                    await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
                except Exception:
                    await fuck_other.finish("权限不足，无法禁言")
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'对方反制了你的码'))
            elif response['stat'] == 3:
                #没测到
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=qid)+'你太短了测不到'))
            elif response['stat'] == 4:
                #测成功了，还偷走了码
                if response['steal_card'] == 'FUCK_CARD':
                    card = '禁言码'
                elif response['steal_card'] == 'COUNTER_CARD':
                    card = '反制码'
                quantity = response['quantity']
                try:
                    await bot.set_group_ban(group_id=gid,user_id=qid,duration=random.randint(5*60,15*60))
                except Exception:
                    await fuck_other.finish("权限不足，无法禁言")
                await bot.send_group_msg(group_id=gid,message=(MessageSegment.at(user_id=to_qid)+'你不仅被'+MessageSegment.at(user_id=qid)+f'测了，还被偷走了{quantity}张{card}'))