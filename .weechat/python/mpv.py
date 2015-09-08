#!/usr/bin/env python2

import weechat 
import json
import socket
import os.path 
import time

def get_mpv_info():
	client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	client.connect("/tmp/mpvsocket")
	res = {}
	for i in ['filename', 'media-title', 'playback-time', 'length']:
		req = '{"command": ["get_property", "%s"]}\n' %i
		client.send(req)
		res[i] = json.loads(client.recv(1024))['data']
		
	client.close()
	return res
	
def parse_info():
	np = get_mpv_info()
	filename = np['filename'].replace('_', ' ')
	title = np['media-title'].replace('_', ' ')
        progress = time.strftime("%H:%M:%S",time.gmtime(np['playback-time']))
        duration = time.strftime("%H:%M:%S", time.gmtime(np['length']))
	percent = int((np['playback-time']/np['length']) * 100)
       
	bar_prog = int(round((np['playback-time']/np['length'])*15, 1))
	bar = '['+'>'*bar_prog+'-'*(15-bar_prog)+']'
	return filename, title, progress, duration, percent, bar
 
def mpv_np(data, buffer, args):
	filename, title, progress, duration, percent, bar = parse_info()
        color = "01,01"
        op = "/me nw %s{} %s{}/{}" % ("11", "09")
	weechat.command(weechat.current_buffer(), 
	    op.format(filename, progress, duration))
	return weechat.WEECHAT_RC_OK
 
def mpv_np_title(data, buffer, args):
	filename, title, progress, duration, percent, bar = parse_info()
	weechat.command(weechat.current_buffer(), 
	    "/me nw 11{}".format(title))
	return weechat.WEECHAT_RC_OK  

weechat.register("weechat-np-mpv", "Bodzioslaw aka pwg", "0.1", "LGPL", "Now playing for mpv", "", "")

hook = weechat.hook_command("mpv", "Now playing mpv", "", "", "", "mpv_np", "")
hook = weechat.hook_command("mpv-title", "Now playing mpv with tittle", "", "", "", "mpv_np_title", "")
