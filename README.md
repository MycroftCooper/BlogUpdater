# 卖烤麸烤饼烤馕烤羊肉串烤包子的

# 个人学习用博客自动更新器

项目名称：博客更新器
版本号：2.0.0
更新日期：21.8.28
作者：MycroftCooper
主要语言：Python

主要功能：

- 更新博客内容
- 爬取百度热搜榜新闻信息并更新至博客
- 爬取指定城市七天天气并更新到博客

适用条件：

- 使用hexo框架的博客

使用方法：

1. 下载BlogUpdater.7z并解压
2. 对BlogUpdater目录下的setting_data.data配置文件进行更改：
   - BlogPath
     是hexo博客的根目录
   - NewsPagePath
     是新闻页面在hexo框架下的根目录
   - WeatherPagePath
     是天气页面在hexo框架下的根目录
   - City
     是指定要查询天气的城市
   - ###后的数据字典
     是各个城市名称与对应的局部URL(未全录入)
     如果没有你所在的城市，可以尝试`A省名拼音(大写)/城市拼音(小写)`
3. 将BlogUpdater.exe创建快捷方式至计算机的启动目录下
4. 完成，每次计算机开机时，自动更新博客

各个文件说明:
- BlogUpdater.7z 打包好的exe文件，可以直接使用
- main.py 主入口
- setting_data.data 配置文件，第一次使用需要修改
- news_spider.py 新闻爬虫代码
- weather_spider.py 天气爬虫代码
- weatherPage.css 天气页面输出css样式

效果可见于我的博客: https://mycroftcooper.github.io/
如果对你有所帮助，欢迎Star一下
