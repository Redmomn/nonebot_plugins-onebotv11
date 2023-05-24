import sqlite3
from nonebot import logger,on_startswith,on_regex
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import permission,GroupMessageEvent
import os



if os.path.exists('./data/fuckcard/db'):
    if os.path.isfile('./data/fuckcard/db/card_information.db'):
        pass
    else:
        try:
            logger.info('数据库不存在，即将创建数据库')
            file = open(file='./data/fuckcard/db/card_information.db',mode='w')
            file.close()
            logger.info('数据库创建成功')
        except Exception:
            logger.warning('数据库创建失败，请检查文件夹读写权限')
            raise Exception

else:
    logger.debug('数据库路径不存在，即将创建数据库目录')
    try:
        os.makedirs('./data/fuckcard/db')
    except Exception:
        logger.warning('数据库目录创建失败，请检查文件夹读写权限')
        raise Exception
    if os.path.isfile('./data/fuckcard/db/card_information.db'):
        pass
    else:
        try:
            logger.info('数据库不存在，即将创建数据库')
            file = open(file='./data/fuckcard/db/card_information.db',mode='w')
            file.close()
            logger.info('数据库创建成功')
        except Exception:
            logger.warning('数据库创建失败，请检查文件夹读写权限')
            raise Exception


client = sqlite3.connect('./data/fuckcard/db/card_information.db')
database = client.cursor()


#好像没用
async def database_exist(group_id:int) -> bool :
    response = database.execute(f'''
                     SELECT count(*) 
                     FROM sqlite_master 
                     WHERE type='table' 
                     AND name = 'group_{group_id}';
                     ''')
    if response[0] == 1: #存在表则返回1
        return True
    else:
        return False

#创建表
async def create_tables(group_id:int):
    database.execute(f'''
                     CREATE TABLE group_{group_id}(QID INT PRIMARY KEY NOT NULL,
                     禁言码 INT NOT NULL,
                     反制码 INT NOT NULL,
                     测别人码次数 INT NOT NULL,
                     被禁言次数 INT NOT NULL,
                     反制别人次数 INT NOT NULL,
                     被反制次数 INT NOT NULL);
                     ''')

#查询数据
async def select_data(group_id:int,qid:int) -> dict :
    try:
        #查找用户的所有数据
        response = database.execute(f'''
                                    SELECT * FROM group_{group_id} where {qid};
                                    ''')
    except sqlite3.OperationalError:                    #表不存在
        await create_tables(group_id=group_id)
        response = database.execute(f'''
                                    SELECT * FROM group_{group_id} where {qid};
                                    ''')
    data = response.fetchall()
    #数据为空，用户不存在此表中
    if data == []:
        await insert_database(group_id=group_id,qid=qid)
        response = database.execute(f'''
                                    SELECT * FROM group_{group_id} where {qid};
                                    ''')
        return response[0]
    else:
        return response[0]
        
#表里不存在的用户，插入数据，全部置零
async def insert_database(group_id:int,qid:int):
    '''
    数据库插入数据
    参数:
        group_id(int):QQ群号,也就是数据库的表
    '''
    database.execute(f'''
                     INSERT INTO group_{group_id} VALUES ({qid},0,0,0,0,0,0);
                     ''')
    #提交更改
    client.commit()

async def update_database(group_id:int,qid:int,key:str,value:int|str):
    database.execute(f'''
                     UPDATE group_{group_id} 
                     SET {key}={value} 
                     WHERE QID={qid};
                     ''')
    client.commit()
    

