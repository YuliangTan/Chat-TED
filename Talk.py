import wx
import datetime
class myapp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None,title="chatroom",pos = (100,50),size = (400,300))
        
        self.bkg = wx.Panel(frame)
        
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
        
        frame.Show(True)
        return True
    def btaction(self,evt):
        now = datetime.datetime.now()
        self.tshow.SetDefaultStyle(wx.TextAttr("GREEN"))
        self.tshow.AppendText("I:"+now.strftime('%Y-%m-%d %H:%M:%S')+"\n")
        self.tshow.SetDefaultStyle(wx.TextAttr("BLACK"))
        self.tshow.AppendText(self.tinput.GetValue() + "\n")
        self.tinput.SetValue("")
 
if __name__ == '__main__':
    app = myapp()
    app.MainLoop()