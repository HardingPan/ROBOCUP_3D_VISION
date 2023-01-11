import socket


def my_send(data_type, data):
    data_type = int(data_type)
    data = str(data)

    data_bytes = bytes.fromhex(data)

    type_str = "%08x" % data_type
    type_bytes = bytes.fromhex(type_str)

    length = len(data_bytes)
    length_str = "%08x" % length
    length_bytes = bytes.fromhex(length_str)

    result_bytes = type_bytes + length_bytes + data_bytes
    # print(result_bytes)
    return result_bytes


ip = '192.168.1.66'
port = 6666

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))  # 连接裁判盒

msg = my_send(1, "0000")  # 得到二进制数据
client.sendall(msg)  # 发送
