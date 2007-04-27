#!/usr/bin/env python

# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by John Hoffman

from __future__ import division

from BitTorrent.platform import install_translation
install_translation()

DOWNLOAD_SCROLL_RATE = 1

import sys, os
from threading import Event
from time import time, localtime, strftime

from BitTorrent.obsoletepythonsupport import *
from BitTorrent.launchmanycore import LaunchMany
from BitTorrent.defaultargs import get_defaults
from BitTorrent.parseargs import parseargs, printHelp
from BitTorrent import configfile
from BitTorrent import version
from BitTorrent import BTFailure

try:
    curses = import_curses()
    import curses.panel
    from curses.wrapper import wrapper as curses_wrapper
    from signal import signal, SIGWINCH
except:
    print _("Textmode GUI initialization failed, cannot proceed.")
    print
    print _("This download interface requires the standard Python module "
            "\"curses\", which is unfortunately not available for the native "
            "Windows port of Python. It is however available for the Cygwin "
            "port of Python, running on all Win32 systems (www.cygwin.com).")
    print
    print _("You may still use \"btdownloadheadless.py\" to download.")
    sys.exit(1)

exceptions = []

def fmttime(n):
    if n <= 0:
        return None
    n = int(n)
    m, s = divmod(n, 60)
    h, m = divmod(m, 60)
    if h > 1000000:
        return _("connecting to peers")
    return _("ETA in %d:%02d:%02d") % (h, m, s)

