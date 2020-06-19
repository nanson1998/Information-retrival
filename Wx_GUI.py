import wx
import codecs
import IR 
import crawl

path = './Data/'

def GetTitle_name(file):
    file = codecs.open(path + file, "r", "utf-8")
    content = file.read()
    file.close()
    for i in range(0, len(content)):
        if (content[i] == "\n"):
            return content[:i-2]       

def GetTitle_content(file):
    file = codecs.open(path + file, "r", "utf-8")
    content = file.read()
    file.close()
    for i in range(0, len(content)):
        if (content[i] == "."):
            return content[:i]         
def GetContent(file):
    for i in range(len(file), 0):
        if (file[i] == "/"):
            return file[i + 1:]


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
    	panel = wx.Panel(self)

    	Font_TitleLable = wx.Font(50, wx.ROMAN, wx.ITALIC, wx.NORMAL)

    	self.TitleLable = wx.StaticText(panel, -1, "       Tìm kiếm dữ liệu     ", pos=(190, 20))
    	self.TitleLable.SetFont(Font_TitleLable)

    	self.Query_Label = wx.StaticText(panel, -1, "Nhập thông tin", pos=(70, 130))
    	self.Query_TextBox = wx.TextCtrl(panel, pos=(150, 120), size=(1000, 30))

    	self.Content_TextBox = wx.ListBox(panel, pos=(650, 230), size=(500, 400), style = wx.TE_MULTILINE)

    	Radiobox_list = ['Cosine', 'Distance']
    	self.Radiobox = wx.RadioBox(panel, label = 'Tìm Kiếm bằng', pos = (170, 170), choices = Radiobox_list, majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
    	self.Radiobox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)


    	self.Document_Listbox = wx.ListBox(panel, pos = (50, 230),size = (550,400), choices = [], style = wx.LB_HSCROLL)
    	self.Document_Listbox.Bind(wx.EVT_LISTBOX, self.onListBox) 

    	self.Search_Button = wx.Button(panel, -1, "Tìm kiếm", pos =(340, 180))
    	self.Search_Button.Bind(wx.EVT_BUTTON, self.Click_SearchButton)

    	self.Exit_Button = wx.Button(panel,-1,"Thoát", pos = (1180, 600))
    	self.Exit_Button.Bind(wx.EVT_BUTTON, self.Click_ExitButton)

    	self.Crawl_Button = wx.Button(panel, -1, "Crawl", pos =(440, 180))
    	self.Crawl_Button.Bind(wx.EVT_BUTTON, self.Click_CrawlButton)

    	self.Stop_Crawl_Button = wx.Button(panel, -1, "Dừng crawl", pos =(540, 180))
    	self.Stop_Crawl_Button.Bind(wx.EVT_BUTTON, self.Click_CrawlButton)



    	self.SetSize((1335, 700))
    	self.SetTitle('IR')
    	self.Centre()

    def Click_ExitButton(self, e):
        self.Close()

    def Click_CrawlButton(self, e):
        crawl.start_crawl()

    
        
    def Click_SearchButton(self, e):
        if (self.Query_TextBox.GetValue() == ""):
            wx.MessageBox('Bạn chưa nhập query!', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            if (self.Radiobox.GetStringSelection() == "Cosine"):
                cosine = IR.listCosine(self.Query_TextBox.GetValue())
                list_file = list(cosine.keys())
                hot1 = list(cosine.keys())
                for i in range(0, len(list_file)):
                    if (ord(list_file[i][0]) >= 65 and ord(list_file[i][0]) <= 90):
                        list_file[i] = GetTitle_name(list_file[i]) 
                        hot1[i] = list_file[i]
                    else:
                        list_file[i] = GetTitle_content(list_file[i]) 
                        hot1[i] = list_file[i]
                self.Document_Listbox.Set(list_file)
                self.Content_TextBox.Set(hot1)

            elif (self.Radiobox.GetStringSelection() == "Distance"):
                distance = IR.listDistance(self.Query_TextBox.GetValue())
                list_file1 = list(distance.keys())
                hot = list(distance.keys())
                for i in range(0, len(list_file1)):
                    if (ord(list_file1[i][0]) >= 65 and ord(list_file1[i][0]) <= 90):
                        hot[i] = list_file1[i]
                        list_file1[i] = GetTitle_name(list_file1[i]) 
                       
                    else:
                        hot[i] = list_file1[i]
                        list_file1[i] = GetTitle_content(list_file1[i]) 
                       
                self.Document_Listbox.Set(list_file1)
                self.Content_TextBox.Set(hot)

    def onRadioBox(self,e):
     	print (self.Radiobox.GetStringSelection())
        
    def onListBox(self,e):
        file = ""
        temp = e.GetEventObject().GetStringSelection()
        i = len(temp) - 1 
        while i >= 0:
            if (temp[i] == "/"):
                file = temp[i+ 1:]
                break
            i = i - 1
                
        file = codecs.open(path + file, "r", "utf-8")
        text = file.read()
        self.Content_TextBox.SetLabel(text)
        file.close()
def main():

     app = wx.App()
     ex = Example(None)
     ex.Show()
     app.MainLoop()


if __name__ == '__main__':
    main()