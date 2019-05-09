#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
from urllib import request
import os

def getHouseList(url):
    house =[]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    #get从网页获取信息
    res = requests.get(url,headers=headers)
    #解析内容
    soup = BeautifulSoup(res.content,'lxml')
    #房源title
    housename_divs = soup.find_all('div',class_='title')
    for housename_div in housename_divs:
        housename_as=housename_div.find_all('a')
        for housename_a in housename_as:
            housename=[]
            #标题
            housename.append(housename_a.get_text())
            #超链接
            housename.append(housename_a['href'])
            house.append(housename)
    huseinfo_divs = soup.find_all('div',class_='houseInfo')
    for i in range(len(huseinfo_divs)):
        info = huseinfo_divs[i].get_text()
        infos = info.split('|')
        #小区名称
        house[i].append(infos[0])
        #户型
        house[i].append(infos[1])
        #平米
        house[i].append(infos[2])
        #朝向
        house[i].append(infos[3])
    #查询总价
    house_prices = soup.find_all('div',class_='totalPrice')
    for i in range(len(house_prices)):
        #价格
        price = house_prices[i].get_text()
        house[i].append(price)
    #单价
    house_danjias = soup.find_all('div', class_='unitPrice')
    for i in range(len(house_danjias)):
        danjia = house_danjias[i].find('span')
        house[i].append(danjia.get_text())
    #楼层
    house_post = soup.find_all('div',class_='positionInfo')
    for i in range(len(house_post)):
        house[i].append(house_post[i].get_text())
    #标签
    house_tags = soup.find_all('div',class_='tag')
    for i in range(len(house_tags)):
        #链家隐藏了热推的房屋信息
        if(i>=len(house)):
            break
        #满二
        second = house_tags[i].find('span',class_='five')
        #满五
        five = house_tags[i].find('span',class_='taxfree')
        if(second):
            house[i].append(second.get_text())
        elif(five):
            house[i].append(five.get_text())
        else:
            house[i].append('未满五年')
    return house

#爬取房屋详细信息：所在区域、套内面积、户型图
def houseinfo(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.content,'lxml')
    msg =[]
    #所在区域
    areainfos = soup.find_all('span',class_='info')
    for areainfo in areainfos:
        #只需要获取第一个a标签的内容即可
        area = areainfo.find('a')
        if(not area):
            continue
        hrefStr = area['href']
        if(hrefStr.startswith('javascript')):
            continue
        msg.append(area.get_text())
        break
    #根据房屋户型计算套内面积
    infolist = soup.find_all('div',id='infoList')
    num = []
    for info in infolist:
        cols = info.find_all('div',class_='col')
        for i in cols:
            pingmi = i.get_text()
            try:
                a = float(pingmi[:-2])
                num.append(a)
            except ValueError:
                continue
    index = url.rindex('/')
    #房屋信息id
    directory = url[index+1:-5]
    msg.append(directory)
    #每个房屋的图片存放在对应id的目录下
    path = 'd:/images/'+directory
    if(not os.path.exists(path)):
        os.makedirs(path)
    imgurls =  soup.find_all('div',class_='thumbnail')
    for imgurl in imgurls:
        imgurluls = imgurl.find('ul',class_='smallpic')
        lis = imgurluls.find_all('li')
        i=123
        for li in lis:
            imgurl = li.find_all('img')
            for url in imgurl:
                filename = 'image'+str(i)
                src = url['src']
                src=src.replace('120x80','710x400')
                # print(src)
                request.urlretrieve(src,path+'/'+filename+'.jpg')
                i=i+1
    msg.append(sum(num))

    #详细信息中的税费查询是否满五或者满二
    content = None
    contents = soup.find_all('div',class_='baseattribute clear')
    for i in range(len(contents)):
        name = contents[i].find('div',class_='name')
        if(name.get_text()=='税费解析'):
            content_div = contents[i].find('div',class_='content')
            content = content_div.get_text()
            if(content.find('满二')>0 or content.find('满两')>0):
                if(content.find('不满')>0):
                    continue
                else:
                    content='满二'
            elif(content.find('满五')>0):
                if(content.find('不满')>0):
                    continue
                else:
                    content='满五'
        else:
            continue
        msg.append(content)
    return msg

#将房源信息写入txt文件
def writeFile(houseinfo):
    f = open('d:/房源1.txt','a',encoding='utf8')
    # houseinfo.join('\n')
    f.write(houseinfo+'\n')
    f.close()

def appendHouse(url):
    houses =getHouseList(url)
    for house in houses:
        link = house[1]
        if(not link.startswith('http')):
            continue
        mianji = houseinfo(link)
        #将套内面积、所在区域增加到房源信息
        house.extend(mianji)
        xiaoqu = house.pop(2)
        house.insert(0,xiaoqu)
        print(house)
        info = "###$$$".join([str(x) for x in house])
        writeFile(info)

def getJiaHeCheng():
    for i in range(1,2):
        print('-----分隔符',i,'-------')
        url ='https://sjz.lianjia.com/ershoufang/hy1l2c3220030486991985c3220030686377458c3220030683227637rs%E7%B4%AB%E6%99%B6%E6%82%A6%E5%9F%8E/'

    # if i==1:
    #         url ='https://sjz.lianjia.com/ershoufang/c3211056503745/?sug=%E5%92%8C%E5%B9%B3%E4%B8%96%E5%AE%B6'
    #     else:
    #         url = 'https://sjz.lianjia.com/ershoufang/pg'+str(i)+'rs%E6%98%9F%E6%B2%B3%E7%9B%9B%E4%B8%96%E5%9F%8E/'
            # url='https://sjz.lianjia.com/ershoufang/pg'+str(i)+'c3211056507395/?sug=%E7%9B%9B%E4%B8%96%E9%95%BF%E5%AE%89'
        appendHouse(url)

def getShengShiChangAn():
    for i in range(1,4):
        print('-----分隔符',i,'-------')
        if i==1:
            url ='https://sjz.lianjia.com/ershoufang/c3211056507395/?sug=%E7%9B%9B%E4%B8%96%E9%95%BF%E5%AE%89'
        else:
            url='https://sjz.lianjia.com/ershoufang/pg'+str(i)+'c3211056507395/?sug=%E7%9B%9B%E4%B8%96%E9%95%BF%E5%AE%89'
        appendHouse(url)
#主函数
def main():
    # getJiaHeCheng()
    getShengShiChangAn()

if __name__ == '__main__':
    main()