def fmtsize(n):
    n = long(n)
    unit = [' B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    i = 0
    if (n > 999):
        i = 1
        while i + 1 < len(unit) and (n >> 10) >= 999:
            i += 1
            n >>= 10
        n /= 1024
    if i > 0:
        size = '%.1f' % n + '%s' % unit[i]
    else:
        size = '%.0f' % n + '%s' % unit[i]
    return size

def ljust(s, size):
    s = s[:size]
    return s + (' '*(size-len(s)))

def rjust(s, size):
    s = s[:size]
    return (' '*(size-len(s)))+s


class CursesDisplayer(object):

    def __init__(self, scrwin):
        self.messages = []
        self.scroll_pos = 0
        self.scroll_time = 0

        self.scrwin = scrwin
        signal(SIGWINCH, self.winch_handler)
        self.changeflag = Event()
        self._remake_window()
        curses.use_default_colors()

    def winch_handler(self, signum, stackframe):
        self.changeflag.set()
        curses.endwin()
        self.scrwin.refresh()
        self.scrwin = curses.newwin(0, 0, 0, 0)
        self._remake_window()
        self._display_messages()

    def _remake_window(self):
        self.scrh, self.scrw = self.scrwin.getmaxyx()
        self.scrpan = curses.panel.new_panel(self.scrwin)
        self.mainwinh = (2*self.scrh)//3
        self.mainwinw = self.scrw - 4  # - 2 (bars) - 2 (spaces)
        self.mainwiny = 2         # + 1 (bar) + 1 (titles)
        self.mainwinx = 2         # + 1 (bar) + 1 (space)
        # + 1 to all windows so we can write at mainwinw

        self.mainwin = curses.newwin(self.mainwinh, self.mainwinw+1,
                                     self.mainwiny, self.mainwinx)
        self.mainpan = curses.panel.new_panel(self.mainwin)
        self.mainwin.scrollok(0)
        self.mainwin.nodelay(1)

        self.headerwin = curses.newwin(1, self.mainwinw+1,
                                       1, self.mainwinx)
        self.headerpan = curses.panel.new_panel(self.headerwin)
        self.headerwin.scrollok(0)

        self.totalwin = curses.newwin(1, self.mainwinw+1,
                                      self.mainwinh+1, self.mainwinx)
        self.totalpan = curses.panel.new_panel(self.totalwin)
        self.totalwin.scrollok(0)

        self.statuswinh = self.scrh-4-self.mainwinh
        self.statuswin = curses.newwin(self.statuswinh, self.mainwinw+1,
                                       self.mainwinh+3, self.mainwinx)
        self.statuspan = curses.panel.new_panel(self.statuswin)
        self.statuswin.scrollok(0)

        try:
            self.scrwin.border(ord('|'),ord('|'),ord('-'),ord('-'),ord(' '),ord(' '),ord(' '),ord(' '))
        except:
            pass
        rcols = (_("Size"),_("Download"),_("Upload"))
        rwids = (8, 10, 10)
        rwid = sum(rwids)
        start = self.mainwinw - rwid
        self.headerwin.addnstr(0, 2, '#', start, curses.A_BOLD)
        self.headerwin.addnstr(0, 4, _("Filename"), start, curses.A_BOLD)

        for s,w in zip(rcols, rwids):
            st = start + max(w - len(s), 0)
            self.headerwin.addnstr(0, st, s[:w], len(s[:w]), curses.A_BOLD)
            start += w

        self.totalwin.addnstr(0, self.mainwinw - 27, _("Totals:"), 7, curses.A_BOLD)

        self._display_messages()

        curses.panel.update_panels()
        curses.doupdate()
        self.changeflag.clear()


    def _display_line(self, s, bold = False):
        if self.disp_end:
            return True
        line = self.disp_line
        self.disp_line += 1
        if line < 0:
            return False
        if bold:
            self.mainwin.addnstr(line, 0, s, self.mainwinw, curses.A_BOLD)
        else:
            self.mainwin.addnstr(line, 0, s, self.mainwinw)
        if self.disp_line >= self.mainwinh:
            self.disp_end = True
        return self.disp_end

    def _display_data(self, data):
        if 3*len(data) <= self.mainwinh:
            self.scroll_pos = 0
            self.scrolling = False
        elif self.scroll_time + DOWNLOAD_SCROLL_RATE < time():
            self.scroll_time = time()
            self.scroll_pos += 1
            self.scrolling = True
            if self.scroll_pos >= 3*len(data)+2:
                self.scroll_pos = 0

        i = self.scroll_pos//3
        self.disp_line = (3*i)-self.scroll_pos
        self.disp_end = False

        while not self.disp_end:
            ii = i % len(data)
            if i and not ii:
                if not self.scrolling:
                    break
                self._display_line('')
                if self._display_line(''):
                    break
            ( name, status, progress, peers, seeds, seedsmsg, dist,
              uprate, dnrate, upamt, dnamt, size, t, msg ) = data[ii]
            t = fmttime(t)
            if t:
                status = t
            name = ljust(name,self.mainwinw-32)
            size = rjust(fmtsize(size),8)
            uprate = rjust('%s/s' % fmtsize(uprate),10)
            dnrate = rjust('%s/s' % fmtsize(dnrate),10)
            line = "%3d %s%s%s%s" % (ii+1, name, size, dnrate, uprate)
            self._display_line(line, True)
            if peers + seeds:
                datastr = _("    (%s) %s - %s peers %s seeds %s dist copies - %s dn %s up") % (
                    progress, status, peers, seeds, dist,
                    fmtsize(dnamt), fmtsize(upamt) )
            else:
                datastr = '    '+status+' ('+progress+')'
            self._display_line(datastr)
            self._display_line('    '+ljust(msg,self.mainwinw-4))
            i += 1

    def display(self, data):
        if self.changeflag.isSet():
            return

        inchar = self.mainwin.getch()
        if inchar == 12: # ^L
            self._remake_window()

        self.mainwin.erase()
        if data:
            self._display_data(data)
        else:
            self.mainwin.addnstr( 1, self.mainwinw//2-5,
                                  _("no torrents"), 12, curses.A_BOLD )
        totalup = 0
        totaldn = 0
        for ( name, status, progress, peers, seeds, seedsmsg, dist,
              uprate, dnrate, upamt, dnamt, size, t, msg ) in data:
            totalup += uprate
            totaldn += dnrate

        totalup = '%s/s' % fmtsize(totalup)
        totaldn = '%s/s' % fmtsize(totaldn)

        self.totalwin.erase()
        self.totalwin.addnstr(0, self.mainwinw-27, _("Totals:"), 7, curses.A_BOLD)
        self.totalwin.addnstr(0, self.mainwinw-20 + (10-len(totaldn)),
                              totaldn, 10, curses.A_BOLD)
        self.totalwin.addnstr(0, self.mainwinw-10 + (10-len(totalup)),
                              totalup, 10, curses.A_BOLD)

        curses.panel.update_panels()
        curses.doupdate()

        return inchar in (ord('q'),ord('Q'))

    def message(self, s):
        self.messages.append(strftime('%x %X - ',localtime(time()))+s)
        self._display_messages()

    def _display_messages(self):
        self.statuswin.erase()
        winpos = 0
        for s in self.messages[-self.statuswinh:]:
            self.statuswin.addnstr(winpos, 0, s, self.mainwinw)
            winpos += 1
        curses.panel.update_panels()
        curses.doupdate()

    def exception(self, s):
        exceptions.append(s)
        self.message(_("SYSTEM ERROR - EXCEPTION GENERATED"))



def LaunchManyWrapper(scrwin, config):
    LaunchMany(config, CursesDisplayer(scrwin), 'launchmany-curses')


if __name__ == '__main__':
    uiname = 'launchmany-curses'
    defaults = get_defaults(uiname)
    try:
        if len(sys.argv) < 2:
            printHelp(uiname, defaults)
            sys.exit(1)
        config, args = configfile.parse_configuration_and_args(defaults,
                                      uiname, sys.argv[1:], 0, 1)
        if args:
            config['torrent_dir'] = args[0]
        if not os.path.isdir(config['torrent_dir']):
            raise BTFailure(_("Warning: ")+args[0]+_(" is not a directory"))
    except BTFailure, e:
        print _("error: ") + str(e) + _("\nrun with no args for parameter explanations")
        sys.exit(1)

    curses_wrapper(LaunchManyWrapper, config)
    if exceptions:
        print _("\nEXCEPTION:")
        print exceptions[0]
