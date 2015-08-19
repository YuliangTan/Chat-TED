#!/usr/bin/python
#coding=utf-8
import os
import wx
import sys
import time
import Talk
import pymongo
from pymongo_pubsub import Publisher
from pymongo_pubsub import Subscriber
import thread
import simplejson as json
import wx.lib.agw.toasterbox as TB
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import urllib2
def default_cb(evt):
    Talk.myapp(None,id=-1,title=_("With ") + text_json['send'] + _(" Talking"),user_name=text_json['send'],un=text_json['user'],addcon=text_json['content'])
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
            connection = pymongo.MongoClient('mongodb://tyl:22842218@ds051738.mongolab.com:51738/tylchat?authMechanism=SCRAM-SHA-1').get_default_database()
            connection.drop_collection(un)
            sys.exit()
    def AddFriend(self,event):
        """
        Based on the wxPython demo by the same name
        """
        dlg = wx.TextEntryDialog(
                self, 'Please Enter Your Friend Name',
                'Add Friend', '')
        if dlg.ShowModal() == wx.ID_OK:
            if not dlg.GetValue():
               wx.MessageBox(_('Please enter your Friend name'), _('Error'), 
                  wx.OK | wx.ICON_ERROR)
            else:
              name = dlg.GetValue()
              try:
                friend = urllib2.urlopen("http://chat-tyl.coding.io/put_db.php?content=PASS&db=USER&where=NAME&where_a==&where_t=" + name).read()
              except urllib2.HTTPError,e:
                wx.MessageBox(_('Check Your NetWork,and try it again'),_('Error'), wx.OK | wx.ICON_ERROR)
              if friend == '':
                 wx.MessageBox(_("We can't find it"),_('Error'), wx.OK | wx.ICON_ERROR)
              else:
                dlg = wx.SingleChoiceDialog(
                      self, "Find your Friend", 'Search results',
                      [name], 
                      wx.CHOICEDLG_STYLE
                      )
                if dlg.ShowModal() == wx.ID_OK:
                   try:
                     list = urllib2.urlopen("http://chat-tyl.coding.io/put_db.php?content=FRIEND&db=USER&where=NAME&where_a==&where_t=" + name).read()
                     data = json.loads(list)
                   except urllib2.HTTPError,e:
                     wx.MessageBox(_('Check Your NetWork,and try it again'),_('Error'), wx.OK | wx.ICON_ERROR)   
                   for i in data['item']:
                       for j in data[i]:
                           if j == name:
                              connection = pymongo.MongoClient('mongodb://tyl:22842218@ds051738.mongolab.com:51738/tylchat?authMechanism=SCRAM-SHA-1').get_default_database()
                              if un_g not in connection.collection_names():
                                 connection.create_collection(un_g,
                                                    capped=True,
                                                    size=1000000,
                                                    max=None)                               
                              publisher = Publisher(connection, name)
                              send_dic = {
                              'type': 'add-friend',
                              'user' : un_g 
                              }
                              user = json.dumps(send_dic)
                              publisher.push({'message': user, 'send': 'info-chat'})
                              wx.MessageBox(_("Your request send to your friend"),_('Information'), wx.OK | wx.ICON_INFORMATION)                                  
                   dlg.Destroy()
        dlg.Destroy()
    def __init__(self, parent, id, title,user,un):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, wx.Size(210, 450))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, -1)
        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1, -1),
                                wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, lambda evt,un=un : self.OnClickLeftKey(evt,un), self.tree)
        root = self.tree.AddRoot('My friend')
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        gra     = il.Add(wx.Image("user.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        grb     = il.Add(wx.Image("group.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.tree.SetImageList(il)
        self.tree.AssignImageList(il)
        self.il = il
        for i in user['item']:
                ch=self.tree.AppendItem(root, i)
                self.tree.SetItemImage(ch,grb , which = wx.TreeItemIcon_Normal)
                for j in user[i]:
                        gr=self.tree.AppendItem(ch, j)
                        self.tree.SetItemImage(gr,gra , which = wx.TreeItemIcon_Normal)
        global un_g
        un_g = un
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, lambda evt,un=un : self.OnClose(evt,un), m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_friend = menu.Append(wx.ID_NEW, "&Add Friend", "Meet your friend")
        menuBar.Append(menu, "&Option")
        self.Bind(wx.EVT_MENU, self.AddFriend, m_friend)
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        #self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Center()
        self.Bind(wx.EVT_CLOSE, lambda evt,un=un : self.OnClose(evt,un))
        toaster = TB.ToasterBox(self, tbstyle=TB.TB_COMPLEX)
        toaster.SetPopupPauseTime(3000)
        tbpanel = toaster.GetToasterBoxWindow()
        panel = wx.Panel(tbpanel, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(panel, wx.ID_ANY, label="Welcome \n My friend " + un + "\n Nice to meet you")
        sizer.Add(text, 0, wx.EXPAND)
        panel.SetSizer(sizer)
        toaster.AddPanel(panel)
        wx.CallLater(100, toaster.Play)
        thread.start_new_thread(self.receive, ())
    def putinfo(self,data):
        global text_json
        text_json= json.loads(data['message'])
        if text_json['type'] == 'info-in-line': 
           toaster = TB.ToasterBox(self, tbstyle=TB.TB_COMPLEX)
           wx.CallAfter(toaster.SetPopupPauseTime,3000)
           tbpanel = toaster.GetToasterBoxWindow()
           panel = wx.Panel(tbpanel,-1)
           sizer = wx.BoxSizer(wx.VERTICAL)
           text = wx.StaticText(panel, wx.ID_ANY, label=text_json['send'] + " say: \n " + text_json['content'])
           wx.CallAfter(sizer.Add,text, 0, wx.EXPAND)
           button = wx.Button(panel, wx.ID_ANY, "Click to view")
           wx.CallAfter(sizer.Add,button, 0, wx.EXPAND)
           wx.CallAfter(button.Bind,wx.EVT_BUTTON,default_cb)
           wx.CallAfter(panel.SetSizer,sizer)
           wx.CallAfter(toaster.AddPanel,panel)
           time.sleep (1)
           wx.CallAfter(toaster.Play)
           time.sleep (1)
        if text_json['type'] == 'add-friend':
           toaster = TB.ToasterBox(self, tbstyle=TB.TB_COMPLEX)
           wx.CallAfter(toaster.SetPopupPauseTime,3000)
           tbpanel = toaster.GetToasterBoxWindow()
           panel = wx.Panel(tbpanel,-1)
           sizer = wx.BoxSizer(wx.VERTICAL)
           text = wx.StaticText(panel, wx.ID_ANY, label=text_json['user'])
           wx.CallAfter(sizer.Add,text, 0, wx.EXPAND)
           button = wx.Button(panel, wx.ID_ANY, "I agree")
           wx.CallAfter(sizer.Add,button, 0, wx.EXPAND)
           #wx.CallAfter(button.Bind,wx.EVT_BUTTON,default_cb)
           wx.CallAfter(panel.SetSizer,sizer)
           wx.CallAfter(toaster.AddPanel,panel)
           time.sleep (1)
           wx.CallAfter(toaster.Play)
           time.sleep (1)            
    def put_info(self,data):
        wx.CallAfter(self.putinfo,data=data)
    def receive(self):
        connection = pymongo.MongoClient('mongodb://tyl:22842218@ds051738.mongolab.com:51738/tylchat?authMechanism=SCRAM-SHA-1').get_default_database()
        if un_g not in connection.collection_names():
            connection.create_collection(un_g,
                                                    capped=True,
                                                    size=1000000,
                                                    max=None) 
        i = 1
        while (i == 1):
            subscriber = Subscriber(connection, un_g,callback=self.put_info ,
                        matching={'send': 'info-chat'})
            subscriber.listen()
