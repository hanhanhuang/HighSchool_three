import requests,os
from bs4 import BeautifulSoup
import tkinter as tk
import urllib.request,pathlib
import PIL.Image, PIL.ImageTk
from tkinter import *

photos=[]
movieN=[]
cname=[]
alevel=[]
ename=[]
rtime=[]
content=[]
movieNum=0
while(1):
    if(movieNum<10):
        url='https://movies.yahoo.com.tw/movie_thisweek.html'
    elif((bs.find('li','nexttxt').a)==None):
        break
    else:
        nextp=bs.find('li','nexttxt').a.get('href')
        url=nextp
    html=requests.get(url)
    html.encoding="utf-8"
    bs=BeautifulSoup(html.text,'html.parser')

    items=bs.find_all('div','release_info')

    for item in items:
        cName=item.find('div','release_movie_name').a.text.strip()
        eName=item.find('div','en').a.text.strip()
        rTime=item.find('div','release_movie_time')
        level=item.find('span').text.strip()
        txt=item.find('div','release_text').text.strip()
        movieNum+=1
       
        print('新片編號:',movieNum)
        print('中文片名:',cName)
        print('英文片名:',eName)
        print(rTime.text)
        print('期待度:',level)
        print('內容摘要:',txt)
        print()
        movieN.append(movieNum)
        cname.append(cName)
        alevel.append(level)
        ename.append(eName)
        rtime.append(rTime.text)
        content.append(txt)
   
    items2=bs.find_all('div','release_foto')
    for item2 in items2:
        photo=item2.a.img['src']
        photos.append(photo)
    for photo in photos:
        with requests.get(photo) as r:
            r.raise_for_status()
            with open(os.path.basename(photo),'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
#down
def testfunc_1():
    global dataindex
    global l, l2, l3, l4, panel, imgs
    C['state'] = tk.NORMAL
    dataindex = dataindex+1
    l.destroy()
    l2.destroy()
    l3.destroy()
    l4.destroy()
    l = tk.Label(win, text='中文片名：'+cname[dataindex], bg = 'white')
    l.place(x=150, y=20)
    l2 = tk.Label(win, text='英文片名：'+ename[dataindex], bg = 'white')
    l2.place(x=150, y=60)
    l3 = tk.Label(win, text=rtime[dataindex], bg = 'white')
    l3.place(x=150, y=100)
    l4 = tk.Label(win, text='期待度：'+alevel[dataindex], bg = 'white')
    l4.place(x=150, y=140)
    panel.destroy()
    panel = Label(win, image = imgs[dataindex])
    panel.place(x=20, y=20)
    if(dataindex == len(alevel)-1):
        B['state'] = tk.DISABLED
        
#up       
def testfunc_2():
    global dataindex
    global l, l2, l3, l4, panel, imgs
    B['state'] = tk.NORMAL
    dataindex = dataindex-1
    l.destroy()
    l2.destroy()
    l3.destroy()
    l4.destroy()
    l = tk.Label(win, text='中文片名：'+cname[dataindex], bg = 'white')
    l.place(x=150, y=20)
    l2 = tk.Label(win, text='英文片名：'+ename[dataindex], bg = 'white')
    l2.place(x=150, y=60)
    l3 = tk.Label(win, text=rtime[dataindex], bg = 'white')
    l3.place(x=150, y=100)
    l4 = tk.Label(win, text='期待度：'+alevel[dataindex], bg = 'white')
    l4.place(x=150, y=140)
    panel.destroy()
    panel = Label(win, image = imgs[dataindex])
    panel.place(x=20, y=20)
    if(dataindex == 0):
        C['state'] = tk.DISABLED
        
#GUI
win = tk.Tk()
win.title('本週新片')
win.geometry('500x300')
win.configure(background = 'white')

dataindex = 0
imgs = []
for i in range(len(alevel)):
    path = os.path.basename(photos[i])
    image = PIL.Image.open(path)
    image = image.resize((100, 100), PIL.Image.ANTIALIAS) #平滑濾波:高質量的重採樣濾波，以計算輸出像素值
    img = PIL.ImageTk.PhotoImage(image)
    imgs.append(img)
    
panel = Label(win, image = imgs[dataindex])
panel.place(x=20, y=20)
l = tk.Label(win, text='中文片名：'+cname[dataindex], bg = 'white')
l.place(x=150, y=20)
l2 = tk.Label(win, text='英文片名：'+ename[dataindex], bg = 'white')
l2.place(x=150, y=60)
l3 = tk.Label(win, text=rtime[dataindex], bg = 'white')
l3.place(x=150, y=100)
l4 = tk.Label(win, text='期待度：'+alevel[dataindex], bg = 'white')
l4.place(x=150, y=140)

#down_button
B = tk.Button(win, text = '下一筆', command = testfunc_1)
B.place(x=200, y=200)

#up_button
C = tk.Button(win, text = '上一筆', command = testfunc_2)
C.place(x=100, y=200)
C['state'] = tk.DISABLED

win.mainloop()