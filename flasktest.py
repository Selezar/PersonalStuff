'''
This is a flask file containing a lot of useful and experimental web scraping code. Everything is mainly placed here so that the user can use the
browser as an interface and not need to create a custom GUI with Tkinter. Websites scraped include Tumblr.
Another function included edits text file as well. This code also exercises and implements historic record management of code with text files

'''

from flask import Flask, render_template, request, url_for
import urllib
import urlparse
from random import randint
from bs4 import BeautifulSoup
import os
import urllib2

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def Root():
    
    return render_template('root.html')

# This will save all links to text file
@app.route('/SaveImglinks')
def RootCrawler():
    f = open("ImgLinks.txt",'a')
    urls = []
    
    MyImgStack = []
 
    print ("POPULATING STACK WITH ALL WEBPAGE ADDRESS..")
    print ("")
    z = 1
    while z<21:
        var2 = "http://grab-tits-akd.tumblr.com/page/"+str(z)
        print ("\"http://grab-tits-akd.tumblr.com/page/"+str(z)+"\",")
        urls.append(var2)
        z+=1
        
    print ("")
    print ("FETCHING IMG LINKS FROM ALL WEBSITES..")
    print ("")
    
    p=0
    while p<len(urls):
        r = urllib.urlopen(urls[p]).read()
        soup = BeautifulSoup(r.content)
        x = soup.find_all("img")

        k=0
        while k<len(x):
            print x[k].get('src')
            print len(urls)
            print p
            print ("")
            MyImgStack.append(x[k].get('src'))
       
            if "static" in x[k].get('src'):
                MyImgStack.pop()
            if "Login" in x[k].get('src'):
                MyImgStack.pop()
            if "avatar" in x[k].get('src'):
                MyImgStack.pop()
            if "avatars" in x[k].get('src'):
                MyImgStack.pop()
            if "plugin" in x[k].get('src'):
                MyImgStack.pop()
            if "plugins" in x[k].get('src'):
                MyImgStack.pop()
            if "px.srvcs" in x[k].get('src'):
                MyImgStack.pop()
            if "statcounter" in x[k].get('src'):
                MyImgStack.pop()
            if "square" in x[k].get('src'):
                MyImgStack.pop()
            if "counter" in x[k].get('src'):
                MyImgStack.pop()
            if "php" in x[k].get('src'):
                MyImgStack.pop()
            if "thumb" in x[k].get('src'):
                MyImgStack.pop()
            if "thumbs" in x[k].get('src'):
                MyImgStack.pop()
            
            k+=1
        p+=1
     
    print ("POPULATING TEXTFILE WITH ALL SAVED LINKS..")
    
    L = 0
    while L<len(MyImgStack):
        f.write(MyImgStack[L]+'\n')
        print ("Link Written: "+str(MyImgStack[L]) )
        L +=1
        
    f.close()
    
    return '''
    
    <!DOCTYPE html>
   <head>
      <title>CRAWLER</title>
      <script language="javascript">
    window.location.href = "http://localhost:5000"
   </script>
   </head>
   <body>
   <h1>YOU SHALL NOT PASS</h1>
   </body>
</html>
'''

#This will fetch a random line of img link from text file and send it to index.html to be viewed
@app.route('/RHimg')
def RandomHimgWebPage():

    f = open("ImgLinks.txt",'r')
    lines = f.readlines()
    
    RandomLine = randint(0,(len(lines)-1))
    
    print ("TOTAL NUMBER OF LINES: "+str(len(lines)))
    print ("RANDOM LINE BEING READ: " + str(RandomLine))
    
    ImgLink = lines[RandomLine]
    print ImgLink
        
    f.close()
    
    return render_template('index.html', ImgLink=ImgLink)

#This will rewrite the text file line by line leaving out any lines with rmstring in it 
@app.route('/RmLines/<rmstring>')
def RemoveLinesFromTextFile(rmstring):
    f = open("ImgLinks.txt",'r')

    lines = f.readlines()

    f.close()

    f = open("ImgLinks.txt","w")
    x=0
    for line in lines:
        if rmstring not in line:

            f.write(line)
            print line
        x+=1
        
    print x       
    f.close()
    return '''
    <!DOCTYPE html>
   <head>
      <title>CRAWLER</title>
      <script language="javascript">
    window.location.href = "http://localhost:5000"
   </script>
   </head>
   <body>
   <h1>YOU SHALL NOT PASS</h1>
   </body>
</html>
'''

