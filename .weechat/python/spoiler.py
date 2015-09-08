#!/usr/bin/env python2

import weechat 

def spoiler_colors(data, buffer, args):
    color = "01,01"
    weechat.command(weechat.current_buffer(), color + "".join(args))
    return weechat.WEECHAT_RC_OK  

weechat.register("weechat-spoilers", "Luminarys", "0.1", "MIT", "Spoiler colors", "", "")

hook = weechat.hook_command("spoiler", "Now using spoiler colors", "", "", "", "spoiler_colors", "")
