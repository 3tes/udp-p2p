import socket, uuid, select, threading, time, json

port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", port))
s.setblocking(0)
active = {}
portip = {}
data = 0
addrs = 0

def main():
    threading.Thread(target=recive, daemon=True).start()
    threading.Thread(target=ping, daemon=True).start()
    while 1:
        if data == b"register":
            register()
        if "con" in str(data):
            uuids = str(data)[-37:-1]
            connect(uuids, addrs)

def get_port(ip):
    return portip[ip]
def get_uuid(ip):
    return list(active.keys())[list(active.values()).index(ip)]
def get_ip(uuidi):
    return active[uuidi]

def recive():
    global data
    global addrs
    while 1:
        ready = select.select([s], [], [], 0)
        if ready[0]:
            data, addrs = s.recvfrom(1024)

def register():
    global data
    uu = uuid.uuid4()
    au = str(uu).encode()
    s.sendto(bytes(au), addrs)
    ip, port = addrs
    active[str(uu)] = ip
    portip[ip] = port
    data = 0
    print(f"{ip}:{port} connected")

def ping():
    global active
    global portip
    global data
    delete = []
    while 1:
        if delete:
            for i in delete.copy():
                try:
                    ip = get_ip(i)
                    del active[i]
                    del portip[ip]
                    del delete[delete.index(i)]
                except:
                    del delete[delete.index(i)]
                print(f"{ip} disconected")
        if bool(active) == True:
            time.sleep(1)
            data = 0
            for i in active.copy():
                ip = get_ip(i)
                port = get_port(ip)
                s.sendto(b"ping", (ip, port))
                time.sleep(0.1)
                if data != b"here":
                    delete.append(i)

def connect(senui, sender):
    global data
    ip, port = sender
    if get_uuid(ip) == senui:
        s.sendto(b"Error : You cannot connect to your self", sender)
        data = 0
        return
    try:
        emi = get_ip(senui)
        emp = get_port(emi)
        sni, snp = sender
        s.sendto(json.dumps({"icn": "icn", "ip":emi, "port":emp}).encode("utf-8"), sender)
        s.sendto(json.dumps({"enc": "ecn", "ip":sni, "port":snp}).encode("utf-8"), (emi, emp))
    except:
        s.sendto(b"Error Invalid UUID", sender)
        data = 0


if __name__ == "__main__":
    print("ready")
    main()