#This will crawl specified website and return all href links with the specific tag word in it
@app.route('/LinkSearch/<WebPage>/<KeyWord>')
def LinkSearch(WebPage,KeyWord):

    url = "http://"+str(WebPage)+"/"
    LookForKeyWord = KeyWord

    urls = [url]                #stack of urls to scrape

    while len(urls)>0:
        try:
            htmltext = urllib.urlopen(urls[0]).read()
        except:
            print urls[0]
        
        soup = BeautifulSoup(htmltext)
    
        urls.pop(0)
        print len(urls)
    
        for line in soup.findAll('a',href=True):
            line['href'] = urlparse.urljoin(url,line['href'])
            #print line['href']
    
            if url in line['href'] and line['href'] not in visited and LookForKeyWord in line['href']:
                urls.append(line['href'])
                visited.append(line['href'])
                
    f = open("LinkRetrieve.txt",'w')
    print ("Writing ALL LINKS TO test1.txt file....")
    for que in visited:
        f.write(que+'\n')
        print que
    f.close()
    return '''
    <!DOCTYPE html>
   <head>
      <title>CRAWLER</title>
      <script language="javascript">
    window.location.href = "http://localhost:5000"
   </script>
   </head>
   <body>
   <h1>YOU SHALL NOT PASS</h1>
   </body>
</html>
'''

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
    NewFrontPageUrls = map(lambda a: str(a), Rooturls)
    
    with open('UpdateLog.txt') as f:
        UpdateLogLines = f.read().splitlines()
    
    Intersect = set(NewFrontPageUrls) & set(UpdateLogLines)

    for stuff in Intersect:
        print stuff
        NewFrontPageUrls.remove(stuff)
    
    f = open("UpdateLog.txt",'a')
    
    print ("Printing everything in Rooturls list now:")    
    for item in NewFrontPageUrls:
        f.write(item+'\n')
        print item
    #----------------SECTION TO CONVERT MULTIPLE LINKS INTO ROOTURLS LIST DONE-------------------------#    
    
    f.close()
    ChoosePath = 0          #Variable used to identify what the saved path anme will be dependant on genre tag
    
    Counter=0
    while Counter<len(NewFrontPageUrls):
        
        WebPageData = urllib.urlopen(NewFrontPageUrls[Counter]).read()
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
            elif 'Incest' in line.text:
                print ("THIS COMIC HAS Incest TAG")
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
                print ("THIS COMIC HAS Sister TAG")
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
     
        url = NewFrontPageUrls[Counter] +'//'
        print ("STARTING Download from URL: "+str(url))
        print ("=====================================================================================")   
    
        #Creating the folder with name trunctated from the url itself
        if ChoosePath == 0:
            CreateNewpath = "C:\Python27\Images\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 1:
            CreateNewpath = "C:\Python27\Images\Str8-Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 2:
            CreateNewpath = "C:\Python27\Images\Lact\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 3:
            CreateNewpath = "C:\Python27\Images\Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 4:
            CreateNewpath = "C:\Python27\Images\Incest\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 5:
            CreateNewpath = "C:\Python27\Images\Teacher\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 6:
            CreateNewpath = "C:\Python27\Images\Apron\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 7:
            CreateNewpath = "C:\Python27\Images\Paizuri\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 8:
            CreateNewpath = "C:\Python27\Images\Megane\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 9:
            CreateNewpath = "C:\Python27\Images\Force\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 10:
            CreateNewpath = "C:\Python27\Images\Sister\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 11:
            CreateNewpath = "C:\Python27\Images\Elf\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 12:
            CreateNewpath = "C:\Python27\Images\Hairjob\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 13:
            CreateNewpath = "C:\Python27\Images\Hypnosis\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 14:
            CreateNewpath = "C:\Python27\Images\Military\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 15:
            CreateNewpath = "C:\Python27\Images\Reverseforce\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 16:
            CreateNewpath = "C:\Python27\Images\Story\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 17:
            CreateNewpath = "C:\Python27\Images\Smallp\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 18:
            CreateNewpath = "C:\Python27\Images\Stocking\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
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
            htmltext = urllib.urlopen(urls[p]).read()   
            soup = BeautifulSoup(htmltext)
        
            print ""    
            AllImageLinks = soup.find_all('img',src=True)
            
            for q in AllImageLinks:
                if "ads-iframe" not in q['src'] and ".png" not in q['src']:
                    #The name should be incremental from 0 to infinity with.jpg at end
                    Full_name = str(Name) + ".jpg"
                    
                    urllib.urlretrieve(q['src'], os.path.join(MyPath, (Full_name)))
                    print q['src']
                    
            p+=1
            Name+=1                 #increasing name variable so name of file is increased
            
        print ("Finished Download of "+url.replace('http://www.hentaibox.net/hentai-manga/','')+ "Enjoy!")
        Counter +=1
        
        
    return render_template('root.html')

