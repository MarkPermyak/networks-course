import time
import struct
import socket
import select

def ping(host):
    send, accept, lost = 0, 0, 0
    sumtime, shorttime, longtime  =  0, 1000, 0
    data_type, data_code, data_checksum = 8, 0, 0
    data_ID = 0
    data_Sequence = 1
    payload_body = b'abcdefghijklmnopqrstuvwxyz12345.' 

    addr  =  socket.gethostbyname(host)
    print(f"Обмен пакетами с {host} по с 32 байтами данных:")
    for batch in range(0, 4):
        send = batch + 1

        icmp_packet = struct.pack('>BBHHH32s',
                              data_type,
                              data_code,
                              data_checksum,
                              data_ID,
                              data_Sequence + batch,
                              payload_body)
        icmp_chesksum = chesksum(icmp_packet)
        icmp_packet = struct.pack('>BBHHH32s',
                              data_type,
                              data_code,
                              icmp_chesksum,
                              data_ID,
                              data_Sequence + batch,
                              payload_body)
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        request_time = time.time()
        s.sendto(icmp_packet, (addr, 80))

        times = reply_ping(request_time, s, data_Sequence + batch)
        if times > 0:
            print(f"Ответ от {addr}: число байт = 32 время = {int(times * 1000)} мс")
            accept += 1
            return_time = int(times * 1000)
            sumtime += return_time
            if return_time > longtime:
                longtime = return_time
            if return_time < shorttime:
                shorttime = return_time
            time.sleep(0.7)
        else:
            lost += 1
            print("Истекло время запроса.")
        if send == 4:
            print(f"Статистика Ping для {addr}:")
            print(f"\tПакетов: отправлено = {batch + 1}, получено = {accept}, потерянно = {batch + 1 - accept}")
            print(f"\t({int((batch + 1 - accept) / (batch + 1) * 100)}% потерь)")
            print(f"Приблизительное время приема-передачи в мс:")
            print(f"\tМинимальное = {shorttime} мс, Максимальное = {longtime} мс, Среднее = {sumtime/send} мс")

def chesksum(data):
    n = len(data)
    m = n % 2
    sum = 0
    for i in range(0, n - m ,2):
        sum += (data[i]) + ((data[i+1]) << 8)
    if m:
        sum += (data[-1])
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16) 
    answer = ~sum & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def reply_ping(request_time, s, data_Sequence, timeout = 2):
    while True:
        start = time.time()
        ready = select.select([s], [], [], timeout)
        waiting = (time.time() - start)
        if ready[0] == []:
            return -1
        time_received = time.time()
        received_packet, _ = s.recvfrom(1024)
        icmpHeader = received_packet[20:28]
        type, _, _, _, sequence = struct.unpack(">BBHHH", icmpHeader)
        if type == 0 and sequence == data_Sequence:
            return time_received - request_time
        timeout = timeout - waiting
        if timeout <= 0:
            return -1
 
if __name__ == "__main__":
    host = input("ping ")
    ping(host)
