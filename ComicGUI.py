'''
general purpose comic GUI for reading comics off of a variety of websites. Started with pcomix, hbox and ge hentai .org

Will load comics from pcomix and have a variety of menu bars/label texts

Must use grid to make this look better

Added tool to fetch from hentaibox as well. Improved the gui to have zoom in and out buttons. Also added next page and prev page by clicking on canvas. Must improve the 
scrollbars in this tho. They are way too small.

Added dl links through multiprocessing from hbox

Added Zoom and unzoom buttons. Still quite gimicky. Using globimg to prevent garbage collection but this means the previous image zoomed remains on the canvas when a new image is loaded.
Must change this but idk how right now. Maybe auto zoom out and in once when a new image is clicked once? SUper inelegant and might slow it down but would work.

Added manga reader from g.e.hentai .org

Added page numbers and converted ge hentai org to be class based

Must add dl function from gehentai as well

To speed up added threading where the next comic to the chosen one in ge hentai is automatically dowwnloaded concurrently into a cache. Could do it for all.
'''


from pcomix import *
from gehentaiCLASS import *
from tkinter import *
import tkinter
from PIL import Image,ImageTk
from io import BytesIO
import requests
from Hbox import *
import multiprocessing
import os
import random
from operator import add
from multiprocessing.pool import ThreadPool