#This will fetch all the front page links based on var1 arg passed into it
def FindFrontPageLinks(var1):
    
    if 'Straight-Shota' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Straight-Shota_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Shota' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Shota_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Lactation' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Lactation_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Paizuri' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Paizuri_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Incest' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Incest_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Teacher' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Teacher_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Naked-Apron' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Naked-Apron_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Force' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Force_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Elf' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Elf_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Hairjob' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Hairjob_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Hypnosis' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Hypnosis_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Military-Uniform' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Military-Uniform_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Reverse-Force' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Reverse-Force_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Small-Penis' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Small-Penis_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Stockings' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Stockings_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Story-Arc' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=_Story-Arc_&Series=&pages=&color=&tag=&related=tags&shownew=new"
    elif 'Best' in var1:
        BaseUrl = "http://www.hentaibox.net/?re=&q=&Series=&pages=&color=&tag=&related=&shownew=rating"
    elif 'Trending' in var1:
        BaseUrl = "http://my.hentaibox.net/?trending=manga"

    FrontPageURLS = []
    
    htmltextfile = urllib.urlopen(BaseUrl).read()
    
    Soup = BeautifulSoup(htmltextfile)
    
    AlltdTags = Soup.find_all('td',{'class':'search_gallery_item'})
    
    p=0
    while p<len(AlltdTags):
        print '=============================================================='
        print ("ON ALLTDTAGS LIST NO. : " + str(p))
        Linktags = AlltdTags[p].find_all('a',href=True)
        
        for line in Linktags:
            if "hentai-manga" in line['href']:
                FrontPageURLS.append(line['href'])
                        
            print line
            print ''
        
        p+=1
    
    print '==========================================='
    print ("PRINTING ALL COLLECTED FRONT PAGE URLS: ")
    
    
    for q in FrontPageURLS:
        print q
        print ''
        
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
        print stuff
        NewFrontPageUrls.remove(stuff)
    
    f = open("UpdateLog.txt",'a')
    
    for item in NewFrontPageUrls:
        f.write(item+'\n')

    f.close()
    
    print ''
    print ("The update to all relevant genres has finished...")
    print ''
    return NewFrontPageUrls

    
