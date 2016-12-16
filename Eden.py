'''
Back-end server for the Eden project

Created 4/12/2016

Created to test multiple python concepts and frameworks including web scraping, web hosting thorugh flask, multiprocessing, etc

'''

from flask import Flask, render_template, request, url_for
import urllib
import urllib.request
from urllib.parse import urlparse
from random import randint
from bs4 import BeautifulSoup
import os
import multiprocessing
import shutil
import requests
from robobrowser import RoboBrowser
from collections import OrderedDict
import random

# Initialize the Flask application
app = Flask(__name__)

#Root URL which will host homepage
@app.route('/')
def Root():
    return render_template('EdenRoot.html')

#Update local directory with specified input comic from the site through multiprocess
@app.route('/UpdateFolder/<Name>')
def UpdateDownloadFolder(Name):
    Rooturls = []
    Rooturls = FindFrontPageLinks(Name)
    
    Counter=0
    while Counter<len(Rooturls):
        print ('spawning a process to download manga: '+str(Rooturls[Counter]))
        p = multiprocessing.Process(target=SingleDownloadProcess, args=(Rooturls[Counter],))
        p.start()
        Counter+=1
        
    return render_template('EdenRoot.html')  

#Supplement function for UpdateDownloadFolder
def FindFrontPageLinks(var1):
    
    if 'Straight-Shota' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Straight-Shota&related=&shownew=rating"
    elif 'Shota' in var1:
        BaseUrl = "http://www.hentaibox.net/?q=_Shota_&related=tags&most=tag"
    elif 'Lactation' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Lactation&related=&shownew=rating"
    elif 'Paizuri' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Paizuri&related=&shownew=rating"
    elif 'Sister' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Sister&related=&shownew=rating"
    elif 'Teacher' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Teacher&related=&shownew=rating"
    elif 'Naked-Apron' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Naked-Apron&related=&shownew=rating"
    elif 'Force' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Force&related=&shownew=rating"
    elif 'Elf' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Elf&related=&shownew=rating"
    elif 'Hairjob' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Hairjob&related=&shownew=rating"
    elif 'Hypnosis' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Hypnosis&related=&shownew=rating"
    elif 'Military-Uniform' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Military-Uniform&related=&shownew=rating"
    elif 'Reverse-Force' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Reverse-Force&related=&shownew=rating"
    elif 'Small-Penis' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Small-Penis&related=&shownew=rating"
    elif 'Stockings' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Stockings&related=&shownew=rating"
    elif 'Story-Arc' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=Story-Arc&related=&shownew=rating"
    elif 'Best' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=&related=&shownew=rating"
    elif 'Trending' in var1:
        BaseUrl = "http://my.hentaibox.net/?trending=manga"

    FrontPageURLS = []
    
    htmltextfile = urllib.request.urlopen(BaseUrl).read()
    
    Soup = BeautifulSoup(htmltextfile)
    
    AlltdTags = Soup.find_all('td',{'class':'search_gallery_item'})
    
    p=0
    while p<len(AlltdTags):
        print ('==============================================================')
        print ("ON ALLTDTAGS LIST NO. : " + str(p))
        Linktags = AlltdTags[p].find_all('a',href=True)
        
        for line in Linktags:
            if "hentai-manga" in line['href']:
                FrontPageURLS.append(line['href'])
                        
            print (line)
            print ('')
        
        p+=1
    
    print ('===========================================')
    print ("PRINTING ALL COLLECTED FRONT PAGE URLS: ")
    
    
    for q in FrontPageURLS:
        print (q)
        print ('')
        
    #NEED TO COMPARE ELEMENTS IN FRONTPAGEURL LIST WITH UPDATELOGLINES LIST
    #MATCHES GET REMOVED FROM FRONTPAGEURLS
    #NON MATCHES GET ADDED TO TEXT FILE UpdateLog.txt from FRONTPAGEURLS LIST
    
    NewFrontPageUrls = map(lambda a: str(a), FrontPageURLS)         #Converting list to have no 'u at start
    
    #Section to open text file to check if url is already in it
    with open('UpdateLog.txt') as f:
        UpdateLogLines = f.read().splitlines()     
    #-----------------------------------------------------------#
    Intersect = set(NewFrontPageUrls) & set(UpdateLogLines)

    for stuff in Intersect:
        print (stuff)
        NewFrontPageUrls.remove(stuff)
    
    f = open("UpdateLog.txt",'a')
    
    for item in NewFrontPageUrls:
        f.write(item+'\n')

    f.close()
    
    print ('')
    print ("The update to all relevant genres has finished...")
    print ('')
    return NewFrontPageUrls

