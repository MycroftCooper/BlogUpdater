from os import scandir
import re
import datetime
from bs4 import BeautifulSoup
import urllib.request,urllib.error

# 正则表达式筛选器
findDate=re.compile(r'<div class="date"> (.*?) <br/>')
findWeek=re.compile(r'<br/>(.*?) </div><div class="weathericon">')
findImage=re.compile(r'<div class="weathericon"><img src="(.*?)"/></div>')
findweather=re.compile(r'<div class="desc"> (.*?) </div><div class="windd">')
findWindDir=re.compile(r'<div class="windd"> (.*?) </div><div class="winds">')
findWind=re.compile(r'<div class="windd"> .*? </div><div class="winds"> (.*?) </div>')
findTemperature=re.compile(r'<div class="tmp tmp_lte_.*?"> (.*?) </div>')


savePath = "weather.md"
sCityName = None
baseUrl = ""


def runWeatherSpider(cityName, cityUrl):
    print('*>>>每日天气爬取中...>>>')
    global baseUrl, sCityName
    try:
        sCityName = cityName
        baseUrl = "http://www.nmc.cn/publish/forecast/{}.html".format(cityUrl)
    except KeyError:
        print("*ERROR>城市{}未被加入城市URL字典中，请编辑CityUrlDict.py文件")
        return False
    print("*目标网站:" + baseUrl)
    print("*存储路径:" + savePath)
    html = askURL(baseUrl)
    datalist = getData(html)
    dataMDStr = getMD(datalist)
    writeMD(dataMDStr)
    print('*SUCCESS>天气爬取完毕')
    return True


#获取网页源码
def askURL(url):
    print('*>>>获取网页HTML源码中...>>>')
    # 模拟浏览器头部信息，向服务器发送消息
    head={"User-Agent": "Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print("*SUCCESS>HTML源码爬取完毕！\n")
    except urllib.error.URLError as e:
        print("*ERROR>HTML源码爬取失败！\n")
        if hasattr(e, "code"):
            print("*" + e.code)
        if hasattr(e, "reason"):
            print("*" + e.reason)
    return html


#解析数据
def getData(html):
    print('*>>>解析数据中...>>>')
    dataList=[]
    soup = BeautifulSoup(html,"html.parser")

    for item in soup.find_all('div',class_="weatherWrap"):  #查找符合要求的字符串，形成列表
        #print(item)  
        weatherDict = dict()  #保存天气的所有信息
        item = str(item)

        date = re.findall(findDate,item)[0]
        weatherDict["date"] = date
        week = re.findall(findWeek,item)[0]    
        weatherDict["week"] = week

        image = re.findall(findImage,item)
        if len(image) == 1:
            image.append(image[0])
            image[0] = "/daily_weather/empty.png"
        weatherDict["img"] = image 

        weather = re.findall(findweather,item)
        weatherDict["weather"] = weather
        windDir = re.findall(findWindDir,item)
        weatherDict["windDir"] = windDir
        wind = re.findall(findWind,item)
        weatherDict["wind"] = wind

        temperature = re.findall(findTemperature,item)
        if len(temperature) == 1:
            temperature.append(temperature[0])
            temperature[0] = ""
        weatherDict["temperature"] = temperature

        dataList.append(weatherDict)
    print("*SUCCESS>数据字典已提取")
    return dataList

# 生成MD格式文件
def getMD(dataList):
    print('#>>>MD文件生成中...>>>')
    nowTime = datetime.datetime.now()
    nowTimeStr1 = nowTime.strftime('%Y/%m/%d %H:%M:%S')
    nowTimeStr2 = nowTime.strftime('%Y年%m月%d日 %H:%M:%S')
    cssCodeStr = ""
    try:
        f = open("weatherPage.css",'r',encoding="utf-8")
        cssCodeStr = f.read()
    except FileExistsError:
        print("*ERROR>weatherPage.css文件丢失")
        return
    weatherMDStr = "---\ntitle: 每日天气\ndate: " + nowTimeStr1 + "\n---\n\n"
    weatherMDStr += cssCodeStr
    weatherMDStr += "<h1>{}七日天气</h1>\n<div id=\"lyrow\"><div class=\"weather\">".format(sCityName)

    for i in range(7):
        dailyWeatherMDStr = ""
        if i == 0:
            dailyWeatherMDStr += "<div class=\"today\">\n"       
        else:
            dailyWeatherMDStr += "<div class=\"daily\">\n"
        dailyWeatherMDStr += "<div class=\"data\">{}<br>{}</div>\n".format(dataList[i]["date"], dataList[i]["week"])

        dailyWeatherMDStr += "<div class=\"halfday\">\n"
        dailyWeatherMDStr += "<img src=\"{}\" class=\"img\">\n".format(dataList[i]["img"][0])
        dailyWeatherMDStr += "<div class=\"info\">{}<br>{}<br>{}</div>\n".format(dataList[i]["weather"][0], dataList[i]["windDir"][0], dataList[i]["wind"][0])
        dailyWeatherMDStr += "<div class=\"temperature\">{}</div>\n</div>\n".format(dataList[i]["temperature"][0])

        dailyWeatherMDStr += "<div class=\"halfday\">\n"
        dailyWeatherMDStr += "<div class=\"temperature\">{}</div>\n".format(dataList[i]["temperature"][1])
        dailyWeatherMDStr += "<img src=\"{}\" class=\"img\">\n".format(dataList[i]["img"][1])
        dailyWeatherMDStr += "<div class=\"info\">{}<br>{}<br>{}</div>\n</div>\n</div>\n".format(dataList[i]["weather"][1], dataList[i]["windDir"][1], dataList[i]["wind"][1])
        weatherMDStr += dailyWeatherMDStr

    weatherMDStr += "</div><br><br><h5>更新时间:{} <br> 数据来源:{}</h5></div>\n".format(nowTimeStr2, baseUrl)
    return weatherMDStr

# 保存MD格式文件
def writeMD(dataMDStr):
    f = open(savePath,"w",encoding="utf-8")
    f.write(dataMDStr)
    print("*SUCCESS>MD文件已生成")   