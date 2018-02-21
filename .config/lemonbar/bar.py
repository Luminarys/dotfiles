#!/usr/bin/python
import datetime
import time
import sys
import asyncio
import subprocess
import copy
import re

import i3ipc
import psutil

interface = "enp0s31f6"

def get_bytes(num, suffix='/s', lpad=3):
    for unit in ['Bit','KiB','MiB','GiB','TiB','PiB','EiB','ZiB']:
        if abs(num) < 1024.0:
            return ("%3.1f %s%s" % (num, unit, suffix)).rjust(6 + len(suffix) + lpad, '0')
        num /= 1024.0
    return ("%.1f %s%s" % (num, 'YiB', suffix)).rjust(6 + len(suffix) + lpad, '0')

def get_date():
    today = datetime.date.today()
    return today.strftime("%A %B %d, %Y")

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def get_workspaces(i3, vals):
    output = sys.argv[1]
    workspaces = i3.get_workspaces()
    res = ""
    for workspace in filter(lambda ws: ws.output==output, workspaces):
        name = workspace["name"]
        nvals = {
                "click_start": "%{A:i3-msg workspace " + name + ":}",
                "click_end": "%{A}",
                "name": name
                }
        nvals.update(vals)
        disp = "{click_start}{name}{click_end}"
        if workspace["visible"]:
            res += ("{ul_white}{start_ul}" + disp + "{end_ul} ").format(**nvals)
        else:
            res += disp.format(**nvals) + " "
    return "%{A4:i3-msg workspace next_on_output:}%{A5:i3-msg workspace prev_on_output:}" + res + "%{A}%{A}"

def get_package_updates():
    output = subprocess.Popen("pacman -Qu | wc -l", shell=True, stdout=subprocess.PIPE).communicate()[0]
    num = output.decode("ascii").rstrip()
    if num != "0":
        return "%{A:urxvt -e sudo pacman -Syyu:}%{T2}\uf0ee %{T1}" + num + "%{T1}%{A}"
    else:
        return "\uf05d"

def get_net_transfer(prev):
    output = subprocess.Popen("cat /sys/class/net/" + interface + "/statistics/rx_bytes", shell=True, stdout=subprocess.PIPE).communicate()[0]
    num = int(output.decode("ascii").rstrip())
    readable_num = get_bytes(num - prev)
    return "\uf0ec " + readable_num, num

def get_cpu_usage():
    return "\uf110 " + str(psutil.cpu_percent()).rjust(4, '0') + "%"

def get_ram_usage():
    return "\uf2db " + get_bytes(psutil.virtual_memory().active, suffix="", lpad=1)

def get_ip_addr():
    main_ip_addr = psutil.net_if_addrs()[interface][0].address
    if re.match('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', main_ip_addr):
        return "%{A:connman-gtk --no-icon:}\uf0e8 " + main_ip_addr + "%{A}"
    else:
        return "%{A:connman-gtk --no-icon:}\uf0e8 None%{A}"

def get_mpd_info():
    # client = MPDClient()
    # client.connect("localhost", 6600)
    # np = client.currentsong()
    # pause = "%{A:mpc pause:} \uf3a7 %{A}"
    # play = "%{A:mpc play:} \uf3aa %{A}"
    # if "name" in np:
    #     return np["name"] + " " + pause + play
    # elif "title" in np:
    #     return np["title"] + " " + pause + play
    # else:
    #     return "\uf3bb"
    return "\uf3bb"

def get_langs():
    output = subprocess.Popen(["ibus", "engine"], stdout=subprocess.PIPE).communicate()[0]
    c_lang = output.decode("ascii").rstrip()
    if c_lang == "xkb:us::eng":
        return "%{A:ibus engine libpinyin:}EN%{A}"
    elif c_lang == "libpinyin":
        return "%{A:ibus engine anthy:}CN%{A}"
    elif c_lang == "anthy":
        return "%{A:ibus engine xkb\:us\:\:eng:}JP%{A}"