#Supplement fucntion for UpdateDownloadFolder
def SingleDownloadProcess(ThisURL):
    ChoosePath = 0
    
    WebPageData = urllib.request.urlopen(ThisURL).read()
    SoupToFindTag = BeautifulSoup(WebPageData)
    
    AllDivData = SoupToFindTag.find_all('div',{'class':'pagination'})

    #Section to make custom path directory based on what value you get from genre
    for line in AllDivData:
        #print line.text
        if 'Straight-Shota' in line.text or 'Shotacon' in line.text:
            print ("THIS COMIC HAS TAG Str8-Shota IN IT")
            ChoosePath = 1
        elif 'Lactation' in line.text:
            print ("THIS COMIC HAS Lactation TAG")
            ChoosePath = 2
        elif 'Shota' in line.text:
            print ("THIS COMIC HAS shota TAG")
            ChoosePath = 3
        elif 'Sister' in line.text:
            print ("THIS COMIC HAS sister TAG")
            ChoosePath = 4
        elif 'Teacher' in line.text:
            print ("THIS COMIC HAS Teacher TAG")
            ChoosePath = 5
        elif 'Naked-Apron' in line.text:
            print ("THIS COMIC HAS Apron TAG")
            ChoosePath = 6
        elif 'Paizuri' in line.text:
            print ("THIS COMIC HAS Paizuri TAG")
            ChoosePath = 7
        elif 'Megane' in line.text:
            print ("THIS COMIC HAS Megane TAG")
            ChoosePath = 8
        elif 'Force' in line.text:
            print ("THIS COMIC HAS Force TAG")
            ChoosePath = 9
        elif 'Sister' in line.text:
            print ("THIS COMIC HAS Apron TAG")
            ChoosePath = 10
        elif 'Elf' in line.text:
            print ("THIS COMIC HAS elf TAG")
            ChoosePath = 11
        elif 'Hairjob' in line.text:
            print ("THIS COMIC HAS hairjob TAG")
            ChoosePath = 12
        elif 'Hypnosis' in line.text:
            print ("THIS COMIC HAS hypnosis TAG")
            ChoosePath = 13
        elif 'Military-Uniform' in line.text:
            print ("THIS COMIC HAS military uniform TAG")
            ChoosePath = 14
        elif 'Reverse-Force' in line.text:
            print ("THIS COMIC HAS reverse force TAG")
            ChoosePath = 15
        elif 'Story-Arc' in line.text:
            print ("THIS COMIC HAS story arc TAG")
            ChoosePath = 16
        elif 'Small-Penis' in line.text:
            print ("THIS COMIC HAS small penis TAG")
            ChoosePath = 17
        elif 'Stockings' in line.text:
            print ("THIS COMIC HAS stocking TAG")
            ChoosePath = 18
#====================================SECTION FOR FINDING TAG COMPLETE=========================================#
 
    url = ThisURL +'//'
    print ("STARTING Download from URL: "+str(url))
    print ("=====================================================================================")   

    #Creating the folder with name trunctated from the url itself
    if ChoosePath == 0:
        CreateNewpath = "C:\Python27\Images\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
        #print (CreateNewpath)
        newpath = CreateNewpath
    elif ChoosePath == 1:
        CreateNewpath = "C:\Python27\Images\Str8-Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
        #print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 2:
        CreateNewpath = "C:\Python27\Images\Lact\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 3:
        CreateNewpath = "C:\Python27\Images\Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
        #print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 4:
        CreateNewpath = "C:\Python27\Images\Sister\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
        #print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 5:
        CreateNewpath = "C:\Python27\Images\Teacher\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 6:
        CreateNewpath = "C:\Python27\Images\Apron\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
        #print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 7:
        CreateNewpath = "C:\Python27\Images\Paizuri\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 8:
        CreateNewpath = "C:\Python27\Images\Megane\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 9:
        CreateNewpath = "C:\Python27\Images\Force\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 10:
        CreateNewpath = "C:\Python27\Images\Sister\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 11:
        CreateNewpath = "C:\Python27\Images\Elf\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 12:
        CreateNewpath = "C:\Python27\Images\Hairjob\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 13:
        CreateNewpath = "C:\Python27\Images\Hypnosis\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 14:
        CreateNewpath = "C:\Python27\Images\Military\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 15:
        CreateNewpath = "C:\Python27\Images\Reverseforce\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 16:
        CreateNewpath = "C:\Python27\Images\Story\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 17:
        CreateNewpath = "C:\Python27\Images\Smallp\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 18:
        CreateNewpath = "C:\Python27\Images\Stocking\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    
    #--------------------if path doesnt exist then make it -------------------------------------#
    if not os.path.exists(newpath):
         os.makedirs(newpath)
    
    MyPath = newpath
    
    Name = 0
    urls = []               #This will have all the pages links of current comic
    

    
    
    #-----------Section to figure out how many pages this comic has--------------#
    String1 = url.replace('http://www.hentaibox.net/hentai-manga/','')
    IndexOfUnderscore = String1.index('_')
    NumberofPages = String1[0:IndexOfUnderscore]
    
    print ("Number of pages in current comic: " + str(NumberofPages))
    
    #Populaing urls with all the different web pages starting from 00 to NumberofPages
    t = 1
    while t<(int(NumberofPages)):
        if t>0 and t<10:
            var2 = url+str(t).zfill(2)
        elif t>9 and t<100:
            var2 = url+str(t).zfill(3)
        elif t>99 and t<1000:
            var2 = url+str(t).zfill(4)
        urls.append(var2)
        t+=1
        
    urls.pop(0)             #Getting rid of 00 element since it is same as 01
     
    #Opening each of the pages in urls and extracting image from them   
    p=0
    while p<len(urls):
        htmltext = urllib.request.urlopen(urls[p]).read()   
        soup = BeautifulSoup(htmltext)
    
        print ("")    
        AllImageLinks = soup.find_all('img',src=True)
        
        for q in AllImageLinks:
            if "ads-iframe" not in q['src'] and ".png" not in q['src']:
                #The name should be incremental from 0 to infinity with.jpg at end
                Full_name = str(Name) + ".jpg"
                
                urllib.request.urlretrieve(q['src'], os.path.join(MyPath, (Full_name)))
                print (q['src'])
                
        p+=1
        Name+=1                 #increasing name variable so name of file is increased
        
    print ("Finished Download of "+url.replace('http://www.hentaibox.net/hentai-manga/','')+ "Enjoy!")
   
    print ('')    
    print ("Finished updating. Thank you for waiting. Enjoy!")
    print ('')

