# -*- coding: UTF-8 -*-
import wx
import datetime
import redis
import thread
import simplejson as json
from time import sleep
class myapp(wx.App):
    def __init__(self,user_name,un):
        frame = wx.Frame(None,title="With " + user_name + " Talking",pos = (100,50),size = (400,300))
        global username
        username=user_name
        self.bkg = wx.Panel(frame)
        global un_g
        un_g=un
        self.tshow = wx.TextCtrl(self.bkg,style = wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        self.tinput = wx.TextCtrl(self.bkg)
        self.bt = wx.Button(self.bkg,label = "Send")      
        self.box1 = wx.BoxSizer()
        self.box1.Add(self.tinput,proportion = 1,flag = wx.EXPAND)
        self.box1.Add(self.bt,proportion = 0)        
        self.box2 = wx.BoxSizer(wx.VERTICAL)
        self.box2.Add(self.tshow,flag = wx.EXPAND|wx.ALL,border = 5,proportion = 1)     
        self.box2.Add(self.box1,flag = wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT\
        ,border = 5,proportion = 0)        
        self.bkg.SetSizer(self.box2)       
        self.bt.Bind(wx.EVT_BUTTON,self.btaction)        
        thread.start_new_thread(self.receive, ())
        frame.Show(True)
    def btaction(self,evt):
        now = datetime.datetime.now()
        self.tshow.SetDefaultStyle(wx.TextAttr("GREEN"))
        self.tshow.AppendText("I:"+now.strftime('%Y-%m-%d %H:%M:%S')+"\n")
        self.tshow.SetDefaultStyle(wx.TextAttr("BLACK"))
        self.tshow.AppendText(self.tinput.GetValue() + "\n")
        rc = redis.Redis(host='pub-redis-19834.us-east-1-4.5.ec2.garantiadata.com',port=19834,password='22842218')
        ps = rc.pubsub()
        ps.subscribe([username])
        send_dic = {
         'type': 'p2pchat-in-line',
         'user': username,
         'content': self.tinput.GetValue() 
       }
        user = json.dumps(send_dic)
        rc.publish(username, user)
        self.tinput.SetValue("")
    def receive(self):
       rd = redis.Redis(host='pub-redis-19834.us-east-1-4.5.ec2.garantiadata.com',port=19834,password='22842218')
       ps = rd.pubsub()
       #ps.subscribe(['test', 'user'])
       ps.subscribe([un_g])
       for item in ps.listen():
          if item['type'] == 'message':
               text_json= json.loads(item['data'])
               if text_json['type'] == 'p2pchat-in-line':
                   if text_json['user'] == un_g: 
                       now = datetime.datetime.now()
                       self.tshow.SetDefaultStyle(wx.TextAttr("BLUE"))
                       wx.CallAfter(self.tshow.AppendText, "User:"+now.strftime('%Y-%m-%d %H:%M:%S')+"\n")
                       sleep(0.1)
                       self.tshow.SetDefaultStyle(wx.TextAttr("BLACK"))
                       wx.CallAfter(self.tshow.AppendText, text_json['content'] + "\n")

#if __name__ == '__main__':
    #app = myapp()
    #app.MainLoop()