class ComicGui():

    def __init__(self, master):
        self.window = master

        self.window.title('Comic Reader')
        self.window.geometry('500x500')
        self.window.wm_iconbitmap('fleurdelys label.ico')

        self.ControlFrame = tkinter.Frame(window)
        self.ControlFrame.place(height=1200, width=3200)

        self.LoadTitleButton = tkinter.Button(self.ControlFrame, text='Populate Titles', command=self.LoadTitle)      #Clicking this button will populate the title list with all the titles
        self.LoadTitleButton.pack()

        self.keywordEntry = tkinter.Entry(self.ControlFrame)           #Entry box to enter root keyword
        self.keywordEntry.pack()

        self.GuiTitleList = tkinter.Listbox(self.ControlFrame, width=100, height=15)         # title list that will hold all the titles of the comics
        self.GuiTitleList.bind("<ButtonRelease-1>", self.OnSingle)
        self.GuiTitleList.pack()

        self.ComicPages = tkinter.Listbox(self.ControlFrame, width=80)
        self.ComicPages.bind("<ButtonRelease-1>", self.OnDouble)
        self.ComicPages.pack()

        self.DownloadButton = tkinter.Button(self.ControlFrame, text='D O W N L O A D', command=self.GuiDownloadHandler)  #Clicking this button will go to next page of comic
        self.DownloadButton.pack()

        self.ZoomInButton = tkinter.Button(self.ControlFrame, text='+', command=self.ZoomIn)  #Clicking this button will go to next page of comic
        self.ZoomInButton.pack()

        self.ZoomOutButton = tkinter.Button(self.ControlFrame, text='-', command=self.ZoomOut)  #Clicking this button will go to next page of comic
        self.ZoomOutButton.pack()

        self.PgDescrip = StringVar()
        self.PageInfoLabel = tkinter.Label(self.ControlFrame, textvariable=self.PgDescrip)
        self.PageInfoLabel.pack()
        self.PgDescrip.set('No Comic has been chosen yet')

        self.CurPgDescr = StringVar()
        self.CurrentPgLabel = tkinter.Label(self.ControlFrame, textvariable=self.CurPgDescr)
        self.CurrentPgLabel.pack()
        self.CurPgDescr.set('')

        self.CurComicStr = StringVar()
        self.CurrentComiclabel = tkinter.Label(self.ControlFrame, textvariable=self.CurComicStr)
        self.CurrentComiclabel.pack()
        self.CurComicStr.set('')

        self.hbar=Scrollbar(window, orient=HORIZONTAL)
        self.hbar.grid(row=2, column=0)


        self.vbar=Scrollbar(window, orient=VERTICAL)
        self.vbar.grid(row=0, column=1)

        self.cv = tkinter.Canvas(window,bg='black',scrollregion=(0,0,2000,2000), width=1200, height=1000, xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.cv.bind("<Button-1>", self.LoadNextPageEvent)
        self.cv.bind("<Button-3>", self.LoadPrevPageEvent)
        self.cv.grid(row=0, column=0)

        self.hbar.config(command=self.cv.xview)
        self.vbar.config(command=self.cv.yview)

        #Setting a random image from naruto imagefap folder to be the front page of canvas
        path = 'C:\Python27\GUI\Jaymarvel'

        ImgFapList = os.listdir(path)

        RandomNum = random.randint(0,len(ImgFapList))

        RandomImgName = str(ImgFapList[RandomNum])

        os.chdir(path)

        self.img = Image.open(RandomImgName)

        self.photo = ImageTk.PhotoImage(self.img)

        self.MyCanvas = self.cv.create_image(10, 10, image=self.photo, anchor='nw')

        #Zoom stuff
        self.smallCounter = 0
        self.biggerCounter = 0

        #Threadstuff
        self.pool = ThreadPool(processes=1)
        self.SelectedComicPages = []            #this is the current comic list which has all the img links in it
        self.NextComicImgLinks = []             #this is the next comic in the list with all its img links in it
        self.CurrentTitleURL = ''                    #This is current comic url
        self.NextTitleURL = ''                #This is next comic url

        self.TitlesCached = []                  #These are all the titles already downloaded into cache
        self.TitlesToDownload = []              #These are the titles that are yet to be downloaded

        self.TotalTitleLinks = []               #This will have smaller lists inside which will each hold separate comic titles


    def LoadTitle(self):
        '''
        Button function which will fetch all the titles from specified site
        '''
        self.EnteredKeyWord = self.keywordEntry.get()
        #Deleting prvious pages from the list
        self.GuiTitleList.delete(0,END)

        if '!tag' in self.EnteredKeyWord:
            '''
            For hbox titles
            '''
            self.TitleList = FetchTaggedHBOXTitles(self.EnteredKeyWord[5:])
            self.InsertIntoList( self.GuiTitleList, 0, self.TitleList)

        elif '!search' in self.EnteredKeyWord:
            '''
            For hbox titles
            '''
            self.TitleList = FetchSearchedHBOXTitles(self.EnteredKeyWord[8:])
            self.InsertIntoList( self.GuiTitleList, 0, self.TitleList)

        elif '!series' in self.EnteredKeyWord:
            '''
            For Hbox titles
            '''
            self.TitleList = FetchSeriesHBOXTitles(self.EnteredKeyWord[8:])
            self.InsertIntoList( self.GuiTitleList, 0, self.TitleList)

        elif '$GE' in self.EnteredKeyWord:
            '''
            For GE hentai.org
            '''
            keyword = self.EnteredKeyWord[self.EnteredKeyWord.index('$GE')+4:self.EnteredKeyWord.index(':')-1]
            stars = int(self.EnteredKeyWord[self.EnteredKeyWord.index(':')+1:])
            gh = geHENTAI(keyword, stars)

            self.TupleList = gh.GetTitles()
            self.TitleList = list(map(add, self.TupleList[0], self.TupleList[1]))

            self.InsertIntoList( self.GuiTitleList, 0, self.TitleList)

        else:
            '''
            For pcomix
            '''    
            self.TitleList = FindTitles(self.EnteredKeyWord)
            self.InsertIntoList( self.GuiTitleList, 0, self.TitleList)

    def InsertIntoList(self, FuncListbox, counter, FuncArray):
        '''
        This function accepts listbox from gui and a array and inserts them chronologically into the listbox
        '''

        while counter<len(FuncArray):
            FuncListbox.insert(counter, FuncArray[counter])
            counter+=1

        FuncListbox.pack()


    def OnSingle(self, event):
        '''
        Function to handle event whenever someone clicks and lets go of item on title list
        '''
        #Section to get the highlighted text on the list- 
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])

        if '!search' in self.EnteredKeyWord or '!tag' in self.EnteredKeyWord or '!series' in self.EnteredKeyWord:
            '''
            This is for hbox tags
            '''
            self.SelectedComicPages = FetchImageLinks(value)
            self.Total_Comic_Pg_Num = len(self.SelectedComicPages)

            #Deleting prvious pages from the list
            self.ComicPages.delete(0,END)

            self.InsertIntoList(self.ComicPages, 0, self.SelectedComicPages)
            #Setting the selection to be the first automatically
            self.ComicPages.selection_set(0,0)
            #loading first page of comic automatically
            self.AutoLoadFirstPageComic()

        elif '$GE' in self.EnteredKeyWord:
            '''
            This is for g.e.hentai.org tags
            '''
            
            #Removing the name part from title by using the triple $$$ signs and getting the title url
            self.CurrentTitleURL = value[value.index('$$$')+4:]
            self.CurComicStr.set(value[0:value.index('$$$')])

            if self.CurrentTitleURL!=self.NextTitleURL:
                '''
                this means the user has not chosen the next comic in the list but a random one
                '''
                #The next title to the chosen one
                NextValue = widget.get(selection[0]+1)
                self.NextTitleURL = NextValue[NextValue.index('$$$')+4:]

                self.ComObj = Comic(self.CurrentTitleURL)
                #fetching all the img links this comic has
                self.SelectedComicPages = self.ComObj.GetImageLinks()
                #Finding how many pages this comic has
                self.Total_Comic_Pg_Num = len(self.SelectedComicPages)
                #Setting this to the label which will show page description
                self.PgDescrip.set('Pages: '+str(self.Total_Comic_Pg_Num))

                #Deleting prvious pages from the list
                self.ComicPages.delete(0,END)

                self.InsertIntoList(self.ComicPages, 0, self.SelectedComicPages)
                #Setting the selection to be the first automatically
                self.ComicPages.selection_set(0,0)
                #loading first page of comic automatically
                self.AutoLoadFirstPageComic()

                #---------------------Section to start the threading to fect comic images from next title concurrently-----------------------#
                self.async_result = self.pool.apply_async(self.ThreadComic )
                

            elif self.CurrentTitleURL==self.NextTitleURL:
                '''
                this means the user has chosen the next comic in the list so can be loaded from memory instead of fetching it
                '''
                NextValue = widget.get(selection[0]+1)
                self.NextTitleURL = NextValue[NextValue.index('$$$')+4:]

                #fetching it from the stored concurrent process started b4
                self.NextComicImgLinks = self.async_result.get()
                #fetching all the img links this comic has
                self.SelectedComicPages = self.NextComicImgLinks
                #Finding how many pages this comic has
                self.Total_Comic_Pg_Num = len(self.SelectedComicPages)
                #Setting this to the label which will show page description
                self.PgDescrip.set('Pages: '+str(self.Total_Comic_Pg_Num))

                #Deleting prvious pages from the list
                self.ComicPages.delete(0,END)

                self.InsertIntoList(self.ComicPages, 0, self.SelectedComicPages)
                #Setting the selection to be the first automatically
                self.ComicPages.selection_set(0,0)
                #loading first page of comic automatically
                self.AutoLoadFirstPageComic()

                #---------------------Section to start the threading to fect comic images from next title concurrently-----------------------#
                self.async_result = self.pool.apply_async(self.ThreadComic)


        else:
            '''
            This is for pcomix tags
            '''

            self.SelectedComicPages = ReturnImgSources(value)
            self.Total_Comic_Pg_Num = len(self.SelectedComicPages)

            self.TotalPages = len(self.SelectedComicPages)
            self.PgDescrip.set('Pages: '+str(self.TotalPages))  #setting total page label
            #Deleting prvious pages from the list
            self.ComicPages.delete(0,END)

            self.InsertIntoList(self.ComicPages, 0, self.SelectedComicPages)
            #Setting the selection to be the first automatically
            self.ComicPages.selection_set(0,0)
            #loading first page of comic automatically
            self.AutoLoadFirstPageComic()

    def AutoLoadFirstPageComic(self):
        #Setting the current page description to 1
        self.PageCounter = 1
        self.CurPgDescr.set(str(self.PageCounter))

        self.PageSelected = self.ComicPages.get(0)

        self.ImgDimensions = getImgSize(self.PageSelected)

        self.ImgWidth = self.ImgDimensions[0]
        self.ImgHeight = self.ImgDimensions[1]

        self.response = requests.get(self.PageSelected)

        #calling the function to place respone.content onto the canvas
        self.Place_ImageContent_2Canvas(self.response.content)

    def Place_ImageContent_2Canvas(self, content):
        '''
        This will accept a img url response content and convert it into a PIL object and place it onto the canvas
        '''

        self.img = Image.open(BytesIO(content))
        self.GlobImg = self.img
        self.photo = ImageTk.PhotoImage(self.img)

        self.MyCanvas = self.cv.create_image(10, 10, image=self.photo, anchor='nw')


    def LoadNextPageEvent(self, event):
        '''
        This will load the next item on the list and set the cursor selection to the next item as well
        '''
        itemSelected = self.ComicPages.curselection()
        value = self.ComicPages.get(itemSelected[0]+1)

        self.ComicPages.selection_set(itemSelected[0]+1)
        self.ComicPages.selection_clear(itemSelected[0])

        if 'http' in value:
            #Setting the label to current page number
            self.PageCounter+=1
            self.CurPgDescr.set(str(self.PageCounter))

            self.response = requests.get(value)
            #Placing the image onto canvas
            self.Place_ImageContent_2Canvas(self.response.content)

        else:
            '''
            If the list gets to the bottom, this will make it restart at the top again
            '''
            #Setting the label to 1 as it reset to top
            self.PageCounter=1
            self.CurPgDescr.set(str(self.PageCounter))

            self.ComicPages.selection_set(0,0)
            itemSelected = self.ComicPages.curselection()
            value = self.ComicPages.get(itemSelected[0])

            self.response = requests.get(value)
            #Placing the image onto canvas
            self.Place_ImageContent_2Canvas(self.response.content)


    def LoadPrevPageEvent(self, event):
        '''
        Button function to go to the prev item in the list
        '''
        itemSelected = self.ComicPages.curselection()
        value = self.ComicPages.get(itemSelected[0]-1)

        self.ComicPages.selection_set(itemSelected[0]-1)
        self.ComicPages.selection_clear(itemSelected[0])

        if 'http' in value:
            #Setting the label to current page number
            self.PageCounter-=1
            self.CurPgDescr.set(str(self.PageCounter))

            self.response = requests.get(value)
            #Placing the image onto canvas
            self.Place_ImageContent_2Canvas(self.response.content)

        else:
            '''
            If prev item is first item, reset to bottom
            '''
            #Setting the label to current page number
            self.PageCounter = int(self.Total_Comic_Pg_Num)
            self.CurPgDescr.set(str(self.PageCounter))

            self.ComicPages.selection_set(self.PageCounter-1)
            itemSelected = self.ComicPages.curselection()
            value = self.ComicPages.get(itemSelected[0])

            self.response = requests.get(value)
            #Placing the image onto canvas
            self.Place_ImageContent_2Canvas(self.response.content)


    def OnDouble(self, event):
        '''
        Function to handle event whenever someone clicks and lets go of item on comic list
        '''
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])

        #Finding what the chosen link page is

        if '$GE' in self.EnteredKeyWord:
            '''
            This will change the page number labels based on GE libraries
            '''
            try:
                self.pgNum = int(self.ComObj.GetIndexBasedOnPageLink(value))+1
            except:
                self.pgNum = int(self.NextComicImgLinks.index(value))+1

        elif '!search' in self.EnteredKeyWord or '!tag' in self.EnteredKeyWord or '!series' in self.EnteredKeyWord:
            self.pgNum = int(len(self.SelectedComicPages))+1
    
        else:
            '''For pcomix branch'''
            self.pgNum = int(self.TotalPages)+1


        self.CurPgDescr.set(str(self.pgNum))
        self.PageCounter = self.pgNum

        self.ImgDimensions = getImgSize(value)

        self.ImgWidth = self.ImgDimensions[0]
        self.ImgHeight = self.ImgDimensions[1]
        
        self.response = requests.get(value)
        #Placing the image onto canvas
        self.Place_ImageContent_2Canvas(self.response.content)

    def GuiDownloadHandler(self):
        itemSelected = self.ComicPages.curselection()
        value = self.ComicPages.get(itemSelected[0])

        new = value.split('/' , 7)

        sub = new[5]
        FinalURL = next((s for s in self.TitleList if sub in s), None) 
        DownloadComic(FinalURL) #This function will start a multiprocess to download the comic concurrently  


    def ZoomIn(self):
        self.biggerCounter+=1
        self.smallCounter-=1

        self.scaleFactor = (self.biggerCounter/20)+1
        self.img = self.GlobImg
        print ('resizing img by increasing '+str(self.scaleFactor))

        try:
            self.img = self.img.resize((round(self.ImgWidth*self.scaleFactor),round(self.ImgHeight*self.scaleFactor)), Image.ANTIALIAS)
        except ValueError:
            self.img = self.img.resize(self.ImgWidth,self.ImgHeight, Image.ANTIALIAS)

        self.GlobImg = self.img
        self.newphoto = ImageTk.PhotoImage(self.img)
        self.cv.itemconfig(self.MyCanvas, image=self.newphoto)



    def ZoomOut(self):
        self.smallCounter+=1
        self.biggerCounter-=1
        self.scaleFactor = (self.smallCounter/20)+1
        self.img = self.GlobImg
        print ('resizing img by decreasing by '+str(self.scaleFactor))
        try:
            self.img = self.img.resize((round(self.ImgWidth/self.scaleFactor),round(self.ImgHeight/self.scaleFactor)), Image.ANTIALIAS)
        except ValueError:
            self.img = self.img.resize(self.ImgWidth,self.ImgHeight, Image.ANTIALIAS)

        self.newphoto = ImageTk.PhotoImage(self.img)
        self.cv.itemconfig(self.MyCanvas, image=self.newphoto)

    def ThreadComic(self):
        '''
        Concurrent function to crawl the website and keep extracting img urls from nearest titles in the background
        '''
        print ('Starting thread....')
        MyComic = Comic(self.NextTitleURL)
        ImgLinks = MyComic.GetImageLinks()
        print ('Finished Concurrent thread...')
        return ImgLinks


def DownloadComic(FinalURL):
    '''
    Outside class handler to start parallel download process
    '''
    print ('Starting parallel download process..')
    p = multiprocessing.Process(target=MultiprocessDL, args=(FinalURL,))
    p.start()


def MultiprocessDL(FinalURL):  
    '''
    Calls the function to download a url
    '''
    DownloadSelectedComic(str(FinalURL))

def getImgSize(Func_url):
    '''
    This function accepts a image url and returns the dimensions of it
    '''

    RANGE = 5000
   
    req  = requests.get(Func_url,headers={'User-Agent':'Mozilla5.0(Google spider)','Range':'bytes=0-{}'.format(RANGE)})
    im = Image.open(BytesIO(req.content))

    return im.size







if __name__ == '__main__':
    window = tkinter.Tk()
    My_GUI = ComicGui(window)
    window.mainloop()
