# This file is use to get ip of each server
def server_address():
    with open('./generic.yaml',encoding='utf8') as f:
        text = f.readlines()
        for line in text:
            if line.startswith("dbServer"):
                ip = line.split(":")[1].strip()

    return ip

def readfile():
    with open ('./generic.yaml','r') as f:
    # with open ('../deploy/config/generic.yaml','r') as f:
        data = f.readlines()
    f.close()
    ips = {}
    for i in data[8:]:
        name_ip = i.split(":")
        ips[name_ip[0]] = name_ip[1].strip()
    return ips

def get_dbserver_ip():
    ips = readfile()
    return ips['dbServer']
 
def get_harvester1_ip():
    ips = readfile()
    return ips['harverster1'] 

def get_harvester2_ip():
    ips = readfile()
    return ips['harverster2']   


# db_server = 'http://admin:admin@' + get_dbserver_ip() + ':5984'
# print(db_server)