def get_power():
    with open("/sys/class/power_supply/BAT1/charge_now") as fin:
        current_power = int(fin.readline())
    with open("/sys/class/power_supply/BAT1/charge_full") as fin:
        total_power = int(fin.readline())
    percent = 100 * current_power/total_power
    if percent == 100:
        return "\uf114"
    elif percent > 25:
        return "\uf116 {0:.1f}%".format(percent)
    else:
        return "\uf113 {0:.1f}%".format(percent)

vals = {
    "left": "%{l}",
    "right": "%{r}",
    "center": "%{c}",
    "f_white": "%{F#FF000000}",
    "f_clear": "%{F-}",
    "b_black": "%{B#FFFFFFFF}",
    "ul_white": "%{U#FFFFFFFF}",
    "start_ul": "%{+u}",
    "end_ul": "%{-u}",
    "pad": "  ",
    "font_1": "%{T1}",
    "font_2": "%{T2}",
    "font_3": "%{T3}",
    "font_4": "%{T4}",
    }

class async_module(object):
    def __init__(self, interval, args = []):
        self.interval = interval
        self.args = args
        self._loop = asyncio.get_event_loop()

    def _set(self):
        future = asyncio.Future()
        self.args.insert(0, future)
        self.args.insert(1, vals)
        future.add_done_callback(lambda fut: print_bar(fut, vals))
        self._handler = self._loop.call_later(self.interval, self._run)

    def _run(self):
        self.args = self.fn(*self.args)
        self._set()

    def __call__(self, fn):
        self.fn = fn
        future = asyncio.Future()
        self.args.insert(0, future)
        self.args.insert(1, vals)
        future.add_done_callback(lambda fut: set_val(fut, vals))
        self.args = fn(*self.args)
        self._set()

@async_module(10, [])
def async_date(future, vals):
    future.set_result({"date": get_date()})
    return []

@async_module(1, [])
def async_time(future, vals):
    future.set_result({"time": get_time()})
    return []

i3 = i3ipc.Connection()

@async_module(.3, [i3])
def async_workspaces(future, vals, i3):
    future.set_result({"workspaces": get_workspaces(i3, vals)})
    return [i3]

@async_module(600, [])
def async_package_updates(future, vals):
    future.set_result({"updates": get_package_updates()})
    return []

bytes_output = subprocess.Popen(["cat", "/sys/class/net/" + interface + "/statistics/rx_bytes"], stdout=subprocess.PIPE).communicate()[0]
init_num_bytes = int(bytes_output.decode("ascii").rstrip())
_transfer_disp, rx_bytes = get_net_transfer(init_num_bytes)

@async_module(1, [rx_bytes])
def async_network_transfer(future, vals, prev_rx):
    disp, new_prev = get_net_transfer(prev_rx)
    future.set_result({"net_transfer": disp})
    return [new_prev]

@async_module(1, [])
def async_cpu_usage(future, vals):
    future.set_result({"cpu_usage": get_cpu_usage()})
    return []

@async_module(5, [])
def async_ram_usage(future, vals):
    future.set_result({"ram_usage": get_ram_usage()})
    return []

@async_module(5, [])
def async_ip_addr(future, vals):
    future.set_result({"ip_addr": get_ip_addr()})
    return []

@async_module(5, [])
def async_mpd_info(future, vals):
    future.set_result({"mpd_info": get_mpd_info()})
    return []

# @async_module(2, [])
# def async_langs(future, vals):
#     future.set_result({"langs": get_langs()})
#     return []

def set_val(future, vals):
    vals.update(future.result())

def print_bar(future, vals):
    output = "{left} {date} - {time} {center} {workspaces} {right} {cpu_usage}{pad}{ram_usage}{pad}{net_transfer}{pad}{ip_addr}{pad}{pad}{updates}{pad}{f_clear}"
    vals.update(future.result())
    print(output.format(**vals))
    try:
        sys.stdout.flush()
    except BrokenPipeError:
        loop.stop()

loop = asyncio.get_event_loop()
loop.run_forever()
