# Test of dpkt
from typing import Counter
import dpkt
import datetime
import socket

inputFilename = '/home/tom/Documents/WiresharkCaptures/Junk.pcap'
outputFilename = '/home/tom/Documents/WiresharkCaptures/processedJunk.txt'

file_in = open(inputFilename, 'rb')
pcap = dpkt.pcap.Reader(file_in)

file_out = open(outputFilename, 'w')

packetCounter = 0
cumulativeBytesCounter = 0
ipcounter = 0
tcpcounter = 0
udpcounter = 0
lastSecond = -1
currentSecond = 0
udpAndIpPacketCounter = 0

srcIp = "192.168.1.12"
srcpacketCounter = 0
byteCounter = 0

for ts, buf in pcap:
    timeStamp = datetime.datetime.fromtimestamp(ts)
    packetCounter += 1
    cumulativeBytesCounter += len(buf)
    
    # Look to see if this is an ethernet packet
    eth = dpkt.ethernet.Ethernet(buf)
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
       continue

    ip = eth.data
    ipcounter += 1

    ipsrc = socket.inet_ntoa(ip.src)        
    ipdst = socket.inet_ntoa(ip.dst)
    srcport = ''
    dstport = ''

    if ip.p == dpkt.ip.IP_PROTO_TCP:
        tcpcounter +=1
        TCP = ip.data
        iptype = 'tcp'
        srcport = TCP.sport
        dstport = TCP.dport
        byteCounter += len(buf)
        udpAndIpPacketCounter += 1

    if ip.p == dpkt.ip.IP_PROTO_UDP:
        udpcounter += 1
        UDP = ip.data
        iptype = 'udp'
        srcport = UDP.sport
        dstport = UDP.dport
        byteCounter += len(buf)
        udpAndIpPacketCounter += 1

    # Set the time. On the first packet set lastSecond=currentSecond=ts.
    # Also, print out the column headers for the output
    if (udpAndIpPacketCounter == 1):
        lastSecond = ts
        outputString = "dateTime,Time,IP Type,IP Src,Src Port,IP Dest,Dest Port,Packet Size,Cumulative Bytes,Cumulative Bytes In Second,Bytes Per Second\n"
        print(outputString)
        file_out.write(outputString)

    currentSecond = ts

    # Check to see if you've entered a new second. If you have then reset the
    # byteCounter
    stringBytesPerSecond = '0'
    print(str(int(lastSecond)), str(int(currentSecond)))
    if (int(lastSecond) != int(currentSecond)):
        bytesPerSecond = byteCounter/(int(currentSecond)-int(lastSecond))
        print("resetting byteCounter. B/s=" + str(int(bytesPerSecond)))
        # Create a string that you can append on to the end of the output line
        stringBytesPerSecond = str((int(bytesPerSecond)))
        byteCounter = 0
        lastSecond = currentSecond

    outputString = timeStamp.isoformat() + "," + str(ts) + "," + iptype + "," + ipsrc + "," + str(srcport) + "," + ipdst + "," + str(dstport) + "," + str(len(buf)) + "," + str(cumulativeBytesCounter) + "," + str(byteCounter) + "," + stringBytesPerSecond +"\n"
    print(outputString)
    file_out.write(outputString)

print ("Total number of bytes in pcap file:", cumulativeBytesCounter)
print ("Total number of packets in the pcap file: ", packetCounter)
print ("Total number of ip packets: ", ipcounter)
print ("Total number of tcp packets: ", tcpcounter)
print ("Total number of udp packets: ", udpcounter)

