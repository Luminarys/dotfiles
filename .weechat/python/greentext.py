#!/usr/bin/env python2

import weechat 

def meme_arrows(data, buffer, args):
    color = "03>"
    weechat.command(weechat.current_buffer(), color + "".join(args))
    return weechat.WEECHAT_RC_OK  

weechat.register("weechat-meme-arrows", "Luminarys", "0.1", "MIT", "Colored meme arrows", "", "")

hook = weechat.hook_command("gt", "Use meme arrows good", "", "", "", "meme_arrows", "")
hook = weechat.hook_command(">", "Use meme arrows good", "", "", "", "meme_arrows", "")