@app.route('/UpdateFolder/<Name>')
def UpdateDownloadFolder(Name):
    Rooturls = []
    Rooturls = FindFrontPageLinks(Name)
    
    ChoosePath = 0
    
    Counter=0
    while Counter<len(Rooturls):
        
        WebPageData = urllib.urlopen(Rooturls[Counter]).read()
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
            elif 'Incest' in line.text:
                print ("THIS COMIC HAS Incest TAG")
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
     
        url = Rooturls[Counter] +'//'
        print ("STARTING Download from URL: "+str(url))
        print ("=====================================================================================")   
    
        #Creating the folder with name trunctated from the url itself
        if ChoosePath == 0:
            CreateNewpath = "C:\Python27\Images\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 1:
            CreateNewpath = "C:\Python27\Images\Str8-Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 2:
            CreateNewpath = "C:\Python27\Images\Lact\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 3:
            CreateNewpath = "C:\Python27\Images\Atosh\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 4:
            CreateNewpath = "C:\Python27\Images\Incest\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 5:
            CreateNewpath = "C:\Python27\Images\Teacher\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 6:
            CreateNewpath = "C:\Python27\Images\Apron\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 7:
            CreateNewpath = "C:\Python27\Images\Paizuri\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 8:
            CreateNewpath = "C:\Python27\Images\Megane\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 9:
            CreateNewpath = "C:\Python27\Images\Force\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 10:
            CreateNewpath = "C:\Python27\Images\Sister\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 11:
            CreateNewpath = "C:\Python27\Images\Elf\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 12:
            CreateNewpath = "C:\Python27\Images\Hairjob\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 13:
            CreateNewpath = "C:\Python27\Images\Hypnosis\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 14:
            CreateNewpath = "C:\Python27\Images\Military\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 15:
            CreateNewpath = "C:\Python27\Images\Reverseforce\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 16:
            CreateNewpath = "C:\Python27\Images\Story\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 17:
            CreateNewpath = "C:\Python27\Images\Smallp\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
            newpath = CreateNewpath
        elif ChoosePath == 18:
            CreateNewpath = "C:\Python27\Images\Stocking\\"+url.replace('http://www.hentaibox.net/hentai-manga/','')
            print CreateNewpath
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
            htmltext = urllib.urlopen(urls[p]).read()   
            soup = BeautifulSoup(htmltext)
        
            print ""    
            AllImageLinks = soup.find_all('img',src=True)
            
            for q in AllImageLinks:
                if "ads-iframe" not in q['src'] and ".png" not in q['src']:
                    #The name should be incremental from 0 to infinity with.jpg at end
                    Full_name = str(Name) + ".jpg"
                    
                    urllib.urlretrieve(q['src'], os.path.join(MyPath, (Full_name)))
                    print q['src']
                    
            p+=1
            Name+=1                 #increasing name variable so name of file is increased
            
        print ("Finished Download of "+url.replace('http://www.hentaibox.net/hentai-manga/','')+ "Enjoy!")
        Counter +=1
    print ''    
    print ("Finished updating. Thank you for waiting. Enjoy!")
    print ''
    return render_template('root.html')
 