#This downloads hcomics
@app.route('/DLcomics/',methods=['POST'])
def DLcomics():
    
    f = open("UpdateLog.txt",'a')
    Rooturls = []
    NumberofCommas = 0
    Mvar1 = request.form['ComicLink']
    print ("SUBMITTED STRING IS: "+str(Mvar1))
    
    #this section will find how many commas submitted text has and hence how many links there are
    for letter in Mvar1:
        if ',' in letter:
            NumberofCommas+=1
            print ("Found a comma")
            
    print ("NUMBER OF COMMAS FOUND: "+str(NumberofCommas))
    #This section places all the urls submitted through form into RootUrls        
    LoopCounter=0
    while LoopCounter<(NumberofCommas):
        print ("===============================")
        print ("MVAR1 at start of loop is: "+str(Mvar1))
        print ("On loop counter: "+str(LoopCounter))
        CommaIndex = Mvar1.index(',')
        LinkItself = Mvar1[0:CommaIndex]
        Rooturls.append(LinkItself)
        print ("Added to list root urls the link: "+str(LinkItself))
    
        RestofLink = Mvar1[CommaIndex+1:]
        Mvar1 = RestofLink
        print ("NEW MVAR1 is: "+str(Mvar1)+" For loop counter: "+str(LoopCounter))
    
        LoopCounter+=1
        
    Rooturls.append(Mvar1)
    #This section will compare rooturls to urls already in updatelog. If in it, it will make new list only with ones not in it. this new urls will be updated to the same text as well
    ThisPageUrls = map(lambda a: str(a), Rooturls)
    
    with open('UpdateLog.txt') as f:
        UpdateLogLines = f.read().splitlines()
    
    Intersect = set(ThisPageUrls) & set(UpdateLogLines)

    for stuff in Intersect:
        print (stuff)
        ThisPageUrls.remove(stuff)
    
    f = open("UpdateLog.txt",'a')
    
    print ("Printing everything in Rooturls list now:")    
    for item in ThisPageUrls:
        f.write(item+'\n')
        print ('spawning a process to download manga: '+str(item))
        p = multiprocessing.Process(target=SingleProcessBespokeDownload, args=(item,))
        p.start()
    #----------------SECTION TO CONVERT MULTIPLE LINKS INTO ROOTURLS LIST DONE-------------------------#    
    
    f.close()

    return render_template('EdenRoot.html')

#Supplement function for DLcomics    
def SingleProcessBespokeDownload(MyArg):
    ChoosePath = 0          #Variable used to identify what the saved path anme will be dependant on genre tag
    
    print ('')
    print ('THIS IS THE ARGUMENT PASSED INTO THIS FOR THIS PROCESS: '+str(MyArg))
    print ('')
    
    WebPageData = urllib.request.urlopen(MyArg).read()
    SoupToFindTag = BeautifulSoup(WebPageData,'html.parser')
    
    AllDivData = SoupToFindTag.find_all('div',{'class':'pagination'})

    #Section to make custom path directory based on what value you get from genre
    for line in AllDivData:
        #print line.text
        if 'Straight-Shota' in line.text or 'Shotacon' in line.text:
            #print ("THIS COMIC HAS TAG Str8-Shota IN IT")
            ChoosePath = 1
        elif 'Lactation' in line.text:
           # print ("THIS COMIC HAS Lactation TAG")
            ChoosePath = 2
        elif 'Shota' in line.text:
           # print ("THIS COMIC HAS shota TAG")
            ChoosePath = 3
        elif 'Sister' in line.text:
           # print ("THIS COMIC HAS sister TAG")
            ChoosePath = 4
        elif 'Teacher' in line.text:
           # print ("THIS COMIC HAS Teacher TAG")
            ChoosePath = 5
        elif 'Naked-Apron' in line.text:
           # print ("THIS COMIC HAS Apron TAG")
            ChoosePath = 6
        elif 'Paizuri' in line.text:
           # print ("THIS COMIC HAS Paizuri TAG")
            ChoosePath = 7
        elif 'Megane' in line.text:
           # print ("THIS COMIC HAS Megane TAG")
            ChoosePath = 8
        elif 'Force' in line.text:
           # print ("THIS COMIC HAS Force TAG")
            ChoosePath = 9
        elif 'Sister' in line.text:
          #  print ("THIS COMIC HAS Sister TAG")
            ChoosePath = 10
        elif 'Elf' in line.text:
          #  print ("THIS COMIC HAS elf TAG")
            ChoosePath = 11
        elif 'Hairjob' in line.text:
          #  print ("THIS COMIC HAS hairjob TAG")
            ChoosePath = 12
        elif 'Hypnosis' in line.text:
          #  print ("THIS COMIC HAS hypnosis TAG")
            ChoosePath = 13
        elif 'Military-Uniform' in line.text:
           # print ("THIS COMIC HAS military uniform TAG")
            ChoosePath = 14
        elif 'Reverse-Force' in line.text:
          #  print ("THIS COMIC HAS reverse force TAG")
            ChoosePath = 15
        elif 'Story-Arc' in line.text:
          #  print ("THIS COMIC HAS story arc TAG")
            ChoosePath = 16
        elif 'Small-Penis' in line.text:
          #  print ("THIS COMIC HAS small penis TAG")
            ChoosePath = 17
        elif 'Stockings' in line.text:
           # print ("THIS COMIC HAS stocking TAG")
            ChoosePath = 18
