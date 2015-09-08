#!/usr/bin/env python2

import weechat 

def spurdo(data, buffer, args):
    replacements = [
        ["[.]", " :DD"],
        [",", " XDD"],
        ["''", ""],

        ["wh", "w"],
        ["th", "d"],

        ["af", "ab"],
        ["ap", "ab"],
        ["ca", "ga"],
        ["ck", "gg"],
        ["co", "go"],
        ["ev", "eb"],
        ["ex", "egz"],
        ["et", "ed"],
        ["iv", "ib"],
        ["it", "id"],
        ["ke", "ge"],
        ["nt", "nd"],
        ["op", "ob"],
        ["ot", "od"],
        ["po", "bo"],
        ["pe", "be"],
        ["pi", "bi"],
        ["up", "ub"],
        ["va", "ba"],

        ["ck", "gg"],
        ["cr", "gr"],
        ["kn", "gn"],
        ["lt", "ld"],
        ["mm", "m"],
        ["nt", "dn"],
        ["pr", "br"],
        ["ts", "dz"],
        ["tr", "dr"],

        ["bs", "bz"],
        ["ds", "dz"],
        ["es", "es"],
        ["fs", "fz"],
        ["gs", "gz"],
        [" is", " iz"],
        ["ls", "lz"],
        ["ms", "mz"],
        ["ns", "nz"],
        ["rs", "rz"],
        ["ss", "sz"],
        ["ts", "tz"],
        ["us", "uz"],
        ["ws", "wz"],
        ["ys", "yz"],

        ["alk", "olk"],
        ["ing", "ign"],

        ["ic", "ig"],
        ["ng", "nk"],

        ["kek", "geg"],
        ["epic", "ebin"],
    ]

    text = "".join(args)
    for rep in replacements:
        text = text.replace(rep[0], rep[1])

    weechat.command(weechat.current_buffer(), text)
    return weechat.WEECHAT_RC_OK  

weechat.register("weechat-spurdo", "Luminarys", "0.1", "MIT", "Spurdo your text", "", "")

hook = weechat.hook_command("spurdo", "Makes your message ebin ;DD", "", "", "", "spurdo", "")
