#!/usr/bin/python
import datetime
import time
import sys
import asyncio
import subprocess

import i3ipc
import psutil
from mpd import MPDClient

def run_async(fn, args, vals):
    future = asyncio.Future()
    args.insert(0, future)
    args.insert(1, vals)
    asyncio.ensure_future(fn(*args))
    future.add_done_callback(lambda fut: print_bar(fut, vals))

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
        return "%{A:urxvt -e sudo pacman -Syyu:}%{T2}\uf220 %{T1}" + num + "%{T1}%{A}"
    else:
        return ""

def get_net_transfer(prev):
    output = subprocess.Popen("cat /sys/class/net/wlp4s0/statistics/rx_bytes", shell=True, stdout=subprocess.PIPE).communicate()[0]
    num = int(output.decode("ascii").rstrip())
    readable_num = get_bytes(num - prev)
    return "\uf30c " + readable_num, num

def get_cpu_usage():
    return "\uf3ec " + str(psutil.cpu_percent()).rjust(4, '0') + "%"

def get_ram_usage():
    return "\uf3e0 " + get_bytes(psutil.virtual_memory().active, suffix="", lpad=1)

def get_ip_addr():
    return "%{A:connman-gtk:}\uf2c1 " + psutil.net_if_addrs()["wlp4s0"][0].address + "%{A}"

def get_mpd_info():
    client = MPDClient()
    client.connect("localhost", 6600)
    np = client.currentsong()
    pause = "%{A:mpc pause:} \uf3a7 %{A}"
    play = "%{A:mpc play:} \uf3aa %{A}"
    if "name" in np:
        return np["name"] + " " + pause + play
    else:
        return np["title"] + " " + pause + play

def get_langs():
    output = subprocess.Popen("ibus engine", shell=True, stdout=subprocess.PIPE).communicate()[0]
    c_lang = output.decode("ascii").rstrip()
    if c_lang == "xkb:us::eng":
        return "%{A:ibus engine libpinyin:}EN%{A}"
    elif c_lang == "libpinyin":
        return "%{A:ibus engine anthy:}CN%{A}"
    elif c_lang == "anthy":
        return "%{A:ibus engine xkb\:us\:\:eng:}JP%{A}"

@asyncio.coroutine
def async_date(future, vals):
    yield from asyncio.sleep(10)
    future.set_result({"date": get_date()})
    run_async(async_date, [], vals)

@asyncio.coroutine
def async_time(future, vals):
    yield from asyncio.sleep(1)
    future.set_result({"time": get_time()})
    run_async(async_time, [], vals)

@asyncio.coroutine
def async_workspaces(future, vals, i3):
    yield from asyncio.sleep(0.3)
    future.set_result({"workspaces": get_workspaces(i3, vals)})
    run_async(async_workspaces, [i3], vals)

@asyncio.coroutine
def async_package_updates(future, vals):
    yield from asyncio.sleep(600)
    future.set_result({"workspaces": get_package_updates()})
    run_async(async_package_updates, [], vals)

@asyncio.coroutine
def async_network_transfer(future, vals, prev_rx):
    yield from asyncio.sleep(1)
    disp, new_prev = get_net_transfer(prev_rx)
    future.set_result({"net_transfer": disp})
    run_async(async_network_transfer, [new_prev], vals)

@asyncio.coroutine
def async_cpu_usage(future, vals):
    yield from asyncio.sleep(1)
    future.set_result({"cpu_usage": get_cpu_usage()})
    run_async(async_cpu_usage, [], vals)

@asyncio.coroutine
def async_ram_usage(future, vals):
    yield from asyncio.sleep(5)
    future.set_result({"ram_usage": get_ram_usage()})
    run_async(async_ram_usage, [], vals)

@asyncio.coroutine
def async_ip_addr(future, vals):
    yield from asyncio.sleep(5)
    future.set_result({"ip_addr": get_ip_addr()})
    run_async(async_ip_addr, [], vals)

@asyncio.coroutine
def async_mpd_info(future, vals):
    yield from asyncio.sleep(5)
    future.set_result({"mpd_info": get_mpd_info()})
    run_async(async_mpd_info, [], vals)

@asyncio.coroutine
def async_langs(future, vals):
    yield from asyncio.sleep(2)
    future.set_result({"langs": get_langs()})
    run_async(async_langs, [], vals)

def print_bar(future, vals):
    vals.update(future.result())
    print(output.format(**vals))
    try:
        sys.stdout.flush()
    except BrokenPipeError:
        loop.stop()

i3 = i3ipc.Connection()
loop = asyncio.get_event_loop()

bytes_output = subprocess.Popen("cat /sys/class/net/wlp4s0/statistics/rx_bytes", shell=True, stdout=subprocess.PIPE).communicate()[0]
init_num_bytes = int(bytes_output.decode("ascii").rstrip())
transfer_disp, rx_bytes = get_net_transfer(init_num_bytes)

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

    "date": get_date(),
    "time": get_time(),
    "updates": get_package_updates(),
    "net_transfer": transfer_disp,
    "cpu_usage": get_cpu_usage(),
    "ram_usage": get_ram_usage(),
    "ip_addr": get_ip_addr(),
    "mpd_info": get_mpd_info(),
    "langs": get_langs(),
    }

vals["workspaces"] = get_workspaces(i3, vals)

output = "{left} {date} - {time} {center} {workspaces} {mpd_info} {right} {cpu_usage}{pad}{ram_usage}{pad}{net_transfer}{pad}{ip_addr}{pad}{updates}{pad}{langs} {f_clear}"
print(output.format(**vals))
sys.stdout.flush()

run_async(async_date, [], vals)
run_async(async_time, [], vals)
run_async(async_workspaces, [i3], vals)
run_async(async_package_updates, [], vals)
run_async(async_network_transfer, [rx_bytes], vals)
run_async(async_cpu_usage, [], vals)
run_async(async_ram_usage, [], vals)
run_async(async_ip_addr, [], vals)
run_async(async_mpd_info, [], vals)
run_async(async_langs, [], vals)

loop.run_forever()
