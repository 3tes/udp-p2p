import socket, time, threading, sys, select, json, os, math, pickle

server = "51.89.75.5"
sport = 8080
saddr = (server, sport)
port = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)
reg = False
data = 0
adrrs = (server, sport)
stop = False
peer_ip = ""
peer_port = 0
last = []
done = False


def main():
    global peer_ip
    global peer_port
    threading.Thread(target=recive, daemon=True).start()
    if reg == False:
        re = str(register())[2:-1]
        print(f"Your UUID is: {re}")
    threading.Thread(target=ping, daemon=True).start()
    inp = input("Do you wand to send (s) or recive (r) ? : ")
    if inp == "s":
        ui = input("To wich UUID do you want to connect ? : ")
        connecting(ui)

    elif inp == "r":
        print("Waiting of conection")
        while "enc" not in str(data):
            time.sleep(1)
        m_recive()
    else:
        print("Error")
        exit(200)



def register():
    global data
    s.sendto(b"register", (server, sport))
    time.sleep(0.1)
    return data

def recive():
    global data
    global adrrs
    global s
    while 1:
        if stop:
            break
        ready = select.select([s], [], [], 0)
        if ready[0]:
            data, addrs = s.recvfrom(8000)

def ping():
    i = 0
    global data
    global done
    while 1:
        if stop:
            break
        if data == b"ping":
            s.sendto(b"here", adrrs)
            data = 0
        if "Message" in str(data):
            print(str(data)[2:-1])
            data = 0
        if data == b"pping":
            s.sendto(b"pping", adrrs)
            data = 0
        if data == b"dis":
            print("Disconected")
            os._exit(1)
        if "bfile" in str(data):
            print("Start")
            threading.Thread(target=file_recive, args=(data,), daemon=True).start()
            data = 0
        if "ps$" in str(data):
            sdata = str(data)[2:-1].split("$")
            lost = pickle.loads(str(sdata[1]))
            time.sleep(0.3)
            for i in lost:
                s.sendto(bytes(str(f"ft${i}$" + last[i]).encode()), (peer_ip, peer_port))
            data = 0
        if data == b"done":
            done = True


def connecting(uuids):
    global peer_ip
    global peer_port
    if len(uuids) != 36:
        print("invalid UUID")
        exit(404)
    print("Connecting")
    s.sendto(b"con-uuid-" + bytes(uuids.encode()), saddr)
    time.sleep(0.1)
    if "Error" in str(data):
        print(str(data)[2:-1])
        exit(404)
    while "icn" not in str(data):
        time.sleep(1)
    ziel = json.loads(data.decode("utf-8"))
    peer_ip = ziel["ip"]
    peer_port = ziel["port"]
    i = 3
    while i != 0:
        s.sendto(b"pping", (peer_ip, peer_port))
        i = i - 1
        time.sleep(0.5)
    print("Connected")
    send_file()

def send_file():
    global data
    global last
    fi = input("Which file woud you like to send ?(full path): ")

    with open(fi, "rb") as f:
        fdata = f.read(7800)
        while data:
            last.append(data)
            data = f.read(7800)
    parts = len(last)
    name = os.path.basename(fi)
    s.sendto(bytes(f"bfile ${parts}${name}".encode()), (peer_ip, peer_port))
    time.sleep(2)
    n = 0
    for i in last:
        s.sendto(bytes(f"ft${n}${i}".encode()), (peer_ip, peer_port))
        print(f"Sending: {n}")
        n = n + 1
    s.sendto(b"efile", (peer_ip, peer_port))
    while done == False:
        time.sleep(1)
    print("Done")

def file_recive(init):
    global data
    fa = {}
    ar = str(init.decode()).split("$")
    parts = ar[1]
    name = ar[2]
    print(f"Getting {name} with {parts} parts")
    for i in range(int(parts)):
        fa[i] = 0
    fa = frecive(fa)
    wf = open(name, "wb")
    for f in fa:
        val = fa[f]
        wf.write(val)
    wf.close()
    s.sendto(b"done", (peer_ip, peer_port))

def check(fa):
    lost = []
    for a in fa:
        if fa[a] == 0:
            lost.append(a)
    if not lost:
        return fa
    else:
        psend(lost, fa)

def psend(lost, fa):
    load = pickle.dumps(lost)
    s.sendto(bytes(str("ps$" + load).encode()), (peer_ip, peer_port))
    frecive(fa)

def frecive(fa):
    global data
    while 1:
        if "ft" in data:
            cdata = data.decode().split("$")
            fa[cdata[0]] = cdata[1]
            data = 0
            print(f"Reciving: {cdata[0]}")
        if data == b"efile":
            data = 0
            fa = check(fa)
            return fa


def message():
    while 1:
        m = input("Message: ")
        s.sendto(b"Message : " + bytes(m.encode()), (peer_ip, peer_port))




def m_recive():
    i = 3
    ziel = json.loads(data.decode("utf-8"))
    peer_ip = ziel["ip"]
    peer_port = ziel["port"]
    print("Connected")
    while i != 0:
        s.sendto(b"pping", (peer_ip, peer_port))
        i = i - 1
        time.sleep(0.5)
    while 1:
        time.sleep(0.5)



if __name__ == "__main__":
    #try:
    main()
    #except:
        #s.sendto(b"dis", (peer_ip, peer_port))