#====================================SECTION FOR FINDING TAG COMPLETE=========================================#
 
    url = MyArg +'//'
    print ("STARTING Download from URL: "+str(url))
    print ("=====================================================================================")   

    #Creating the folder with name trunctated from the url itself
    if ChoosePath == 0:
        CreateNewpath = "C:\Python27\Images\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 1:
        CreateNewpath = "C:\Python27\Images\Str8-Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 2:
        CreateNewpath = "C:\Python27\Images\Lact\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 3:
        CreateNewpath = "C:\Python27\Images\Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 4:
        CreateNewpath = "C:\Python27\Images\Sister\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 5:
        CreateNewpath = "C:\Python27\Images\Teacher\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 6:
        CreateNewpath = "C:\Python27\Images\Apron\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 7:
        CreateNewpath = "C:\Python27\Images\Paizuri\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 8:
        CreateNewpath = "C:\Python27\Images\Megane\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 9:
        CreateNewpath = "C:\Python27\Images\Force\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 10:
        CreateNewpath = "C:\Python27\Images\Sister\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
       # print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 11:
        CreateNewpath = "C:\Python27\Images\Elf\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 12:
        CreateNewpath = "C:\Python27\Images\Hairjob\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 13:
        CreateNewpath = "C:\Python27\Images\Hypnosis\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 14:
        CreateNewpath = "C:\Python27\Images\Military\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 15:
        CreateNewpath = "C:\Python27\Images\Reverseforce\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 16:
        CreateNewpath = "C:\Python27\Images\Story\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
     #   print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 17:
        CreateNewpath = "C:\Python27\Images\Smallp\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    elif ChoosePath == 18:
        CreateNewpath = "C:\Python27\Images\Stocking\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
      #  print CreateNewpath
        newpath = CreateNewpath
    
    #--------------------if path doesnt exist then make it -------------------------------------#
    if not os.path.exists(newpath):
         os.makedirs(newpath)
    
    MyPath = newpath
    
    Name = 0
    urls = []               #This will have all the pages links of current comic
    

    
    
    #-----------Section to figure out how many pages this comic has--------------#
    String1 = url.replace('http://www.hentaibox.net/hentai-manga/','')
    IndexOfUnderscore = String1.index('_')
    NumberofPages = String1[0:IndexOfUnderscore]
    
    print ("Number of pages in current comic: " + str(NumberofPages))
    
    #Populaing urls with all the different web pages starting from 00 to NumberofPages
    t = 1
    while t<(int(NumberofPages)):
        if t>0 and t<10:
            var2 = url+str(t).zfill(2)
        elif t>9 and t<100:
            var2 = url+str(t).zfill(3)
        elif t>99 and t<1000:
            var2 = url+str(t).zfill(4)
        urls.append(var2)
        t+=1
        
    urls.pop(0)             #Getting rid of 00 element since it is same as 01
     
    #Opening each of the pages in urls and extracting image from them   
    p=0
    while p<len(urls):
        htmltext = urllib.request.urlopen(urls[p]).read()   
        soup = BeautifulSoup(htmltext,'html.parser')
    
        print ("")    
        AllImageLinks = soup.find_all('img',src=True)
        
        for q in AllImageLinks:
            if "ads-iframe" not in q['src'] and ".png" not in q['src']:
                #The name should be incremental from 0 to infinity with.jpg at end
                Full_name = str(Name) + ".jpg"
                
                urllib.request.urlretrieve(q['src'], os.path.join(MyPath, (Full_name)))
                print (q['src'])
                
        p+=1
        Name+=1                 #increasing name variable so name of file is increased
        
    print ("Finished Download of "+url.replace('http://www.hentaibox.net/hentai-manga/','')+ "Enjoy!")

