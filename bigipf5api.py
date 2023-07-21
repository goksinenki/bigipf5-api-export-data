#!/usr/bin/python
# -*- coding: UTF-8 -*-
# A script to ssh into a cisco device, set the terminal length
# such that paging is turned off, then run commands.
# the results go into 'resp', then are displayed.
# Tweak to your hearts content!

import paramiko
import cmd
import time
import sys
import requests, json
import time
from time import time, sleep
import threading
from decimal import *
import datetime
from datetime import datetime
import pymysql
import threading
from queue import Queue

my_file1 = open('bigipf5ips.txt', 'rb')
for line in my_file1:
    l = [i.strip() for i in line.decode().split(' ')]
    IP = l[0]
    if IP == "ipaddress1" or IP == "ipaddress2":
        # IP = sys.argv[1]
        # pool = sys.argv[2]
        my_file = open('bigipf5sonuc.txt', 'w')
        my_file2 = open('bigipf5vspools.txt', 'w')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP, username='root', password='F5_SSHPASSWORD')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command(
            'curl -u root:F5_SSHPASSWORD -sk --request GET \'https://127.0.0.1/mgmt/tm/ltm/virtual\'')

        list = stdout.readlines()
        output = [line.rstrip() for line in list]
        a = ('\n'.join(output))
        print(IP)
        # print (a)
        output_dict = json.loads(a)
        kactane = len(output_dict['items']);
        for i in range(0, kactane):
            try:
                # print (i)
                vsname = (output_dict['items'][i]['name'])
                vspartitionipport = (output_dict['items'][i]['destination'])
                poolpart = (output_dict['items'][i]['pool'])
                connectionLimit = (output_dict['items'][i]['connectionLimit'])
                ipProtocol = (output_dict['items'][i]['ipProtocol'])
                # my_file.write('%s,%s,%s,%s,%s,%s'%(IP,vsname,vspartitionipport,poolpart,connectionLimit,ipProtocol) + "\n")
                vsipport = vspartitionipport.split("/")[2]
                vspartition = vspartitionipport.split("/")[1]
                vsip = vsipport.split(":")[0]
                vsport = vsipport.split(":")[1]
                poolname = poolpart.split("/")[2]
                partition = poolpart.split("/")[1]
                pool = poolpart.replace("/", "~")
                # print (poolpart)
                stdin, stdout, stderr = ssh.exec_command(
                    'curl -u root:F5_SSHPASSWORD -sk --request GET \'https://127.0.0.1/mgmt/tm/ltm/pool/%s/members\'' % (
                        pool))
                list2 = stdout.readlines()
                # print (list2)
                output2 = [line.rstrip() for line in list2]
                b = ('\n'.join(output2))
                my_file2.write('%s,%s,%s,%s,%s,%s' % (IP, vsip, vsname, vsport, partition, poolname + "\n"))
                # print (b)
                try:
                    output_dict2 = json.loads(b)
                    # print (output_dict2)
                    kactane2 = len(output_dict2['items']);
                    for k in range(0, kactane2):
                        try:
                            nodepartport = (output_dict2['items'][k]['fullPath'])
                            nodeip = (output_dict2['items'][k]['address'])
                            nodestate = (output_dict2['items'][k]['state'])
                            nodestate2 = (output_dict2['items'][k]['session'])
                            ratio = (output_dict2['items'][k]['ratio'])
                            nodeport = nodepartport.split(":")[1]
                            my_file.write('%s,%s,%s,%s,%s,%s,%s' % (
                                IP, vsname, poolname, nodeip, nodeport, nodestate, nodestate2) + "\n")
                        except KeyError as ke:
                            print('Key Not Found in pool dict:', ke)
                except json.JSONDecodeError:
                    print("Empty response")
            except KeyError as ke:
                print('Key Not Found in virtualserver dict:', ke)
        my_file.close()
        my_file2.close()
        ssh.close()
        my_file3 = open('bigipf5vspools.txt', 'rb')
        for line in my_file3:
            l = [i.strip() for i in line.decode().split(',')]
            IP = l[0]
            vsip = l[1]
            vsname = l[2]
            vsport = l[3]
            partition = l[4]
            poolname = l[5]
            sql = """INSERT INTO BIGIP_vip_params (vpx_ip,ipv46,vip_name,port,parti,poolname) VALUES ('%s','%s','%s','%s','%s','%s')""" % (
                IP, vsip, vsname, vsport, partition, poolname)
      
            db = pymysql.connect(host='DBSERVERIPADDRESS',
                                 user='root',
                                 password='DBPASSWORD',
                                 database='DBNAME',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            # print (sql)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Commit your changes in the database
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            db.close()

        my_file3.close()

        my_file4 = open('bigipf5sonuc.txt', 'rb')
        for line in my_file4:
            l = [i.strip() for i in line.decode().split(',')]
            IP = l[0]
            vip_name = l[1]
            poolname = l[2]
            memberip = l[3]
            memberport = l[4]
            memberstatus = l[5]
            monitorstatus = l[6]

            sql = """INSERT INTO BIGIP_service_params (vpx_ip,vip_name,poolname,memberip,memberport,memberstatus,monitorstatus) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (
                IP, vip_name, poolname, memberip, memberport, memberstatus, monitorstatus)
  
            db = pymysql.connect(host='DBSERVERIPADDRESS',
                                 user='root',
                                 password='DBPASSWORD',
                                 database='DBNAME',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            # print (sql)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Commit your changes in the database
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            db.close()

        my_file4.close()
    else:
        # IP = sys.argv[1]
        # pool = sys.argv[2]
        # IP = "10.129.48.47"
        my_file = open('bigipf5sonuc.txt', 'w')
        my_file2 = open('bigipf5vspools.txt', 'w')
        # pool = "ME_DM2_VIP_Pool"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP, username='F5_SSHUSERNAME', password='F5_SSHPASSWORD')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command(
            'curl -u F5_SSHUSERNAME:F5_SSHPASSWORD -sk --request GET \'https://127.0.0.1/mgmt/tm/ltm/virtual\'')
 
        list = stdout.readlines()
        output = [line.rstrip() for line in list]
        a = ('\n'.join(output))
        print(IP)
        # print (a)
        output_dict = json.loads(a)
        kactane = len(output_dict['items']);
        for i in range(0, kactane):
            try:
                # print (i)
                vsname = (output_dict['items'][i]['name'])
                vspartitionipport = (output_dict['items'][i]['destination'])
                poolpart = (output_dict['items'][i]['pool'])
                connectionLimit = (output_dict['items'][i]['connectionLimit'])
                ipProtocol = (output_dict['items'][i]['ipProtocol'])
                # my_file.write('%s,%s,%s,%s,%s,%s'%(IP,vsname,vspartitionipport,poolpart,connectionLimit,ipProtocol) + "\n")
                vsipport = vspartitionipport.split("/")[2]
                vspartition = vspartitionipport.split("/")[1]
                vsip = vsipport.split(":")[0]
                vsport = vsipport.split(":")[1]
                poolname = poolpart.split("/")[2]
                partition = poolpart.split("/")[1]
                pool = poolpart.replace("/", "~")
                # print (poolpart)
                stdin, stdout, stderr = ssh.exec_command(
                    'curl -u F5_SSHUSERNAME:F5_SSHPASSWORD -sk --request GET \'https://127.0.0.1/mgmt/tm/ltm/pool/%s/members\'' % (
                        pool))
                list2 = stdout.readlines()
                # print (list2)
                output2 = [line.rstrip() for line in list2]
                b = ('\n'.join(output2))
                my_file2.write('%s,%s,%s,%s,%s,%s' % (IP, vsip, vsname, vsport, partition, poolname + "\n"))
                # print (b)
                try:
                    output_dict2 = json.loads(b)
                    # print (output_dict2)
                    kactane2 = len(output_dict2['items']);
                    for k in range(0, kactane2):
                        try:
                            nodepartport = (output_dict2['items'][k]['fullPath'])
                            nodeip = (output_dict2['items'][k]['address'])
                            nodestate = (output_dict2['items'][k]['state'])
                            nodestate2 = (output_dict2['items'][k]['session'])
                            ratio = (output_dict2['items'][k]['ratio'])
                            nodeport = nodepartport.split(":")[1]
                            my_file.write('%s,%s,%s,%s,%s,%s,%s' % (
                                IP, vsname, poolname, nodeip, nodeport, nodestate, nodestate2) + "\n")
                        except KeyError as ke:
                            print('Key Not Found in pool dict:', ke)
                except json.JSONDecodeError:
                    print("Empty response")
            except KeyError as ke:
                print('Key Not Found in virtualserver dict:', ke)
        my_file.close()
        my_file2.close()
        ssh.close()
        my_file3 = open('bigipf5vspools.txt', 'rb')
        for line in my_file3:
            l = [i.strip() for i in line.decode().split(',')]
            IP = l[0]
            vsip = l[1]
            vsname = l[2]
            vsport = l[3]
            partition = l[4]
            poolname = l[5]
            sql = """INSERT INTO BIGIP_vip_params (vpx_ip,ipv46,vip_name,port,parti,poolname) VALUES ('%s','%s','%s','%s','%s','%s')""" % (
                IP, vsip, vsname, vsport, partition, poolname)
            
            db = pymysql.connect(host='DBSERVERIPADDRESS',
                                 user='root',
                                 password='DBPASSWORD',
                                 database='DBNAME',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            # print (sql)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Commit your changes in the database
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            db.close()

        my_file3.close()

        my_file4 = open('bigipf5sonuc.txt', 'rb')
        for line in my_file4:
            l = [i.strip() for i in line.decode().split(',')]
            IP = l[0]
            vip_name = l[1]
            poolname = l[2]
            memberip = l[3]
            memberport = l[4]
            memberstatus = l[5]
            monitorstatus = l[6]

            sql = """INSERT INTO BIGIP_service_params (vpx_ip,vip_name,poolname,memberip,memberport,memberstatus,monitorstatus) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (
                IP, vip_name, poolname, memberip, memberport, memberstatus, monitorstatus)
            db = pymysql.connect(host='DBSERVERIPADDRESS',
                                 user='root',
                                 password='DBPASSWORD',
                                 database='DBNAME',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            # print (sql)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Commit your changes in the database
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            db.close()

        my_file4.close()
my_file1.close()

# sys.exit (1)