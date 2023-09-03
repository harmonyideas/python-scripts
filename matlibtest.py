from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')
import math

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx

# !/usr/bin/python
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   <<MATLIB DEMO>>
#
# -------------------------------------------------------------------------------

import wxversion

#wxversion.select("2.8")
import wx, wx.html
import sys

aboutText = """<p>MatLibTest %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>"""


class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600, 400)):
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())


class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About <<project>>",
                           style=wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME | wx.RESIZE_BORDER |
                                 wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400, 200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth() + 25, irep.GetHeight() + 10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()


class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150, 150), size=(800, 600))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()

        #panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        #m_text = wx.StaticText(panel, -1, "Hello World!")
        #m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        #m_text.SetSize(m_text.GetBestSize())
        #box.Add(m_text, 0, wx.ALL, 10)

        #m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
        #m_close.Bind(wx.EVT_BUTTON, self.OnClose)
        #box.Add(m_close, 0, wx.ALL, 10)

        #panel.SetSizer(box)
        #panel.Layout()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()



class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self,-1, self.figure)
        self.sizer = wx.BoxSizer()
        self.sizer.AddStretchSpacer(1)
        self.sizer.Add(self.canvas, 0, wx.ALIGN_CENTER)
        self.sizer.AddStretchSpacer(1)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        #t = arange(0.0, 5.0, 0.01)
        t = arange(-pi, pi, 0.01)

        s = (sin(t))

        self.axes.plot(t, s)

if __name__ == "__main__":
    app = wx.App(redirect=True)  # Error messages go to popup window
    top = Frame("MyProject")
    #fr = wx.Frame(None, title='test', size=wx.Size(800, 600))
    panel = CanvasPanel(top)
    panel.draw()
    #fr.Show()
    top.Show()
    app.MainLoop()