#Section for ImageFap
@app.route('/IFP/<RootKeyword>/<RootPageNum1>')
def ImageFapScraping(RootKeyword,RootPageNum1):
    
    RootPageNum = int(RootPageNum1)

    if (RootPageNum%5)==0:
        print ('Spawning 5 processes to concurrently solve this function.. ')
        
        #Divinding up the total number of pages into five so that 5 proceeses can parallely carry them out
        #Tests here are done with rootpagenum=25
        SmallerPageLimits = round(RootPageNum/5)                    # 5
        FinSmallerPageLimitStart1 = 0                               # 0
        FinSmallerPageLimit1 = RootPageNum-(SmallerPageLimits*4)  # 5  so 0 to 5
        
        FinSmallerPageLimitStartMid = FinSmallerPageLimit1+1        # 6
        FinSmallerPageLimitMid  = RootPageNum-(SmallerPageLimits*3)   # 10     
    
        FinSmallerPageLimitStart2 = FinSmallerPageLimitMid+1        # 11
        FinSmallerPageLimit2 = RootPageNum-(SmallerPageLimits*2)    # 15
        
        FinSmallerPageLimitStart3 = FinSmallerPageLimit2+1          # 16
        FinSmallerPageLimit3 = RootPageNum-(SmallerPageLimits)      # 20
        
        FinSmallerPageLimitEndStart = FinSmallerPageLimit3+1        # 21
        FinSmallerPageLimitEndEnd = RootPageNum                     # 25
        
        #Starting the multiprocess (FIVE OF THEM)
        thiscount = 0
        while thiscount<5:
            if thiscount==0:
                #print ('Starting page for first half: '+str(FinSmallerPageLimitStart1)+' ending page for first half: '+str(FinSmallerPageLimit1)
                p = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart1, FinSmallerPageLimit1, ))
                p.start()
            elif thiscount==1:
               # print 'Starting page for mid half: '+str(FinSmallerPageLimitStartMid)+' ending page for mid half: '+str(FinSmallerPageLimitMid)
                p2 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStartMid, FinSmallerPageLimitMid,  ))
                p2.start()
            elif thiscount==2:
                #print 'Starting page for second2nd to last half: '+str(FinSmallerPageLimitStart2)+' ending page for second2nd to last half: '+str(FinSmallerPageLimit2)
                p3 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart2, FinSmallerPageLimit2,  ))
                p3.start()
            elif thiscount==3:
               # print 'Starting page for second to last half: '+str(FinSmallerPageLimitStart3)+' ending page for second to last half: '+str(FinSmallerPageLimit3)
                p4 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart3, FinSmallerPageLimit3,  ))
                p4.start()
            elif thiscount==4:
                #print 'Starting page for last half: '+str(FinSmallerPageLimitEndStart)+' ending page for last half: '+str(FinSmallerPageLimitEndEnd)
                p5 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitEndStart, FinSmallerPageLimitEndEnd,  ))
                p5.start()
            thiscount+=1
        
        
    elif (RootPageNum%4)==0:
       # print 'Spawning 4 processes to concurrently solve this function.. '
        
        #Divinding up the total number of pages into four so that 4 proceeses can parallely carry them out
        #Tests here are done with rootpagenum=32
        SmallerPageLimits = round(RootPageNum/4)                    # 8
        FinSmallerPageLimitStart1 = 0                               # 0
        FinSmallerPageLimit1 = RootPageNum-(SmallerPageLimits*3)  # 8  so 0 to 8
        
        FinSmallerPageLimitStartMid = FinSmallerPageLimit1+1        # 9
        FinSmallerPageLimitMid  = RootPageNum-(SmallerPageLimits*2)   # 16     
    
        FinSmallerPageLimitStart2 = FinSmallerPageLimitMid+1        # 17
        FinSmallerPageLimit2 = RootPageNum-(SmallerPageLimits)      # 24
        
        FinSmallerPageLimitEndStart = FinSmallerPageLimit2+1        # 25
        FinSmallerPageLimitEndEnd = RootPageNum                     # 32
        
        #Starting the multiprocess (FOUR OF THEM)
        thiscount = 0
        while thiscount<4:
            if thiscount==0:
                #print 'Starting page for first half: '+str(FinSmallerPageLimitStart1)+' ending page for first half: '+str(FinSmallerPageLimit1)
                p = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart1, FinSmallerPageLimit1, ))
                p.start()
            elif thiscount==1:
               # print 'Starting page for mid half: '+str(FinSmallerPageLimitStartMid)+' ending page for mid half: '+str(FinSmallerPageLimitMid)
                p2 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStartMid, FinSmallerPageLimitMid,  ))
                p2.start()
            elif thiscount==2:
               # print 'Starting page for second to last half: '+str(FinSmallerPageLimitStart2)+' ending page for second to last half: '+str(FinSmallerPageLimit2)
                p3 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart2, FinSmallerPageLimit2,  ))
                p3.start()
            elif thiscount==3:
                #print 'Starting page for last half: '+str(FinSmallerPageLimitEndStart)+' ending page for last half: '+str(FinSmallerPageLimitEndEnd)
                p4 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitEndStart, FinSmallerPageLimitEndEnd,  ))
                p4.start()
            thiscount+=1
        
        
    elif (RootPageNum%3)==0:
        #print 'Spawning 3 processes to concurrently solve this function.. '
        
        #Divinding up the total number of pages into three so that 3 proceeses can parallely carry them out
        #Tests here are done with rootpagenum=9
        SmallerPageLimits = round(RootPageNum/3)                    # 3 
        FinSmallerPageLimitStart1 = 0                               # 0
        FinSmallerPageLimit1 = RootPageNum-(SmallerPageLimits*2)  # 3  so 0 to 3
        
        FinSmallerPageLimitStartMid = FinSmallerPageLimit1+1        # 4
        FinSmallerPageLimitMid  = RootPageNum-SmallerPageLimits   # 6     
    
        FinSmallerPageLimitStart2 = FinSmallerPageLimitMid+1        # 7
        FinSmallerPageLimit2 = RootPageNum
        
        #Starting the multiprocess (THREE OF THEM)
        thiscount = 0
        while thiscount<3:
            if thiscount==0:
                #print 'Starting page for first half: '+str(FinSmallerPageLimitStart1)+' ending page for first half: '+str(FinSmallerPageLimit1)
                p = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart1, FinSmallerPageLimit1, ))
                p.start()
            elif thiscount==1:
               # print 'Starting page for mid half: '+str(FinSmallerPageLimitStartMid)+' ending page for mid half: '+str(FinSmallerPageLimitMid)
                p2 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStartMid, FinSmallerPageLimitMid,  ))
                p2.start()
            elif thiscount==2:
               # print 'Starting page for last half: '+str(FinSmallerPageLimitStart2)+' ending page for last half: '+str(FinSmallerPageLimit2)
                p3 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart2, FinSmallerPageLimit2,  ))
                p3.start()
            thiscount+=1
        
        
    elif (RootPageNum%2)==0:
        #print 'Spawning 2 processes to concurrently solve this function.. '
        
        #Divinding up the total number of pages into two so that 2 proceeses can parallely carry them out
        SmallerPageLimits = round(RootPageNum/2)
        FinSmallerPageLimitStart1 = 0
        FinSmallerPageLimit1 = RootPageNum-SmallerPageLimits
    
        FinSmallerPageLimitStart2 = FinSmallerPageLimit1+1
        FinSmallerPageLimit2 = RootPageNum
        
        #Starting the multiprocess (TWO OF THEM)
        thiscount = 0
        while thiscount<2:
            if thiscount==0:
                #print 'Starting page for first half: '+str(FinSmallerPageLimitStart1)+' ending page for first half: '+str(FinSmallerPageLimit1)
                p = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart1, FinSmallerPageLimit1, ))
                p.start()
            elif thiscount==1:
                #print 'Starting page for second half: '+str(FinSmallerPageLimitStart2)+' ending page for second half: '+str(FinSmallerPageLimit2)
                p2 = multiprocessing.Process(target=SingleProcessOfDownloading, args=(RootKeyword, FinSmallerPageLimitStart2, FinSmallerPageLimit2,  ))
                p2.start()
            thiscount+=1
    return render_template('EdenRoot.html')

