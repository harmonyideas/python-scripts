#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import random


class TicTacToe(wx.Frame):
    counter = 0
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    scale = {'width': 90, 'height': 90}
    moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(self, parent, title):

        super(TicTacToe, self).__init__(parent, title=title,
                                        size=(400, 400))
        self.panel = wx.Panel(self)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.l1 = wx.StaticText(
            self.panel, -1, "Please select a move [0-8]", pos=(3, 325))

        hbox1.Add(self.l1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.t1 = wx.TextCtrl(self.panel, pos=(165, 320),
                              size=(50, 25), style=wx.TE_PROCESS_ENTER)

        hbox1.Add(self.t1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.t1.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)
        self.Centre()
        self.Show()

    def OnPaint(self, e):
        dc = wx.ClientDC(self)
        column = 10
        row = 15
        z = 0
        for x in range(0, 3):
            for y in range(0, 3):
                self.board[z] = [column, row, self.scale['width'],
                                 self.scale['height']]
                dc.DrawRectangle(column, row, int(self.scale['width']),
                                 int(self.scale['height']))
                dc.DrawLabel(str(self.moves[z]),
                             self.board[z], wx.ALIGN_CENTER)
                column = column + 100
                z = z + 1
            column = 10
            row = row + 100
        forecolor = (153, 0, 0)
        dc.SetTextForeground(forecolor)

    def OnEnterPressed(self, e):
        pos = self.t1.GetValue()
        if pos.lower() == "q":
            quit()

        self.updatemoves(int(pos), "P1")
        self.computermoves("C")

        if self.checkmoves("P1"):
            print("P1 is the Winner!")
        elif self.checkmoves("C"):
            print("Computer is the Winner!")

        self.t1.SetValue("")
        self.Refresh()
        self.Update()

    def updatemoves(self, pos, player):
        if self.counter <= 8:
            self.moves[pos] = player
            self.counter += 1
        else:
            print("Out of moves")

    def findmoves(self):
        cpumoves = []
        for x in range(9):
            if self.moves[x] == int(x):
                cpumoves.insert(x, x)
        return cpumoves

    def computermoves(self, player):
        if self.counter < 8:
            choice = random.choice(self.findmoves())
            self.moves[choice] = player
            self.counter += 1
        else:
            print("Out of moves")
        return 0

    def checkmoves(self, le):
        return ((self.moves[0] == le and self.moves[1] == le and self.moves[2] == le) or  # across the top
                # across the middle
                (self.moves[3] == le and self.moves[4] == le and self.moves[5] == le) or
                # across the bottom
                (self.moves[6] == le and self.moves[7] == le and self.moves[8] == le) or
                # down the left side
                (self.moves[0] == le and self.moves[3] == le and self.moves[6] == le) or
                # down the middle
                (self.moves[1] == le and self.moves[4] == le and self.moves[7] == le) or
                # down the right side
                (self.moves[2] == le and self.moves[5] == le and self.moves[8] == le) or
                # diagonal
                (self.moves[2] == le and self.moves[4] == le and self.moves[6] == le) or
                (self.moves[0] == le and self.moves[4] == le and self.moves[8] == le))  # diagonal


if __name__ == '__main__':
    app = wx.App()
    TicTacToe(None, 'TicTacToe')
    app.MainLoop()
