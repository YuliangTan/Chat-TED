# -*- coding: UTF-8 -*-
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
    def __init__(self, parent, id,title,user_name,un,addcon):
        wx.Frame.__init__(self,parent,id,title,wx.DefaultPosition,wx.Size(400,300))
        global username
        username=user_name
        self.bkg = wx.Panel(self,-1)
        global un_g
        un_g=un
        self.tshow = wx.TextCtrl(self.bkg,style = wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        self.tinput = wx.TextCtrl(self.bkg)
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
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.bt.Bind(wx.EVT_BUTTON,self.btaction)        
        thread.start_new_thread(self.receive, ())
        self.Show()
    def btaction(self,evt):
        now = datetime.datetime.now()
        self.tshow.SetDefaultStyle(wx.TextAttr("GREEN"))
        self.tshow.AppendText(_("I:")+now.strftime('%Y-%m-%d %H:%M:%S')+"\n")
        self.tshow.SetDefaultStyle(wx.TextAttr("BLACK"))
        self.tshow.AppendText(self.tinput.GetValue() + "\n")
        global content
        content = self.tinput.GetValue()
        thread.start_new_thread(self.send, ())
        self.tinput.SetValue("")
    def put_text(self,data): 
               text_json= json.loads(data['message'])
               if text_json['type'] == 'p2pchat-in-line':
                           now = datetime.datetime.now()
                           self.tshow.SetDefaultStyle(wx.TextAttr("BLUE"))
                           wx.CallAfter(self.tshow.AppendText, _("User:")+now.strftime('%Y-%m-%d %H:%M:%S')+"\n")
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
                      matching={'send': un_g})
             subscriber.listen()
    def send(self): 
        connection = pymongo.MongoClient('mongodb://tyl:22842218@ds051738.mongolab.com:51738/tylchat?authMechanism=SCRAM-SHA-1').get_default_database()
        #database = connection.tylchat_collection.pubsub_db
        publisher = Publisher(connection, username)
        try:
            s = urllib2.urlopen("http://chat-tyl.coding.io/read_cache.php?name="+ username + "-" + un_g +"&del=NO&check=OK").read()
        except urllib2.HTTPError,e:
           print e.code
        if s == "":
             send_dic = {
             'type': 'info-in-line',
             'send': un_g,
             'user' : username,
             'content': content 
             }
             user = json.dumps(send_dic)
             publisher.push({'message': user, 'send': 'info-chat'})
        else:
             send_dic = {
             'type': 'p2pchat-in-line',
             'content': content 
             }
             user = json.dumps(send_dic)
             publisher.push({'message': user, 'send': username})          
#if __name__ == '__main__':
    #app = myapp()
    #app.MainLoop()