#A single process of downloading stuff
def SingleProcessOfDownloading(Keyword,PageLimitStart,PageLimitEnd):
   # print '==================================================================='
    #print 'Starting Process..'
    #print 'Starting from page no. '+str(PageLimitStart)+' |Ending at page no. '+str(PageLimitEnd)
 

    #Section to figure out how many pages this keyword in erolord has
    ArrayOfPages = []
    
    walao = PageLimitStart
    while walao<int(PageLimitEnd):
        thisvar = 'http://www.imagefap.com/gallery.php?search='+str(Keyword)+'&page=' + str(walao) + '&submitbutton=Search%21&filter_size=&filter_date='
        walao+=1
        ArrayOfPages.append(thisvar)
    
    for qq in ArrayOfPages:
        print (qq)
        
    GalleryTitleLinkTags = []    
    #Now we go to each of these front pages and get the links of each heading
    for waka in range(len(ArrayOfPages)):
        OpenHtml = urllib.request.urlopen(ArrayOfPages[waka]).read()
        soup1 = BeautifulSoup(OpenHtml,'html.parser')
        ThisLinkTag = soup1.find_all('a',{'class':'gal_title'},href=True)
        for werty in ThisLinkTag:
            if '/profile' not in werty['href']:
                try:
                    AddedWithDomain = 'http://www.imagefap.com' + werty['href'] + '&view=2'
                    GalleryTitleLinkTags.append(AddedWithDomain)
                except:
                    pass
            
    for stuff in GalleryTitleLinkTags:
        print (stuff)
        
    MegaImgLinkList = []
    #Now we have to go to each of these heading galleies and add each image page link to main pageurl list
    for cnt in range(len(GalleryTitleLinkTags)):
        htmlfile = urllib.request.urlopen(GalleryTitleLinkTags[cnt]).read()

        soup = BeautifulSoup(htmlfile,'html.parser')


        Linktag = soup.find_all('div',{'id':'gallery'})

        for line in Linktag:
            Atag = line.find_all('a',href=True)
            for z in Atag:
                print ('http://www.imagefap.com'+ z['href'])
                MegaImgLinkList.append('http://www.imagefap.com'+z['href'])

    
    for po in MegaImgLinkList:
        print (po)
    
    #Now we can start grabbing the img from each of these pages

    
    #First lets make the file directory to store these images
    CreateNewpath = "C:\Python27\Images\ImageFap\\"+str(Keyword)
    print ('Path to store images: '+CreateNewpath)
    newpath = CreateNewpath
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    MyPath = newpath                        #This is one half of where it will be stored, the name of file still has to be genrated with Name variable
    Name = 0
    
    # print ''
    # print 'Initialising Download of images'
    # print 'Initialising Download of images'
    # print 'Initialising Download of images'
    # print ''
    
    #Now to open each of these links and grab the image in them
    thing=0
    while thing<len(MegaImgLinkList):
        try:
            Name = random.randint(0,100000000000)
            NewHtml = urllib.request.urlopen(MegaImgLinkList[thing]).read()
            soup3 = BeautifulSoup(NewHtml,'html.parser')
            ImgTag = soup3.find_all('img',src=True)
            for line in ImgTag:
                if 'http://' in line['src'] and 'thumb' not in line['src'] and 'ip.gif' not in line['src']and 'xorigin.fap.to' not in line['src']:
                    print (line['src'])
                    if '.gif' in line['src']:
                        #The name should be incremental from 0 to infinity with.gif at end if it is a gif
                        Full_name = str(Name) + ".gif"
                    else:
                        #The name should be incremental from 0 to infinity with.jpg at end
                        Full_name = str(Name) + ".jpg"
                        
                    urllib.request.urlretrieve(line['src'], os.path.join(MyPath, (Full_name)))
        except:
            pass
        thing +=1

    
    print ('FINISHED DOWNLOADING ALL ENJOY')


