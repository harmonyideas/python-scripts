import math
import matplotlib
import wx
import wx.html
import sys
import numpy as np
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


# !/usr/bin/python
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   
#
# -------------------------------------------------------------------------------


aboutText = """<p>Sorry, there is no information about this program. It is
running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
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
        self.Bind(wx.EVT_CLOSE, self.onclose)
        menubar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.onclose, m_exit)
        menubar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.onabout, m_about)
        menubar.Append(menu, "&Help")
        self.SetMenuBar(menubar)
        self.statusbar = self.CreateStatusBar()

    def onclose(self, event):
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def onabout(self, event):
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
        # t = arange(0.0, 5.0, 0.01)
        t = np.arange(0.0, 1.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)


if __name__ == "__main__":
    app = wx.App()  # Error messages go to popup window
    top = Frame("MyProject")
    # fr = wx.Frame(None, title='test', size=wx.Size(800, 600))
    panel = CanvasPanel(top)
    panel.draw()
    # fr.Show()
    top.Show()
    app.MainLoop()
