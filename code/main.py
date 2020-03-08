from serial_port import Port



port = Port("com4",115200,1)
send_str="AT\r\n"
send_bytes = bytes(send_str, encoding="utf8")
port.Send_data(send_bytes)
# for each_char in send_bytes:
#     port.Send_data(each_char)
print(str(port.Read_size(20),encoding="utf8"))
print("123\r\n123123")

#byte=bytes("123123", encoding="utf8")