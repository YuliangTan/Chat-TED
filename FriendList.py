#!/usr/bin/python
#coding=utf-8
import os
import wx
import sys
import Talk
import redis
import thread
import simplejson as json
from gi.repository import Notify
def default_cb(n, action,txt):
    assert action == "view_text"
    Talk.myapp(None,id=-1,title=_("With ") + txt['send'] + _(" Talking"),user_name=txt['send'],un=txt['user'],addcon=txt['content'])
    n.close()
class MyFrame(wx.Frame):
    def OnClickLeftKey(self, event,un):
        Talk.myapp(None,id=-1,title=_("With ") + self.tree.GetItemText(event.GetItem()) + _(" Talking"),user_name=self.tree.GetItemText(event.GetItem()),un=un,addcon="")
    def OnClose(self, event,un):
        dlg = wx.MessageDialog(self, 
            _("Do you really want to close this application?"),
            _("Confirm Exit"), wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
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
        for i in user['item']:
                ch=self.tree.AppendItem(root, i) 
                for j in user[i]:
                        self.tree.AppendItem(ch, j)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Center()
        self.Bind(wx.EVT_CLOSE, lambda evt,un=un : self.OnClose(evt,un))
        global un_g
        un_g = un
        thread.start_new_thread(self.receive, ())
    def receive(self):
       rd = redis.Redis(host='pub-redis-19834.us-east-1-4.5.ec2.garantiadata.com',port=19834,password='22842218')
       ps = rd.pubsub()
       #ps.subscribe(['test', 'user'])
       ps.subscribe([un_g])
       for item in ps.listen():
          if item['type'] == 'message':
               text_json= json.loads(item['data'])
               if text_json['type'] == 'info-in-line':
                   if text_json['user'] == un_g: 
                       Notify.init ("Chat-TYL")
                       n = Notify.Notification.new (text_json['send'] + _(" say:"),text_json['content'],"file://" + os.path.abspath(os.path.curdir) + "/Chat-TYL.ico")
                       n.add_action("view_text", _("Click me to see"), lambda n,action,txt =text_json: default_cb(n,action,txt))
                       n.show ()  