<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ 跨平台 Python 异步机器人框架 ✨_
<!-- prettier-ignore-end -->
<p align="center">
  <a href="https://pypi.python.org/pypi/nonebot2">
    <img src="https://img.shields.io/pypi/v/nonebot2" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">
  <br />
  <a href="https://onebot.dev/">
    <img src="https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="onebot">
  </a>

  <br />
</p>

# 基于nonebot2框架的插件，适用于onebotv11协议
</div>

## 插件详解

~~懒得写了~~

- 关于命令前缀的配置，请参见[NoneBot配置](https://nb2.baka.icu/docs/appendices/config#command-start-%E5%92%8C-command-separator)
- 下列以`/`开头的指令均是使用了命令前缀`/`

- 其中防撤回修改自[nonebot-plugin-antirecall](https://github.com/Jerry080801/nonebot-plugin-antirecall/ "防撤回") ~~忘了修改了什么~~
- 战地查询插件修改自[nonebot-plugin-bfchat](https://github.com/050644zf/nonebot-plugin-bfchat) 对战地五相关的代码稍做了修改
- 测码插件
  - 发送`测码`试试吧
  - 接入[nonebot-plugin-access-control](https://github.com/bot-ssttkkl/nonebot-plugin-access-control)插件，要提前开启哦
- 广播插件
  - 此插件使用权限仅限超级管理员，详见[NoneBot SUPERUSER配置](https://nb2.baka.icu/docs/appendices/config#superusers)
  - `/msg`向指定的群里发送消息，提供可选参数项`--g`和`--bot`，其中`--g`用于将消息发至指定的群，不填则发送至本群，`--bot`用于指定发送消息的bot，不填则默认使用响应的bot，在消息中输入`[@{qq}]`可以@指定qq的人，示例
    ```
    /msg 哼哼哼啊啊啊啊啊[@114514] --g 114514 --bot 1919810
    ```
  - `/all`向所有的群发送消息，提供可选参数项`--bot`
  - 其他命令用法请发送`/help`获取
- 防止改群名片
  - 请发送`/help`获取