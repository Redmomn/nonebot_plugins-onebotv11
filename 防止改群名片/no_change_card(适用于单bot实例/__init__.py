import os,sqlite3,nonebot,asyncio
from nonebot import logger,get_bot,require,on_notice,on_command
from nonebot.adapters.onebot.v11 import Bot,GroupMessageEvent,GroupIncreaseNoticeEvent,GroupDecreaseNoticeEvent,permission,MessageSegment,Event
from nonebot.permission import SUPERUSER
require('nonebot_plugin_apscheduler')
from nonebot_plugin_apscheduler import scheduler




if os.path.exists('./data/group_nickname/db'):
    if os.path.isfile('./data/group_nickname/db/nickname.db'):
        pass
    else:
        try:
            logger.info('数据库不存在，即将创建数据库')
            file = open(file='./data/group_nickname/db/nickname.db',mode='w')
            file.close()
            logger.info('数据库创建成功')
        except Exception:
            logger.warning('数据库创建失败，请检查文件夹读写权限')
            raise Exception

else:
    logger.debug('数据库路径不存在，即将创建数据库目录')
    try:
        os.makedirs('./data/group_nickname/db')
    except Exception:
        logger.warning('数据库目录创建失败，请检查文件夹读写权限')
        raise Exception
    if os.path.isfile('./data/group_nickname/db/nickname.db'):
        pass
    else:
        try:
            logger.info('数据库不存在，即将创建数据库')
            file = open(file='./data/group_nickname/db/nickname.db',mode='w')
            file.close()
            logger.info('数据库创建成功')
        except Exception:
            logger.warning('数据库创建失败，请检查文件夹读写权限')
            raise Exception

client = sqlite3.connect('./data/group_nickname/db/nickname.db')
database = client.cursor()

def a1():
    response = database.execute("select * from sqlite_master where type='table' AND name='group_stat';")
    for i in response:
        return #表不存在直接跳过for
    database.execute("""CREATE TABLE group_stat (GID INT PRIMARY KEY NOT NULL,
                     STAT INT NOT NULL);
                     """)
a1() #stat初始化
class no(object):
    def __init__(self,group_id:int) -> None:
        self.group_id = group_id
        pass
    
    #好像没用
    async def database_exist(self) -> bool :
        response = database.execute(f'''
                        SELECT count(*) 
                        FROM sqlite_master 
                        WHERE type='table' 
                        AND name='group_{self.group_id}';
                        ''')
        for i in response:
            if i[0] == 1: #存在表则返回1
                return True
            else:
                return False
        # if response[0] == 1: #存在表则返回1
        #     return True
        # else:
        #     return False

    #创建表
    async def create_tables(self):
        database.execute(f'''
                        CREATE TABLE group_{self.group_id}(QID INT PRIMARY KEY NOT NULL,
                        群名片 TEXT NOT NULL,
                        更改群名片次数 INT NOT NULL,
                        身份 TEXT NOT NULL,
                        是否白名单 TEXT NOT NULL);
                        ''')

    #查询数据
    async def select_data(self,qid:int) -> dict :
        try:
            #查找用户的所有数据
            response = database.execute(f'''
                                        SELECT * FROM group_{self.group_id} WHERE QID={qid};
                                        ''')
        except sqlite3.OperationalError: #表不存在
            return False
        data = response.fetchall()
        #数据为空，用户不存在此表中
        if data == []:
            return 0
        else:
            data_a = data[0]
            re = {}
            re['QID'] = data_a[0]
            re['CARD'] = data_a[1]
            re['CHANGE_TIMES'] = data_a[2]
            re['ROLE'] = data_a[3]
            re['BMD'] = data_a[4]
            return re
            
    #表里不存在的用户，插入数据，全部置零
    async def insert_database(self,qid:int,card:str,role:str = 'member',is_bmd:bool = False):
        '''
        数据库插入数据
        参数:
            qid(int):QQ
        '''
        database.execute(f'''
                        INSERT INTO group_{self.group_id} VALUES ({qid},'{card}',0,'{role}','{is_bmd}');
                        ''')
        #提交更改
        client.commit()

    # 更新数据库
    async def update_database(self,qid:int,key,value):
        database.execute(f'''
                        UPDATE group_{self.group_id} 
                        SET {key}='{value}' 
                        WHERE QID={qid};
                        ''')
        client.commit()
    
    # 删除条目
    async def delete_data(self,qid:int):
        database.execute(
            f"""DELETE FROM group_{self.group_id} WHERE QID={qid}"""
        )
        client.commit()
    
    # 群开关状态表
    async def stat_table(self,increase:bool = True):
        if increase:
            database.execute(
                f"""INSERT INTO group_stat VALUES ({self.group_id},1)"""
            )
        else:
            database.execute(
                f"""DELETE FROM group_stat WHERE GID={self.group_id}"""
            )
        client.commit()
    
    # 查询群开关状态
    async def select_stat(self):
        response = database.execute(
            f"""SELECT stat FROM group_stat WHERE GID={self.group_id}"""
        )
        for i in response:
            if i[0] == 1: #存在数据则返回1
                return True
            else:
                return False
            
    # 删库
    async def drop(self):
        database.execute(
            f"""DROP TABLE group_{self.group_id}"""
        )

async def get_at(event: GroupMessageEvent) -> list:
    """获取at的qq号列表, 不存在则返回False, 类型为list 或 bool"""
    msg = event.get_message()
    at_list = []
    for msg_seg in msg:
        if msg_seg.type == "at":
            if msg_seg.data["qq"] == "all":
                return False
            else:
                at_list.append(int(msg_seg.data["qq"]))
    return at_list

is_admin = SUPERUSER | permission.GROUP_OWNER

init = on_command("初始化",block=True,permission=is_admin)
delete_func = on_command("关闭防改名",block=True,permission=is_admin)
increase_bmd = on_command("白名单",block=True,permission=is_admin)
decrease_bmd = on_command("取消白名单",block=True,permission=is_admin)
look_stat = on_command("stat",block=True,permission=SUPERUSER)
notice = on_notice()

# 功能初始化
@init.handle()
async def init_database(bot:Bot,event:GroupMessageEvent):
    ex = no(event.group_id)
    stat = await ex.database_exist()
    if stat:
        await bot.send_group_msg(group_id=event.group_id,message='当前功能已开启')
    else:
        info = await bot.get_group_member_info(group_id=event.group_id,user_id=bot.self_id,no_cache=True)
        if info['role'] == 'member':
            await init.finish('权限不足，无法开启，请确保机器人有管理权限')
            return
        await ex.create_tables()
        group_member_list = await bot.get_group_member_list(group_id=event.group_id,no_cache=True)
        for info in group_member_list:
            # 跳过自己的数据库添加
            if info['user_id'] == int(bot.self_id):
                continue
            await ex.insert_database(qid=info['user_id'],card=info['card'],role=info['role'],is_bmd=False)
        await ex.stat_table(increase=True)
        await init.finish(f'初始化完成，已添加{len(group_member_list)}条成员数据到数据库')

# 关闭功能
@delete_func.handle()
async def delete(bot:Bot,event:GroupMessageEvent):
    ex = no(event.group_id)
    stat = await ex.database_exist()
    if stat:  #数据库存在，删库跑路
        await ex.stat_table(increase=False)
        await ex.drop()
        await delete_func.finish("已删除数据库")
    else:
        await delete_func.finish("当前功能未开启")

# 加白名单
@increase_bmd.handle()
async def bmd(bot:Bot,event:GroupMessageEvent) -> list:
    response = database.execute("select * from sqlite_master where type='table';")
    group_enable_list = []
    for i in response:
        if i[1] != 'group_stat':
            group_enable_list.append(int(i[1][6:]))
    if event.group_id not in group_enable_list:
        await increase_bmd.finish('没开插件你加个锤子的白名单')
    # 获取@的qq号
    at_list = await get_at(event)
    ex = no(group_id=event.group_id)
    for qq in at_list:
        await ex.update_database(qid=qq,key='是否白名单',value='True')
    t1msg = [{
        'type':'text',
        'data':{
            'text':'已允许'
        }
    }]
    for qq in at_list:
        tmsg = [{
            'type':'at',
            'data':{
                'qq':qq,
                'name':''
            }
        }]
        t1msg = t1msg + tmsg
    t3msg = [{
        'type':'text',
        'data':{
            'text':'更改群名片'
        }
    }]
    msg = t1msg + t3msg
    await bot.send_group_msg(group_id=event.group_id,message=msg,auto_escape=False)

# 取消白名单
@decrease_bmd.handle()
async def no_bmd(bot:Bot,event:GroupMessageEvent):
    response = database.execute("select * from sqlite_master where type='table';")
    group_enable_list = []
    for i in response:
        if i[1] != 'group_stat':
            group_enable_list.append(int(i[1][6:]))
    if event.group_id not in group_enable_list:
        await increase_bmd.finish('没开插件你取消个锤子的白名单')
    # 获取@的qq号
    at_list = await get_at(event)
    ex = no(group_id=event.group_id)
    for qq in at_list:
        #更新下数据库的群名片
        qq_info = await bot.get_group_member_info(group_id=event.group_id,user_id=qq,no_cache=True)
        await ex.update_database(qid=qq,key='群名片',value=f'{qq_info["card"]}')
        await ex.update_database(qid=qq,key='是否白名单',value='False')
    t1msg = [{
        'type':'text',
        'data':{
            'text':'已禁止'
        }
    }]
    for qq in at_list:
        tmsg = [{
            'type':'at',
            'data':{
                'qq':qq,
                'name':''
            }
        }]
        t1msg = t1msg + tmsg
    t3msg = [{
        'type':'text',
        'data':{
            'text':'更改群名片'
        }
    }]
    msg = t1msg + t3msg
    await bot.send_group_msg(group_id=event.group_id,message=msg,auto_escape=False)

# 查看启用插件的群
@look_stat.handle()
async def stat(bot:Bot,event:Event):
    response = database.execute("select * from sqlite_master where type='table';")
    msg = '开启防止改群名片的群聊:'
    group_enable_list = []
    for i in response:
        if i[1] != 'group_stat':
            group_enable_list.append(int(i[1][6:]))
    for group in group_enable_list:
        group_info = await bot.get_group_info(group_id=group,no_cache=True)
        msg += f"""
        群号：{group}
        群聊名称：{group_info["group_name"]}
        """
    await look_stat.finish(msg)

# 加群之后保存群名片
@notice.handle()
async def save_new(bot:Bot,event:GroupIncreaseNoticeEvent):
    ex = no(event.group_id)
    exist = await ex.database_exist()
    if exist:
        pass
    else:
        return
    global waiting
    waiting = True
    await asyncio.sleep(5)
    info = await bot.get_group_member_info(group_id=event.group_id,user_id=event.user_id,no_cache=True)
    await ex.insert_database(qid=event.user_id,card=info['card'],role=info['role'],is_bmd=False)
    waiting = False

# 退群之后删除这条数据
@notice.handle()
async def delete_old(bot:Bot,event:GroupDecreaseNoticeEvent):
    ex = no(event.group_id)
    exist = await ex.database_exist()
    if exist:
        pass
    else:
        return
    await ex.delete_data(qid=event.user_id)
    

# 开始稽查
async def check():
    # 查询启用的群
    logger.info('开始稽查')
    response = database.execute("select * from sqlite_master where type='table';")
    group_enable_list = []
    # 获取开启插件的群列表
    for i in response:
        if i[1] != 'group_stat':
            group_enable_list.append(int(i[1][6:]))
    for group_id in group_enable_list:
        bot = nonebot.get_bot()
        group_member_list = await bot.get_group_member_list(group_id=group_id,no_cache=True)
        ex = no(group_id=group_id)
        # 获取群成员列表
        for member_info in group_member_list:
            qid = member_info['user_id']
            re = await ex.select_data(qid=qid)
            if re == 0:
                if qid == bot.self_id:
                    continue
                try:
                    if waiting:
                        continue
                    else:
                        await ex.insert_database(qid=qid,card=member_info['card'],role=member_info['role'],is_bmd=False)
                        logger.info(f'发现漏网之鱼{qid}')
                        continue
                except NameError:
                    await ex.insert_database(qid=qid,card=member_info['card'],role=member_info['role'],is_bmd=False)
                    logger.info(f'发现漏网之鱼{qid}')
                    continue
            if re['BMD'] == 'True':
                continue
            if re['CARD'] != member_info['card']:
                re['CHANGE_TIMES'] += 1
                await ex.update_database(qid=qid,key='更改群名片次数',value=f'{re["CHANGE_TIMES"]}')
                await bot.set_group_card(group_id=group_id,user_id=qid,card=f'{re["CARD"]}')
                await bot.send_group_msg(group_id=group_id, message=MessageSegment.at(user_id=qid)+'禁止修改群名片，机器人已自动改回原来的群名片')
            if re['ROLE'] != member_info['role']:
                await ex.update_database(qid=qid,key='身份',value=f'{member_info["role"]}')
    logger.info('稽查完成')

scheduler.add_job(check, "interval", seconds=30, id="114514")
