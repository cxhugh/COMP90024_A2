
def server_address():
    with open('../deploy/config/generic.yaml',encoding='utf8') as f:
        text = f.readlines()
        for line in text:
            if line.startswith("dbServer"):
                ip = line.split(":")[1].strip()

    return "http://admin:admin@" + ip +':5984/'

#print(server_address())