# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Syslog Generator

Had a need to generate generic syslog messages to 
test open source logging solutions.
'''

#syslog_gen.py --host 192.168.1.100 --port 514 --file sample_logs --count 10 --sleep 30
#--host syslog 전송할 주소
#--port syslog 전송할 포트
#--file 전송할 파일
#--count 전송할 메시지 수량 
#--sleep 연속 전송 시 유휴 시간 (sec)
#crontab -e > python3 /root/syslog_send_1.py --host 61.36.41.92 --port 514 --file syslog.txt --count 10

import socket
import argparse
import random
import sys
import time
import logging
import requests
import os
import glob
import fnmatch
from logging.handlers import SysLogHandler

"""
Modify these variables to change the hostname, domainame, and tag
that show up in the log messages. 
"""   
hostname = "syslog_host" #header 1
domain_name = "192.168.1.10" #header 2
tag = ["kernel", "python", "ids", "ips"]
syslog_level = ["info", "error", "warn", "critical"]

def raw_udp_sender(message, host, port):
    # Stubbed in or later use
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = bytes(message, 'UTF-8')
        send = sock.sendto(message, (host, port))
    finally:
        sock.close()

def open_sample_log(sample_log):
    #for download_file in glob.glob('link.txt'):
    download_file = 'link.txt' #download 파일명
    url = 'http://gdata.co.kr/link/document/' + download_file #Download 경로

    r = requests.get(url, allow_redirects=True)
    open('syslog.txt', 'wb').write(r.content) #저장할 파일명

    try:
        with open(sample_log, 'r') as sample_log_file:
            random_logs = random.choice(list(sample_log_file))
            return random_logs
    except FileNotFoundError:
        print("[+] ERROR: Please specify valid filename")
        return sys.exit()

def syslogs_sender():
    # Initalize SysLogHandler
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    syslog = SysLogHandler(address=(args.host, args.port))
    logger.addHandler(syslog)

    for message in range(1, args.count+1):
        # Randomize some fields
        time_output = time.strftime("%b %d %H:%M:%S")
        random_host = " "
        #random_host = random.choice(range(1, 11))
        random_tag = random.choice(tag)
        random_level = random.choice(syslog_level)
        fqdn = "{0}{1}{2}".format(hostname, random_host, domain_name)
        random_pid = random.choice(range(500,9999))

        message = open_sample_log(args.file)

        fields = {'host_field': fqdn, 'date_field': time_output,\
                'tag_field': random_tag}
	
        format = logging.Formatter\
                ('%(date_field)s %(host_field)s {0}[{1}]: %(message)s'\
                .format(random_tag, random_pid))
        syslog.setFormatter(format)
			
        print("[+] Sent: {0}: {1}".format(time_output, message), end='')

        getattr(logger, random_level)(message, extra=fields)

    logger.removeHandler(syslog)
    syslog.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True,
                        help="Remote host to send messages")
    parser.add_argument("--port", type=int, required=True,
                        help="Remote port to send messages")
    parser.add_argument("--file", required=True,
                        help="Read messages from file")
    parser.add_argument("--count", type=int, required=True,
                        help="Number of messages to send")
    parser.add_argument("--sleep", type=float, help="Use with count flag to \
                        send X messages every X seconds, sleep being seconds")

    args = parser.parse_args()

    if args.sleep:
        print("[+] Sending {0} messages every {1} seconds to {2} on port {3}"\
            .format(args.count, args.sleep, args.host, args.port))
        try:
            while True:
                syslogs_sender()
                time.sleep(args.sleep)
                os.remove('syslog.txt') #removed file
        except KeyboardInterrupt:
            # Use ctrl-c to stop the loop
            print("[+] Stopping syslog generator...")
            os.remove('syslog.txt')  # removed file
    else:
        print("[+] Sending {0} messages to {1} on port {2}".format
            (args.count, args.host, args.port))
        syslogs_sender()
        os.remove('syslog.txt') #removed file

