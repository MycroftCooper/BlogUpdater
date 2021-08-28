import os
import ast
import time
import threading
import news_spider
import weather_spider

settingDict = dict()
cityUrlDict = dict()

# 读取设置字典
def readSettingDict():
    global settingDict, cityUrlDict
    settingDataStr = ""
    try:
        f = open("./setting_data.data", 'r', encoding="utf8")
        settingDataStr = f.read()
    except FileExistsError:
        print("ERROR>>setting_data.data文件丢失!")
        return False
    settingDataStrs = settingDataStr.split("###")
    settingDict = ast.literal_eval(settingDataStrs[0])
    cityUrlDict = ast.literal_eval(settingDataStrs[1])
    return True

# 更新hexo博客
def updateBlog():
    os.chdir(settingDict["BlogPath"])
    os.system('hexo clean')
    os.system('hexo d')

if __name__ == "__main__":
    time_start=time.time()
    readSettingDict()
    
    news_spider.savePath = settingDict["NewsPagePath"]
    weather_spider.savePath = settingDict["WeatherPagePath"]

    newsSpiderThreading = threading.Thread\
        (target = news_spider.runNewsSpider)
    weatherSpiderThreading = threading.Thread\
        (target = weather_spider.runWeatherSpider, args = (settingDict["City"], cityUrlDict[settingDict["City"]]))
    newsSpiderThreading.start()
    weatherSpiderThreading.start()
    
    while True:
        if threading.active_count() == 1:
            updateBlog()
            break
        if time.time()-time_start > 20:
            print("ERROR>已超时!")
            break
    time_end=time.time()
    print('\n\n>>>Done!<<<\n总用时>',time_end-time_start)
    input("按任意键退出...")
    