#Downloading by series name
@app.route('/Hbox/<KeyWord>')
def HentaiBoxSearch(KeyWord):
    
    BaseUrl = 'http://www.hentaibox.net/?q='+str(KeyWord)
    print ('Starting search from url '+str(BaseUrl))
    UrlTitles = []                  #This will have the urls of all the titles
    CurrentUrl = []                 #This will have the frontpage of the keyword and more depending on next tag
    CurrentUrl.append(BaseUrl)
    
    MyCounter = 0
    while MyCounter<len(CurrentUrl):
        htmlfile = urllib.request.urlopen(CurrentUrl[MyCounter]).read()
        soup = BeautifulSoup(htmlfile, 'html.parser')
        LinkTag = soup.find_all('a',href=True)
    
        for link in LinkTag:            #Adding all found title links to our list
            if 'hentai-manga' in link['href']:
                print (link['href'])
                UrlTitles.append(link['href'])
            if 'Next' in link.text:
                CurrentUrl.append(link['href'])
        #print ('Length of current url before popping: '+str(len(CurrentUrl)))
        CurrentUrl.pop(0)
        #print 'Length of current url after popping: '+str(len(CurrentUrl))
            
    print ('printing all collected front page urls')    
    for wat in UrlTitles:
        print (wat)
        p = multiprocessing.Process(target=SingleProcessOfDownloadingBySearch, args=(wat,KeyWord,))
        p.start()
    return render_template('EdenRoot.html')

def SingleProcessOfDownloadingBySearch(MyVar1,MyVar2):
    
    url = MyVar1+'/'
    
    CreateNewpath = "C:\Python27\Images\Hbox\\"+str(MyVar2)+'\\'+url.replace('http://www.hentaibox.net/hentai-manga/','')
    print (CreateNewpath)
    newpath = CreateNewpath
    
    #--------------------if path doesnt exist then make it -------------------------------------#
    if not os.path.exists(newpath):
         os.makedirs(newpath)
    
    MyPath = newpath
    Name = 0
    urls = []               #This will have all the pages links of current comic
    
    #-----------Section to figure out how many pages this comic has--------------#
    String1 = url.replace('http://www.hentaibox.net/hentai-manga/','')
    IndexOfUnderscore = String1.index('_')
    NumberofPages = String1[0:IndexOfUnderscore]
    
    print ("Number of pages in current comic: " + str(NumberofPages))
    
    #Populaing urls with all the different web pages starting from 00 to NumberofPages
    t = 1
    while t<(int(NumberofPages)):
        if t>0 and t<10:
            var2 = url+str(t).zfill(2)
        elif t>9 and t<100:
            var2 = url+str(t).zfill(3)
        elif t>99 and t<1000:
            var2 = url+str(t).zfill(4)
        urls.append(var2)
        t+=1
        
    #urls.pop(0)             #Getting rid of 00 element since it is same as 01
    
     
    #Opening each of the pages in urls and extracting image from them   
    p=0
    while p<len(urls):
        htmltext = urllib.request.urlopen(urls[p]).read()   
        soup = BeautifulSoup(htmltext,'html.parser')
    
        print ("")    
        AllImageLinks = soup.find_all('img',src=True)
        
        for q in AllImageLinks:
            if "ads-iframe" not in q['src'] and ".png" not in q['src'] and 'search' not in q['src'] and '/hblr' not in q['src']:
                #The name should be incremental from 0 to infinity with.jpg at end
                Full_name = str(Name) + ".jpg"
                
                urllib.request.urlretrieve(q['src'], os.path.join(MyPath, (Full_name)))
                print (q['src'])
                
        p+=1
        Name+=1                 #increasing name variable so name of file is increased
        
    print ("Finished Download of "+url.replace('http://www.hentaibox.net/hentai-manga/','')+ "Enjoy!")


