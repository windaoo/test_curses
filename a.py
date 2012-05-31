import curses

def notify_resize(scr):
    origy, origx = scr.getyx()
    Y, X = scr.getmaxyx()
    scr.addstr("scr is resized to (y=%d, x=%d)\n" % (Y ,X))
    #scr.hline(Y-1, 0, curses.ACS_HLINE, X)
    scr.hline(Y-40, 0, '-', X)
    scr.move(origy, origx)
    return (Y ,X)

def foo(scr):
    #notify_resize(scr)
    scr.scrollok(True)
    maxy, maxx = scr.getmaxyx()
    win = scr.subwin(1, maxx, maxy-1, 0)
    win.overwrite(scr)
    win.addstr('1')
    win.clear()
    while True:
        key = scr.getch()
        if key == curses.KEY_RESIZE:
            #notify_resize(scr)
            pass
        else:
            try:
                #scr.addstr(str(curses.keyname(key)) + "\t: ",
                win.addstr('2')
                #win.clear()
                scr.addstr(curses.keyname(key) + "\t: ",
                        #curses.A_BLINK)
                        #curses.A_BOLD)
                        #curses.A_NORMAL)
                        curses.A_REVERSE)
                        #curses.A_STANDOUT)
                        #curses.A_UNDERLINE)
                #scr.addstr(str(key) + "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n\n", curses.A_REVERSE)
                scr.addstr(str(key) + "\n", curses.A_REVERSE)
                scr.refresh()
            except:
                scr.scroll()

            win.addstr(curses.keyname(key))
            win.refresh()
    

try:
    curses.wrapper(foo)
except KeyboardInterrupt:
    pass

# vim: set tw=80 ts=4 et sw=4 fdm=indent: ###################### vim modeline #
