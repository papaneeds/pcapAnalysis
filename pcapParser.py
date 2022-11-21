# This python program reads in a pcap file and
# parses it (packet by packet)
# It outputs the results to a csv file
# Author: Tomas Szeredi
# Date: 11/14/2022
#

import dpkt
import datetime
import socket


inputFilename = '/home/tom/Documents/WiresharkCaptures/ParserTest.pcap'
outputFilename = '/home/tom/Documents/WiresharkCaptures/ParserTest.csv'

file_in = open(inputFilename, 'rb')
pcap = dpkt.pcap.Reader(file_in)

file_out = open(outputFilename, 'w')

file_out.write("timestamp,type,source,destination,protocol,notes\n")

packetCounter = 0
cumulativeBytesCounter = 0
ipcounter = 0

for ts, buf in pcap:
    info = ''
    outString = ''

    timeStamp = datetime.datetime.fromtimestamp(ts)
    packetCounter += 1
    cumulativeBytesCounter += len(buf)

    # Look to see if this is an ethernet packet
    eth = dpkt.ethernet.Ethernet(buf)
    typeAsString = eth.get_type(eth.type).__name__
    ip = eth.data

    if isinstance(ip.data, dpkt.icmp.ICMP):
        notes = 'ICMP'
        outString = timeStamp.isoformat() + ',' + typeAsString + ',,,' + notes
    elif isinstance(ip.data, dpkt.icmp6.ICMP6):
        notes = 'ICMP6'
        outString = timeStamp.isoformat() + ',' + typeAsString + ',,,' + notes  
    elif isinstance(ip.data, dpkt.igmp.IGMP):
        # Get the protocol as a string
        proto = ip.get_proto(ip.p).__name__
        notes = 'IGMP'
        ipsrc = socket.inet_ntoa(ip.src)        
        ipdst = socket.inet_ntoa(ip.dst)
        outString = timeStamp.isoformat() + ',' + typeAsString + ',' + ipsrc + ',' + ipdst + ',' + proto + ',' + info          
    elif (eth.type==dpkt.ethernet.ETH_TYPE_IP or eth.type==dpkt.ethernet.ETH_TYPE_IP6):
        ipcounter += 1

        # Get the protocol as a string
        proto = ip.get_proto(ip.p).__name__

        if (eth.type==dpkt.ethernet.ETH_TYPE_IP):
            ipsrc = socket.inet_ntoa(ip.src)        
            ipdst = socket.inet_ntoa(ip.dst)
        else:
            ipsrc = ''
            ipdst = ''

        srcport = ''
        dstport = ''

        if ip.p == dpkt.ip.IP_PROTO_TCP:
            TCP = ip.data
            iptype = 'tcp'
            srcport = TCP.sport
            dstport = TCP.dport
            info = str(srcport) + ' -> ' + str(dstport)
            outString = timeStamp.isoformat() + ',' + typeAsString + ',' + ipsrc + ',' + ipdst + ',' + proto + ',' + info  

        if ip.p == dpkt.ip.IP_PROTO_UDP:
            UDP = ip.data
            iptype = 'udp'
            srcport = UDP.sport
            dstport = UDP.dport 
            info = str(srcport) + ' -> ' + str(dstport)
            outString = timeStamp.isoformat() + ',' + typeAsString + ',' + ipsrc + ',' + ipdst + ',' + proto + ',' + info  
            if (srcport == 53 or dstport == 53 or srcport == 5353 or dstport == 5353):
               notes = str(srcport) + ' -> ' + str(dstport) + ' DNS or MDNS'
            outString = timeStamp.isoformat() + ',' + typeAsString + ',,,' + notes  

    else:   
        outString = timeStamp.isoformat() + ',' + typeAsString + ',,,'  

    file_out.write(outString + '\n')