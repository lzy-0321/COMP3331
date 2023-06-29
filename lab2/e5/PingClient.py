from socket import *
import sys
import time
import statistics
import datetime


def Statistics (rtts):
    if len(rtts) > 0:
        Min_rtt = min(rtts)
        Max_rtt = max(rtts)
        Avg_rtt = statistics.mean(rtts)
        print(f'Min RTT is {int(Min_rtt)} ms, Max RTT is {int(Max_rtt)} ms, Avg RTT is {int(Avg_rtt)} ms\n')
    if len(rtts) == 0:
        print('ALL TIME OUT, Ping is not working\n')

def ping (host,port):
    # Create a UDP socket
    serverName = host
    serverPort = port
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    #Create UDP client socket
    seqnum = 3331
    rtts = []
    while(seqnum < 3345):
        sequence = seqnum
        seqnum += 1
        starttime = time.time()
        # change starttime to year, month, day, hour, minute, second, microsecond
        # use time.time() - the second since 1970 until this minute to get the microsecond
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        message = 'PING:' + ' ' + str(seqnum) + ' ' + 'TIME:' + ' ' + str(dt_ms) + '\r\n'
        clientSocket.sendto(message.encode('utf-8'),(serverName, serverPort))
        clientSocket.settimeout(0.6)
        #Waits up to 600 ms to receive a reply
        try:
            data, address = clientSocket.recvfrom(2048)
            data = data.decode('utf-8')
            ip_address = address[0]
            port_number = address[1]
            gettime = time.time()
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # calculate the time difference in ms
            usetime = (gettime - starttime) * 1000
            rtts.append(usetime)
            print(f'Ping to {ip_address} {port_number}, Time = {str(dt_ms)}, seq = {sequence}, rtt = {int(usetime)} ms')
        except timeout:
            print(f'Ping to {serverName} {serverPort}, Time = {str(dt_ms)}, seq = {sequence}, timeout')
    print('Finished')
    # calculate the minimum, maximum and average RTT, check the ping is working or not
    Statistics(rtts)
    clientSocket.close()
    # Close the socket


if len(sys.argv) < 3:
    print('required host prot')
    exit(1)
host = sys.argv[1]
port = int (sys.argv[2])
ping(host, port)