#Download images from Erolord   
@app.route('/erolord/<Keyword>')
def ErolordScraping(Keyword):
    #baseurl will be built using the keyword. This is the starting position of the algorithm a.k.a first page of erolord.com with keyword
    BaseURL = 'http://erolord.com/parody/' + Keyword + '/'
    print BaseURL
    #Opening base url in command line to start scraping its data
    HtmlFile = urllib.urlopen(BaseURL).read()
    soup = BeautifulSoup(HtmlFile)
        
    #Section to figure out how many pages this keyword in erolord has
    ArrayOfPageNumbers = []
    SoupLinkTagswithLast = soup.find_all('a',{'class':'last'})
    SoupLinkTagswithPageLarger = soup.find_all('a',{'class':'page larger'},href=True)
    for line in SoupLinkTagswithLast:
        print line['href']
        BaseURLwithpages = BaseURL+'page/'
        NumberofPages = line['href'].replace(BaseURLwithpages,'')
        FinalNumberofPages = int(NumberofPages.replace('/',''))
        ArrayOfPageNumbers.append(FinalNumberofPages)
       
    for owo in SoupLinkTagswithPageLarger:
        print owo['href']
        BaseURLwithpages = BaseURL+'page/'
        NumberofPages = owo['href'].replace(BaseURLwithpages,'')
        FinalNumberofPages = int(NumberofPages.replace('/',''))
        ArrayOfPageNumbers.append(FinalNumberofPages)
        
    for lolo in ArrayOfPageNumbers:
        print lolo
        
        NUMPAGE = max(ArrayOfPageNumbers)
        
    #Now that we know number of pages we can find all the links with it
    MacroPageURLS = []
    counter = 1
    while counter<(NUMPAGE+1):
        CurrentPage = BaseURL+'page/'+str(counter)
        MacroPageURLS.append(CurrentPage)
        counter+=1
    
    for owo in MacroPageURLS:
        print owo
    #Now we have to go to each of these pages and find all img links
    UniqueImgPageURLS = []
    i=0
    while i<len(MacroPageURLS):
        print 'Opening Page URL: '+str(MacroPageURLS[i])
        htmlf = urllib.urlopen(MacroPageURLS[i]).read()
        soup2 = BeautifulSoup(htmlf)
        LinkTags = soup2.find_all('a',{'class':'aa1'},href=True)
        for stuff in LinkTags:
            UniqueImgPageURLS.append(stuff['href'])
            print 'Added img link'
            
        i+=1
    print ''
    print 'These are all the unique image links for '+str(Keyword)
    for q in UniqueImgPageURLS:
        print q
    
    #Now we have to open each of these individual links and download the biggest image from in it
    
    #First lets make the file directory to store these images
    CreateNewpath = "C:\Python27\Images\EROLORD\\"+str(Keyword)
    print 'Path to store images: '+CreateNewpath
    newpath = CreateNewpath
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    MyPath = newpath                        #This is one half of where it will be stored, the name of file still has to be genrated with Name variable
    Name = 0
    
    print ''
    print 'Initialising Download of images'
    print 'Initialising Download of images'
    print 'Initialising Download of images'
    print ''
    
    #Now to open each of these links and grab the image in them
    thing=0
    while thing<len(UniqueImgPageURLS):
        NewHtml = urllib.urlopen(UniqueImgPageURLS[thing]).read()
        soup3 = BeautifulSoup(NewHtml)
        ImgTag = soup3.find_all('img',{'class':'mainimg'},src=True)
        print 'On Loop number: ' + str(thing)
        
        for t in ImgTag:
            #The name should be incremental from 0 to infinity with.jpg at end
            Full_name = str(Name) + ".jpg"
            urllib.urlretrieve(t['src'], os.path.join(MyPath, (Full_name)))
            print t['src']
            
        thing +=1
        Name +=1
    
    print ('FINISHED DOWNLOADING ALL ENJOY')
    #baseurl will be built using the keyword. This is the starting position of the algorithm a.k.a first page of erolord.com with keyword
    BaseURL = 'http://erolord.com/parody/' + Keyword + '/'
    print BaseURL
    #Opening base url in command line to start scraping its data
    HtmlFile = urllib.urlopen(BaseURL).read()
    soup = BeautifulSoup(HtmlFile)
        
    #Section to figure out how many pages this keyword in erolord has
    SoupLinkTags = soup.find_all('a',{'class':'last'},href=True)
    for line in SoupLinkTags:
        BaseURLwithpages = BaseURL+'page/'
        NumberofPages = line['href'].replace(BaseURLwithpages,'')
        FinalNumberofPages = int(NumberofPages.replace('/',''))
        print ('Number of pages: '+str(FinalNumberofPages))
        
    #Now that we know number of pages we can find all the links with it
    MacroPageURLS = []
    counter = 1
    while counter<(FinalNumberofPages+1):
        CurrentPage = BaseURL+'page/'+str(counter)
        MacroPageURLS.append(CurrentPage)
        counter+=1
    
    for owo in MacroPageURLS:
        print owo
    #Now we have to go to each of these pages and find all img links
    UniqueImgPageURLS = []
    i=0
    while i<len(MacroPageURLS):
        print 'Opening Page URL: '+str(MacroPageURLS[i])
        htmlf = urllib.urlopen(MacroPageURLS[i]).read()
        soup2 = BeautifulSoup(htmlf)
        LinkTags = soup2.find_all('a',{'class':'aa1'},href=True)
        for stuff in LinkTags:
            UniqueImgPageURLS.append(stuff['href'])
            print 'Added img link'
            
        i+=1
    print ''
    print 'These are all the unique image links for '+str(Keyword)
    for q in UniqueImgPageURLS:
        print q
    
    #Now we have to open each of these individual links and download the biggest image from in it
    
    #First lets make the file directory to store these images
    CreateNewpath = "C:\Python27\Images\EROLORD\\"+str(Keyword)
    print 'Path to store images: '+CreateNewpath
    newpath = CreateNewpath
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    MyPath = newpath                        #This is one half of where it will be stored, the name of file still has to be genrated with Name variable
    Name = 0
    
    print ''
    print 'Initialising Download of images'
    print 'Initialising Download of images'
    print 'Initialising Download of images'
    print ''
    
    #Now to open each of these links and grab the image in them
    thing=0
    while thing<len(UniqueImgPageURLS):
        NewHtml = urllib.urlopen(UniqueImgPageURLS[thing]).read()
        soup3 = BeautifulSoup(NewHtml)
        ImgTag = soup3.find_all('img',{'class':'mainimg'},src=True)
        print 'On Loop number: ' + str(thing)
        
        for t in ImgTag:
            #The name should be incremental from 0 to infinity with.jpg at end
            Full_name = str(Name) + ".jpg"
            urllib.urlretrieve(t['src'], os.path.join(MyPath, (Full_name)))
            print t['src']
            
        thing +=1
        Name +=1
    
    print ('FINISHED DOWNLOADING ALL ENJOY')
    return render_template('root.html')

