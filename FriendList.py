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
        fm = self.tree.AppendItem(root, 'Family people')
        tr = self.tree.AppendItem(root, 'Teacher')
        cl = self.tree.AppendItem(root,'ClassMate')
        fr = self.tree.AppendItem(root, 'Friend')
        ot = self.tree.AppendItem(root, 'Other')
        per=ET.parse(user)
        p=per.findall('/family/person')
        q=per.findall('/friend/person')
        r=per.findall('/teacher/person')
        for oneper in p:  #找出person节点
                for child in oneper.getchildren(): #找出person节点的子节点
                        self.tree.AppendItem(fm, child.text)
        for oneper in r:  
                for child in oneper.getchildren(): 
                        self.tree.AppendItem(tr, child.text)
        #cl = self.tree.AppendItem(pl, 'Dev Language')
        #sl = self.tree.AppendItem(pl, 'Shell')
        for oneper in q:  
                for child in oneper.getchildren(): 
                        self.tree.AppendItem(fr, child.text)        
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Center()
        self.Bind(wx.EVT_CLOSE, lambda evt,un=un : self.OnClose(evt,un))
        #self.Bind(wx.EVT_CLOSE, self.OnClose)