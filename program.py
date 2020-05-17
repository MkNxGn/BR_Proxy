from essentials import socket_ops_v2 as socket_ops
from essentials import run_data
from essentials import network_ops
import tkinter
from tkinter import messagebox
import sys
import os

def find_data_file(filename=""):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


window = tkinter.Tk()
window.title('Minecraft Bedrock Proxy - MkNxGn')
window.iconbitmap(find_data_file("fav.ico"))
top = tkinter.Frame(window)
top.pack(side=tkinter.TOP)

_ignore_ = tkinter.Label(top, text="System Log", font="bold")
_ignore_.pack()

Frame = tkinter.Frame(top, padx=10, pady=10)
Frame.pack()
SystemLog = tkinter.Text(Frame, height=15, width=60)
SystemLog.insert(tkinter.END, "Enter Remote Host:Port\n")
SystemLog.insert(tkinter.END, "Then Click Start To Host")
SystemLog.config(state=tkinter.DISABLED)
SystemLog.pack()

Frame2 = tkinter.Frame(top, padx=10, pady=10)
Frame2.pack(side=tkinter.RIGHT)

HostFrame = tkinter.Frame(Frame2)
HostFrame.pack(pady=8)

_ignore_ = tkinter.Label(HostFrame, text="Destination/Remote Settings", font="bold")
_ignore_.pack()

_ignore_ = tkinter.Label(HostFrame, text="Minecraft Server Host:Port ")
_ignore_.pack(side=tkinter.TOP)
Proxy_Settings = {}
ProxyHost = tkinter.Entry(HostFrame, width=40)
ProxyHost.pack(side=tkinter.BOTTOM)


Frame3 = tkinter.Frame(top, padx=10, pady=10)
Frame3.pack(side=tkinter.LEFT)

_ignore_ = tkinter.Label(Frame3, text="Local Settings", font="bold")
_ignore_.pack(side=tkinter.TOP)

optionalIPs = network_ops.Get_IP()


IPFrame = tkinter.Frame(Frame3)
IPFrame.pack()

tkinter.Label(IPFrame, text="Local IP:").pack(side=tkinter.LEFT)
LocalIP = tkinter.StringVar()
LocalIP.set(optionalIPs['ext'][0])

opt_ips = []
for item in optionalIPs['ext']:
    opt_ips.append(item)
for item in optionalIPs['local']:
    opt_ips.append(item)

IPOpts = tkinter.OptionMenu(IPFrame, LocalIP, *opt_ips)
IPOpts.pack(side=tkinter.RIGHT)

PortFrame = tkinter.Frame(Frame3)
PortFrame.pack(pady=5)

_ignore_ = tkinter.Label(PortFrame, text="Local Port:")
_ignore_.pack(side=tkinter.LEFT)

LocalPort = tkinter.Entry(PortFrame)
LocalPort.insert(tkinter.END, "19132")
LocalPort.pack(side=tkinter.RIGHT)

DestIP, DestPort = None, None

def new_connector(client=socket_ops.UDP_Server_Client):
    global DestPort, DestIP
    Log("New Connector: " + str(client.addr) + ". Starting Proxying To: " + str(DestIP) + ":" + str(DestPort))
    try:
        client.meta['proxy'] = socket_ops.UDP_Connector(DestIP, DestPort, timeout=3, max_buffer=5000)
        client.meta['proxy'].on_data = client.send
        client.on_data = client.meta['proxy'].send
    except Exception as e:
        print(e)
        Log("Proxying Error: ", str(e))

def Log(data=None, clear=False):
    global SystemLog
    SystemLog.config(state=tkinter.NORMAL)
    if clear:
        SystemLog.delete('1.0', tkinter.END)
    else:
        SystemLog.insert(tkinter.END, data + "\n")
    SystemLog.config(state=tkinter.DISABLED)


ServerRunning = False
ProxyServer = None
def StartProxy():
    global SystemLog, ServerRunning, RunButton, ProxyServer, DestIP, DestPort
    if ServerRunning == False:
        Log(clear=True)
        try:
            SocketIP, SocketPort = LocalIP.get(), LocalPort.get()
            DestIP, DestPort = ProxyHost.get().split(":")
            DestPort = int(DestPort)
            if "" in [SocketIP, SocketPort,  DestIP, DestPort]:
                Log("One or more required values are empty.")
                messagebox.showwarning("Empty Value", "One or more required values are empty.")
                return
            Log("Starting Server @ IP: " + SocketIP + " On Port: " + SocketPort)
            ProxyServer = socket_ops.UDP_Server(SocketIP, int(SocketPort), new_connector, max_buffer=5000)
            ServerRunning = True
            Log("Proxy Server has Started.")
            RunButton.config(text="Stop")
        except Exception as e:
            Log("Error: " + str(e))
    else:
        Log("Shutting down Proxy Server")
        ProxyServer.shutdown()
        Log("Proxy Server has been Shut down.")
        RunButton.config(text="Start")
        ServerRunning = False


Frame4 = tkinter.Frame(master=window)
Frame4.pack(side="bottom")

RunButton = tkinter.Button(master=Frame4, text="Start", command=StartProxy, width=20)
RunButton.pack(padx=10, pady=10)

window.mainloop()