#Download stuff from imagefap
@app.route('/ImageFap/<Keyword>/<PageLimit>')    
def ImageFapScraping(Keyword,PageLimit):
        
    #Section to figure out how many pages this keyword in erolord has
    ArrayOfPages = []
    
    walao = 0
    while walao<int(PageLimit):
        thisvar = 'http://www.imagefap.com/gallery.php?search='+str(Keyword)+'&page=' + str(walao) + '&submitbutton=Search%21&filter_size=&filter_date='
        walao+=1
        ArrayOfPages.append(thisvar)
    
    for qq in ArrayOfPages:
        print qq
        
    GalleryTitleLinkTags = []    
    #Now we go to each of these front pages and get the links of each heading
    for waka in range(len(ArrayOfPages)):
        OpenHtml = urllib.urlopen(ArrayOfPages[waka]).read()
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
        print stuff
        
    MegaImgLinkList = []
    #Now we have to go to each of these heading galleies and add each image page link to main pageurl list
    for cnt in range(len(GalleryTitleLinkTags)):
        htmlfile = urllib.urlopen(GalleryTitleLinkTags[cnt]).read()

        soup = BeautifulSoup(htmlfile,'html.parser')


        Linktag = soup.find_all('div',{'id':'gallery'})

        for line in Linktag:
            Atag = line.find_all('a',href=True)
            for z in Atag:
                print 'http://www.imagefap.com'+ z['href']
                MegaImgLinkList.append('http://www.imagefap.com'+z['href'])

    
    for po in MegaImgLinkList:
        print po
    
    #Now we can start grabbing the img from each of these pages

    
    #First lets make the file directory to store these images
    CreateNewpath = "C:\Python27\Images\ImageFap\\"+str(Keyword)
    print 'Path to store images: '+CreateNewpath
    newpath = CreateNewpath
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    MyPath = newpath                        #This is one half of where it will be stored, the name of file still has to be genrated with Name variable
    Name = 0
    
    print ''
    print 'Initialising Download of images'
    print 'Initialising Download of images'
    print 'Initialising Download of images'
    print ''
    
    #Now to open each of these links and grab the image in them
    thing=0
    while thing<len(MegaImgLinkList):
        try:
            NewHtml = urllib.urlopen(MegaImgLinkList[thing]).read()
            soup3 = BeautifulSoup(NewHtml,'html.parser')
            ImgTag = soup3.find_all('img',src=True)
            for line in ImgTag:
                if 'http://' in line['src'] and 'thumb' not in line['src'] and 'ip.gif' not in line['src']and 'xorigin.fap.to' not in line['src']:
                    print line['src']
    
                    #The name should be incremental from 0 to infinity with.jpg at end
                    Full_name = str(Name) + ".jpg"
                    urllib.urlretrieve(line['src'], os.path.join(MyPath, (Full_name)))
        except:
            pass
        thing +=1
        Name +=1
    
    print ('FINISHED DOWNLOADING ALL ENJOY')
    return render_template('root.html')


# Run the app
if __name__ == "__main__":

    app.run(host='0.0.0.0',port=5000, debug=True)