@app.route('/FairyTailDB/<Keyword>')
def GetFTImageLinks(Keyword):
    BaseURL = 'http://www.fairytailhentaidb.com/'
    url = 'http://www.fairytailhentaidb.com/index.php?/category/'+str(Keyword)
    print ('Downloading from url: '+str(url))
    
    CurrentUrl = []                 #This will have the frontpage of the keyword and more depending on next tag
    CurrentUrl.append(url)
    
    ImageLinkList = []
    HistoryList = []
    HistoryList.append(url)
    
    MyCounter = 0
    while MyCounter<len(CurrentUrl):
    
        # Go to the page with the keyword
        browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
        browser.open(CurrentUrl[MyCounter])
        
        MyLink = browser.get_links()
        
        for line in MyLink:
            try:
                if 'picture.php' in line['href'] and 'slideshow' not in line['href']:
                    try:
                        #print (line['href'])
                        FullURL = BaseURL+line['href']
                        ImageLinkList.append(FullURL)
                    except:
                        pass
                    
                #this will add pages to the current url list if there is a next page link
                if 'Next' in line.text:
                    
                    print ('Current URL SIZE before appending: '+str(len(CurrentUrl)))
                    NextFULLUrl = BaseURL+line['href']
                    if NextFULLUrl not in HistoryList and NextFULLUrl not in CurrentUrl:
                        CurrentUrl.append(NextFULLUrl)
                        HistoryList.append(NextFULLUrl)
                    print ('Current URL SIZE after appending: '+str(len(CurrentUrl)))
            except:
                pass
        CurrentUrl.pop(0)
        print ('Current URL SIZE after popping: '+str(len(CurrentUrl)))
        
    NewImageList = list(OrderedDict.fromkeys(ImageLinkList))
    
    print ('Printing all collected image page urls now: ')
    for linky in NewImageList:
        print ('Spawning a process')
        print (linky)
        p = multiprocessing.Process(target=SingleProcessFT, args=(linky,Keyword,))
        p.start()
    return render_template('EdenRoot.html')

def SingleProcessFT(ImageURL,Keyword):
    
    BaseURL = 'http://www.fairytailhentaidb.com/'
    
    #Creating download folder
    CreateNewpath = "C:\Python27\Images\FairyTailDB\\"+str(Keyword)
    #print (CreateNewpath)
    newpath = CreateNewpath
    
    #--------------------if path doesnt exist then make it -------------------------------------#
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    MyPath = newpath
    
    # Go to the page with the image url
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(ImageURL)
    
    MyLink = browser.find_all('img',{'id':'theMainImage'},src=True)

    for line in MyLink:
     
        FULL_URL = BaseURL+line['src']
        print (FULL_URL)
        Name = random.randint(0,1000000000000)
        Full_name = str(Name) + ".jpg"
        response = requests.get(FULL_URL, stream=True)
        with open(os.path.join(MyPath, (Full_name)), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    print ('finished')

@app.route('/NarutoDB/<Keyword>')
def GetNarutoImageLinks(Keyword):
    BaseURL = 'http://www.narutohentaidb.com/'
    url = 'http://www.narutohentaidb.com/index.php?/category/'+str(Keyword)
    print ('Downloading from url: '+str(url))
    
    CurrentUrl = []                 #This will have the frontpage of the keyword and more depending on next tag
    CurrentUrl.append(url)
    
    ImageLinkList = []
    HistoryList = []
    HistoryList.append(url)
    
    MyCounter = 0
    while MyCounter<len(CurrentUrl):
    
        # Go to the page with the keyword
        browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
        browser.open(CurrentUrl[MyCounter])
        
        MyLink = browser.get_links()
        
        for line in MyLink:
            try:
                if 'picture?' in line['href'] and 'slideshow' not in line['href'] and Keyword in line['href']:
             
                    print (line['href'])
                    FullURL = BaseURL+line['href']
                    ImageLinkList.append(FullURL)
              
                    
                #this will add pages to the current url list if there is a next page link
                if 'Next' in line.text:
                    
                    print ('Current URL SIZE before appending: '+str(len(CurrentUrl)))
                    NextFULLUrl = BaseURL+line['href']
                    if NextFULLUrl not in HistoryList and NextFULLUrl not in CurrentUrl:
                        CurrentUrl.append(NextFULLUrl)
                        HistoryList.append(NextFULLUrl)
                    print ('Current URL SIZE after appending: '+str(len(CurrentUrl)))
            except:
                pass
        CurrentUrl.pop(0)
        print ('Current URL SIZE after popping: '+str(len(CurrentUrl)))
        
    NewImageList = list(OrderedDict.fromkeys(ImageLinkList))
    
    print ('Printing all collected image page urls now: ')
    for linky in NewImageList:
        print ('Spawning a process')
        print (linky)
        p = multiprocessing.Process(target=SingleProcessNaruto, args=(linky,Keyword,))
        p.start()
    return render_template('EdenRoot.html')
    
def SingleProcessNaruto(ImageURL,Keyword):
    
    BaseURL = 'http://www.narutohentaidb.com/'
    
    #Creating download folder
    CreateNewpath = "C:\Python27\Images\DBnaruto\\"+str(Keyword)
    #print (CreateNewpath)
    newpath = CreateNewpath
    
    #--------------------if path doesnt exist then make it -------------------------------------#
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    MyPath = newpath
    
    # Go to the page with the image url
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(ImageURL)
    
    MyLink = browser.find_all('img',{'id':'theMainImage'},src=True)

    for line in MyLink:
     
        FULL_URL = BaseURL+line['src']
        print (FULL_URL)
        Name = random.randint(0,1000000000000)
        Full_name = str(Name) + ".jpg"
        response = requests.get(FULL_URL, stream=True)
        with open(os.path.join(MyPath, (Full_name)), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response









# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)
