#!/bin/python
import i3ipc

def adjust_gaps(i3, e):
    focused = i3.get_tree().find_focused().workspace()
    non_floating = 0
    if hasattr(focused, "nodes"):
        for c in filter(lambda c: c.type != "floating_con", focused.nodes):
            non_floating += 1
        gaps = 51 - 13 * (non_floating)
        i3.command("gaps outer current set " + str(gaps))

def run():
    i3 = i3ipc.Connection()
    adjust_gaps(i3, None)
    
    i3.on('workspace::focus', adjust_gaps)
    i3.on('window::floating', adjust_gaps)
    i3.on('window::new', adjust_gaps)
    i3.on('window::close', adjust_gaps)
    
    i3.main()

if __name__ == "__main__":
    run()
