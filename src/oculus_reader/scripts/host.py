import socket
import json
import time
from oculus_reader import OculusReader  # 替换为你的 OculusReader 导入路径

def serialize_data(transforms, buttons):
    # 将 numpy 矩阵转换为列表，方便 JSON 序列化
    data = {}
    if transforms is not None:
        data['transforms'] = {k: v.tolist() for k, v in transforms.items()}
    else:
        data['transforms'] = None
    data['buttons'] = buttons
    return json.dumps(data)

def main():
    # 目标服务器 IP 和端口
    SERVER_IP = '192.168.31.71'  # 替换为接收端 IP
    SERVER_PORT = 8888          # 替换为接收端端口

    # 创建 TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"尝试连接服务器 {SERVER_IP}:{SERVER_PORT} ...")
    sock.connect((SERVER_IP, SERVER_PORT))
    print("连接成功！")

    oculus_reader = OculusReader(print_FPS=False)

    try:
        while True:
            time.sleep(0.1)  # 发送频率 10Hz，可根据需求调整
            transforms, buttons = oculus_reader.get_transformations_and_buttons()
            if transforms is None or buttons is None:
                continue
            data_str = serialize_data(transforms, buttons)
            # 发送数据，末尾加换行符方便接收端按行读取
            sock.sendall((data_str + '\n').encode('utf-8'))
    except KeyboardInterrupt:
        print("程序终止，关闭连接...")
    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        sock.close()
        oculus_reader.stop()
        print("已退出。")

if __name__ == '__main__':
    main()
