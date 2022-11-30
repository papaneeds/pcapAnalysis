# This python program reads in a pcap file and
# parses it (packet by packet)
# It outputs the results to a csv file
# Author: Tomas Szeredi
# Date: 11/14/2022
#

import dpkt
import datetime
import socket
import sys

def check_for_ports(srcport, dstport, info):
    # check to see if either the srcport or dstport is one of the well-known
    # or registered ports. If it is then print that in the description
    if (srcport in wellKnownPorts):
        info = "srcport=" + str(srcport) + " " + wellKnownPorts[srcport]
    elif (srcport in registeredPorts):
        info = "srcport=" + str(srcport) + " " + registeredPorts[srcport]
    elif (dstport in wellKnownPorts):
        info = "dstport=" + str(dstport) + " " + wellKnownPorts[dstport]
    elif (dstport in registeredPorts):
        info = "dstport=" + str(dstport) + " " + registeredPorts[dstport]
    else:
        info = "unknown"
    return info

# Read in the files that have the definitions of the well known and registered
# ports
# These files were obtained from Wikipedia (after a bit of processing in Excel
# and saving as tab-delimited files)
wellKnownPorts = {}
registeredPorts = {}

wellKnownPortsFile = open('WellKnownPorts.txt', 'r')
wellKnownPortsLines = wellKnownPortsFile.readlines()

for line in wellKnownPortsLines:
    port, description = line.split("\t")
    wellKnownPorts[port] = description.rstrip().replace(',',' ')

wellKnownPortsFile.close()

registeredPortsFile = open('RegisteredPorts.txt', 'r')
registeredPortsLines = registeredPortsFile.readlines()

for line in registeredPortsLines:
    port, description = line.split("\t")
    registeredPorts[port] = description.rstrip().replace(',',' ')

registeredPortsFile.close()

# do a brutally simple command line argument extraction
# argparse is probably a better way to go, but for now just
# do this.
[program, inputFilename, outputFilename] = sys.argv

file_in = open(inputFilename, 'rb')
pcap = dpkt.pcap.Reader(file_in)

file_out = open(outputFilename, 'w')

file_out.write("timestamp,type,source_ip,source_port,destination_ip,destination_port, protocol,notes\n")

packetCounter = 0
cumulativeBytesCounter = 0
ipcounter = 0

for ts, buf in pcap:
    outString = ''
    info = ''
    timeStamp = ''
    typeAsString = ''
    ipsrc = ''
    srcport = ''
    ipdst = ''
    dstport = ''
    proto = ''

    timeStamp = datetime.datetime.fromtimestamp(ts).isoformat()
    packetCounter += 1
    cumulativeBytesCounter += len(buf)

    # Look to see if this is an ethernet packet
    eth = dpkt.ethernet.Ethernet(buf)
    typeAsString = eth.get_type(eth.type).__name__
    ip = eth.data

    if isinstance(ip.data, dpkt.icmp.ICMP):
        info = 'ICMP'
    elif isinstance(ip.data, dpkt.icmp6.ICMP6):
        info = 'ICMP6'
    elif isinstance(ip.data, dpkt.igmp.IGMP):
        # Get the protocol as a string
        proto = ip.get_proto(ip.p).__name__
        info = 'IGMP'
        ipsrc = socket.inet_ntoa(ip.src)        
        ipdst = socket.inet_ntoa(ip.dst)     
    elif (eth.type==dpkt.ethernet.ETH_TYPE_IP or eth.type==dpkt.ethernet.ETH_TYPE_IP6):
        ipcounter += 1
        # Get the protocol as a string
        proto = ip.get_proto(ip.p).__name__

        if (eth.type==dpkt.ethernet.ETH_TYPE_IP):
            ipsrc = socket.inet_ntoa(ip.src)        
            ipdst = socket.inet_ntoa(ip.dst)

        if ip.p == dpkt.ip.IP_PROTO_TCP:
            TCP = ip.data
            iptype = 'tcp'
            srcport = str(TCP.sport)
            dstport = str(TCP.dport)

            info = check_for_ports(srcport, dstport, info)

        if ip.p == dpkt.ip.IP_PROTO_UDP:
            UDP = ip.data
            iptype = 'udp'
            srcport = str(UDP.sport)
            dstport = str(UDP.dport) 

            info = check_for_ports(srcport, dstport, info)
    
    outString = timeStamp + ',' + typeAsString + ',' + ipsrc + ',' + srcport + ',' + ipdst + ',' + dstport + ',' + proto + ',' + info
    file_out.write(outString + '\n')



