import curses
import curses.ascii
import curses.textpad

class main_win(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.text = []
        self.draw()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        self.iserror_attr = curses.color_pair(1)

    def __addstr(self, s, iserror=False):
        try:
            if iserror:
                self.win.addstr(s, self.iserror_attr)
            else:
                self.win.addstr(s)
        except:
            self.win.scroll()
        self.win.refresh()

    def draw(self):
        maxy, maxx = self.stdscr.getmaxyx()
        self.win = self.stdscr.subwin(maxy-1, maxx, 0, 0)
        self.win.scrollok(True)
        #self.win = curses.newwin(maxy-1, maxx, 0, 0)
        self.win.erase()
        for s, e in self.text:
            self.__addstr(s, e)

    def addstr(self, s, iserror):
        self.text.append((s, iserror,))
        self.__addstr(s, iserror)

class status_bar(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stryx = lambda: "y: %d, x: %d" % self.win.getmaxyx()
        self.hint_str = "Hint: "
        self.draw()

    def __addstr(self, s):
        try:
            self.win.addstr(s, curses.A_BLINK)
        except:
            self.win.scroll()
        self.win.refresh()

    def draw(self):
        maxy, maxx = self.stdscr.getmaxyx()
        self.win = self.stdscr.subwin(1, maxx, maxy-1, 0)
        self.win.scrollok(True)

    def reprint(self):
        self.win.erase()
        s = self.hint_str
        #s += ' ' * (self.win.getmaxyx()[1] - len(s) - 1)
        self.__addstr(s)

    def hint(self, c):
        self.hint_str = "Hint: '%s'" % c
        self.reprint()

    def clearhint(self):
        self.hint_str = "Hint: "
        self.reprint()

class UI(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.main_win = main_win(stdscr)
        self.status_bar = status_bar(stdscr)

    def redraw(self):
        self.stdscr.clear()
        self.main_win.draw()
        self.status_bar.draw()

    def handle_input(self, c, iserror=False):
        self.main_win.addstr(c, iserror)

    def handle_error_input(self, c):
        self.status_bar.hint(c)
    def clearhint(self): self.status_bar.clearhint()
    def refresh(self):
        self.stdscr.refresh()
        self.status_bar.win.refresh()
        self.main_win.win.refresh()

def xx(stdscr):
    stdscr.scrollok(True)
    fcontent = open("text").read()
    ui = UI(stdscr)
    i = 0
    is_error = -1
    #stdscr.addstr("|"+ str(ord(curses.ascii.ctrl('x'))) + "|")

    while True:
        c = stdscr.getch()
        if c == ord(curses.ascii.ctrl('q')):
            break
        elif ord(fcontent[i]) == c:
            if is_error == i:
                ui.handle_input(fcontent[i], True)
                ui.clearhint()
            else:
                ui.handle_input(fcontent[i])

            if i == len(fcontent):
                break
            i += 1
        elif curses.KEY_RESIZE == c:
            ui.redraw()
        else:
            #ui.handle_input(str(curses.keyname(c)))
            ui.handle_error_input(fcontent[i])
            is_error = i
        ui.refresh()

def main(stdscr):
    try:
        xx(stdscr)
    except KeyboardInterrupt:
        pass

curses.wrapper(main)

# vim: set ts=4 sts=4 sw=4 et: ################## vim modeline ################
