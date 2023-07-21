# bigipf5-api-export-data
A script to get all data from bigip F5 LTM Load Balancers and write to mysql database

Summary 

This Python script has 2 parts, the first one read BigIP F5 Load Balancers management IPs from a text file (bigipf5ips.txt) and connect them via SSH. Then execute a Curl request from CLI and get all configurations (IP, virtual server IP, virtual server  name, poolname, partition, poolmembers, ports...etc) then write all the output to text files first. (bigipf5tsonuc.txt and bigipf5vspools) 

* For Security Requirements in our devices iControl and API features are disabled so we need to make an SSH  connection first to execute Curl commands *
  
The second part of the script read the text files (bigipf5tsonuc.txt and bigipf5vspools) and connect to a mysql databases and write all data to database.

![image](https://github.com/goksinenki/bigipf5-api-export-data/assets/917944/f361fb96-ccaf-4cc6-8800-dd7108945f5a)

![image](https://github.com/goksinenki/bigipf5-api-export-data/assets/917944/702c2dd6-c450-4b08-b94d-36e95466a4e4)

Installation / Requirements

pip install paramiko
pip install pymysql
pip install json

