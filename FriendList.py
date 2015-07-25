#!/usr/bin/python
#coding=utf-8
import os
import wx
import sys
import Talk
import redis
from xml.etree import ElementTree as ET
class MyFrame(wx.Frame):
    def OnClickLeftKey(self, event,un):
        Talk.myapp(user_name=self.tree.GetItemText(event.GetItem()),un=un)
    def OnClose(self, event,un):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            os.remove(un + ".xml")
            sys.exit()
    def __init__(self, parent, id, title,user,un):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, wx.Size(200, 450))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, -1)
        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1, -1),
                                wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, lambda evt,un=un : self.OnClickLeftKey(evt,un), self.tree)
        root = self.tree.AddRoot('My friend')
        per=ET.parse(user)
        t=per.findall('/count/tag')
        for oneper in t:  #找出person节点
                ch=self.tree.AppendItem(root, oneper.text)
                u=per.findall('/' + oneper.text + '/person')        
                for oneper in u:
                        for chi in oneper.getchildren():
                                print chi.text
                                self.tree.AppendItem(ch, chi.text)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Center()
        self.Bind(wx.EVT_CLOSE, lambda evt,un=un : self.OnClose(evt,un))