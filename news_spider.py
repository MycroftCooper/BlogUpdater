import re
import ast
import datetime
import urllib.request,urllib.error

newsUrl = "https://top.baidu.com/board?tab=realtime"
savePath = "news.md"

# 主逻辑
def runNewsSpider():
    print('#>>>每日新闻爬取中...>>>')
    print("#目标网站:" + newsUrl)
    print("#存储路径:" + savePath)
    htmlCode = askURL()
    if htmlCode is None:
        print("#ERROR>数据字典爬取失败")
        return False
    newsList = getData(htmlCode)
    if newsList is None:
        print("#ERROR>数据字典生成失败")
        return False
    newsMDStr = getMD(newsList)
    writeMD(newsMDStr)
    print('#SUCCESS>新闻爬取完毕')
    return True


#获取网页源码
def askURL():
    print('#>>>获取网页HTML源码中...>>>')
    # 模拟浏览器头部信息，向服务器发送消息
    head={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    request=urllib.request.Request(newsUrl,headers=head)
    html=""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print("#SUCCESS>HTML源码爬取完毕！\n")
    except urllib.error.URLError as e:
        print("#ERROR>HTML源码爬取失败！\n")
        if hasattr(e, "code"):
            print("#" + str(e.code))
        if hasattr(e, "reason"):
            print("#" + str(e.reason))
    return html


#解析数据
def getData(html):
    print('#>>>解析数据中...>>>')
    newsDictListStr = None
    try:
        findNewsDictList = re.compile(r',"content":\[\{([\s\S]*)\}\],"moreUrl":')
        newsDictListStr = re.findall(findNewsDictList,html)[0]
        print("#SUCCESS>字典串截取成功")
    except IndexError:
        print("#ERROR>字典串截取失败，目标网站源码可能发生改变!")
        return newsDictListStr

    dataStrList = newsDictListStr.split('},{')
    print('#SUCCESS>原始数据字典分析完毕')
    newsList = []
    try:
        for dataStr in dataStrList:
            Str ='{' + dataStr + '}'
            oldDict = ast.literal_eval(Str)
            newDict = dict()
            newDict["index"] = oldDict["index"] + 1
            newDict["article"] = oldDict["word"]
            newDict["info"] = oldDict["desc"]
            newDict["link"] = oldDict["url"]
            newDict["img"] = oldDict["img"]
            newsList.append(newDict)
    except KeyError:
        print("#ERROR>未找到数据字典中的键，原网站数据字典可能已经改变")
        return None
    print("#SUCCESS>新数据字典已提取")   
    return newsList


# 生成MD文件字符串
def getMD(newsList):
    print('#>>>MD文件生成中...>>>')
    nowTime = datetime.datetime.now()
    nowTimeStr1 = nowTime.strftime('%Y/%m/%d %H:%M:%S')
    nowTimeStr2 = nowTime.strftime('%Y年%m月%d日 %H:%M:%S')
    colorList = ["red", "green", "blue"]

    newsMDStr = "---\ntitle: 每日新闻\ndate: {}\n---\n".format(nowTimeStr1)
    newsMDStr += '\n# ' + nowTimeStr2 + '\n'

    for i in range(len(newsList)):
        if i < 3:
            newsMDStr += "\n ## [<font color= {} >{} .{}</font>]({})<br><br>".format(colorList[i], str(newsList[i]["index"]), newsList[i]["article"], newsList[i]["link"])
        else:
            newsMDStr += "\n ### {} .[{}]({}) <br><br>".format(str(newsList[i]["index"]), newsList[i]["article"], newsList[i]["link"])
        newsMDStr += r'<img src="{}" width = 60% height = 60% align= "middle"/><br><br>'.format(newsList[i]["img"])
        if newsList[i]["info"] == "":
            newsMDStr += "> 暂无详细消息<br><br>"
        else:
            newsMDStr += "> {}<br><br>".format(newsList[i]["info"])
    newsMDStr += '**信息来源来自百度热榜，本网站不对真实性负责**\n'
    return newsMDStr


# 保存MD文件
def writeMD(newsMDStr):
    f = open(savePath,"w",encoding="utf-8")
    f.write(newsMDStr)
    print("#SUCCESS>MD文件已生成")   