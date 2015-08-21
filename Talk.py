#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import wx
import datetime
import pymongo
from pymongo_pubsub import Publisher
from pymongo_pubsub import Subscriber
import thread
import simplejson as json
from time import sleep
import urllib2
class myapp(wx.Frame):
    def OnClose(self,evt):
       #re = redis.Redis(host='pub-redis-19834.us-east-1-4.5.ec2.garantiadata.com',port=19834,password='22842218')
       #re.delete(un_g + '-' + username)
       try:
           s = urllib2.urlopen("http://chat-tyl.coding.io/read_cache.php?name="+ un_g + "-" + username +"&del=OK&check=NO").read()
       except urllib2.HTTPError,e:
          print e.code
       self.Destroy()
    def OnFace(self, event):
        dlg = wx.SingleChoiceDialog(
                self, "What's your favorite langauge?", 'The Caption',
                ["�������䣭����", "�������ߣ�)  ��", "�������������", "�������������", "�����������������", "��������������","�ܣ����������","�⣨����������","�t�����������q","����������J","�𣨣������������","�⣨����������","�ᣨ����������","�r���s��t���q","�q���䨌�F���q���䨌�F���q���䨌�F���s","����������������������������","���������������������������������������","���s�F���䣩�s��ة��� ","�q�ɨr�����������q�ɨr","���p����������𣣣�������������","�����F���䣩���������æţ��УߩУ��� ","��( �����)��Ȧ�Ȧ�Ȧ�Ȧ����ڣ�����","��������","(#�F��)","���� c����y�y�� ","(��(��)��) ","( ��___��)y-�� ","��������������","�q(��??��)�r �z�~","<(��3��)>","��(>�ڣ�-)","<(�F����)>","o(���n��)o","�r(������\")�q ","��(._. )>","�R�بQ","O��O!","��-_-)��)����)","m(_ _)m","(�ѣ���) ","�� . �� ","�� ��|||| ","?~? ", "��?��","(T_T)  ","(/�F���)/"], 
                wx.CHOICEDLG_STYLE
                )
        if dlg.ShowModal() == wx.ID_OK: 
            self.tinput.AppendText(dlg.GetStringSelection() )
        dlg.Destroy()
    def __init__(self, parent, id,title,user_name,un,addcon):
        wx.Frame.__init__(self,parent,id,title,wx.DefaultPosition,wx.Size(400,300))
        global username
        username=user_name
        self.bkg = wx.Panel(self,-1)
        global un_g
        un_g=un
        self.tshow = wx.TextCtrl(self.bkg,style = wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY|wx.TE_RICH2|wx.TE_LINEWRAP)
        self.tinput = wx.TextCtrl(self.bkg,style = wx.TE_PROCESS_ENTER)
        self.tinput.Bind(wx.EVT_TEXT_ENTER,self.btaction)
        self.bt = wx.Button(self.bkg,label = _("Send"))      
        self.box1 = wx.BoxSizer()
        self.box1.Add(self.tinput,proportion = 1,flag = wx.EXPAND)
        self.box1.Add(self.bt,proportion = 0)        
        self.box2 = wx.BoxSizer(wx.VERTICAL)
        self.box2.Add(self.tshow,flag = wx.EXPAND|wx.ALL,border = 5,proportion = 1)     
        self.box2.Add(self.box1,flag = wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT\
        ,border = 5,proportion = 0)        
        self.bkg.SetSizer(self.box2)
        if addcon != "":
            now = datetime.datetime.now()
            self.tshow.SetDefaultStyle(wx.TextAttr("BLUE"))
            self.tshow.AppendText(_("User:")+now.strftime('%Y-%m-%d %H:%M:%S')+"\n")       
            self.tshow.SetDefaultStyle(wx.TextAttr("BLACK"))
            self.tshow.AppendText(addcon + "\n")
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        m_face = menu.Append(wx.ID_NEW, "&Face", "Many Face here")
        self.Bind(wx.EVT_MENU,self.OnClose, m_exit)
        self.Bind(wx.EVT_MENU,self.OnFace, m_face)
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.bt.Bind(wx.EVT_BUTTON,self.btaction)        
        thread.start_new_thread(self.receive, ())
        self.Show()
    def btaction(self,evt):
        global content
        content = self.tinput.GetValue()
        if content == "":
             wx.MessageBox(_('Please Enter the text'), _('Try it again'),
                     wx.OK | wx.ICON_ERROR)
        else:
            now = datetime.datetime.now()
            self.tshow.SetDefaultStyle(wx.TextAttr("GREEN"))
            self.tshow.AppendText(_("I:")+now.strftime('%Y-%m-%d %H:%M:%S')+"\n")
            self.tshow.SetDefaultStyle(wx.TextAttr("BLACK"))
            self.tshow.AppendText(self.tinput.GetValue() + "\n")
            thread.start_new_thread(self.send, ())
            self.tinput.SetValue("")
    def put_text(self,data): 
               text_json= json.loads(data['message'])
               if text_json['type'] == 'p2pchat-in-line':
                           now = datetime.datetime.now()
                           self.tshow.SetDefaultStyle(wx.TextAttr("BLUE"))
                           wx.CallAfter(self.tshow.AppendText, _("User:")+text_json['time']+"\n")
                           sleep(0.1)
                           self.tshow.SetDefaultStyle(wx.TextAttr("BLACK"))
                           wx.CallAfter(self.tshow.AppendText, text_json['content'] + "\n")
    def receive(self):
       try:
           s = urllib2.urlopen("http://chat-tyl.coding.io/read_cache.php?name="+ un_g + "-" + username +"&txt=OK&del=NO&check=NO").read()
       except urllib2.HTTPError,e:
          print e.code
       connection = pymongo.MongoClient('mongodb://tyl:22842218@ds051738.mongolab.com:51738/tylchat?authMechanism=SCRAM-SHA-1').get_default_database()
       i = 1
       while (i == 1):
             subscriber = Subscriber(connection, un_g,callback=self.put_text ,
                      matching={'send': username})
             subscriber.listen()
    def send(self): 
        connection = pymongo.MongoClient('mongodb://tyl:22842218@ds051738.mongolab.com:51738/tylchat?authMechanism=SCRAM-SHA-1').get_default_database()
        #database = connection.tylchat_collection.pubsub_db
        publisher = Publisher(connection, username)
        try:
            s = urllib2.urlopen("http://chat-tyl.coding.io/read_cache.php?name="+ username + "-" + un_g +"&del=NO&check=OK").read()
        except urllib2.HTTPError,e:
           print e.code
        now = datetime.datetime.now()
        if s == "":
             send_dic = {
             'type': 'info-in-line',
             'send': un_g,
             'user' : username,
             'time': now.strftime('%Y-%m-%d %H:%M:%S'),
             'content': content 
             }
             user = json.dumps(send_dic)
             publisher.push({'message': user, 'send': 'info-chat'})
        else:
             send_dic = {
             'type': 'p2pchat-in-line',
             'content': content ,
             'time': now.strftime('%Y-%m-%d %H:%M:%S')
             }
             user = json.dumps(send_dic)
             publisher.push({'message': user, 'send': un_g})          
#if __name__ == '__main__':
    #app = myapp()
    #app.MainLoop()