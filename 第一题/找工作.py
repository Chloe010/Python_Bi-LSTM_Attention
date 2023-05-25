import json
import requests
import xlwt

# 动态爬虫-交互

'''
爬虫基本思路
1、首先确认爬取的网站是静态还是动态
    请求头：将python代码伪装成浏览器，对服务器发出请求，防止服务器识别出来爬虫脚本
    若爬取vip用户的网站需要加上cookie-登录信息。
# import urllib.request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
    url="https://www.5iai.com/#/jobList"
    req=urllib.request.Request(url=url,data=data,headers=headers,method="POST")
    r = urllib.request.urlopen(req)
    print(r.read().decode("utf-8"))

2、根据爬取的网站得到一些头部信息和body的JavaScript跳转链接得知：爬虫网站需要用到动态爬虫
3、根据网页检查network得到规律，爬取的两大网站规律如以下：
    pageNumber=n 表示浏览的页面为分页模块的第几页面
    pageSize=n   表示浏览的页面每一页有多少条数据
    &以后为访问网站的方法参数
    
    找工作：
    https://www.5iai.com/api/enterprise/job/public/es?pageSize=10&pageNumber=1&willNature=&function=&wageList=%255B%255D&workplace=&keyword=
    找人才：
    https://www.5iai.com/api/resume/baseInfo/public/es?pageSize=10&pageNumber=1&function=&skills=&workplace=&keyword=
    
4、将爬取到的动态网页存储为可视化json文件方便接下来对目标数据的获取和分析
5、使用正则表达式解析数据
6、保存数据
'''

'''
    爬取找工作网站的代码如下：
    通过浏览可知找工作网站的有158个分页，每个分页有10条数据
    为了方便将爬取的数据存储在单一的json文件，我将pageSize干脆设置为158*10=1580，这样就可以在一个页面显示所有数据。
'''

# （1）发送get请求
url = "https://www.5iai.com/api/enterprise/job/public/es?pageSize=1580&pageNumber=1&willNature=&function=&wageList=%255B%255D&workplace=&keyword="

"""
    请求头：将python代码伪装成浏览器，对服务器发出请求，防止服务器识别出来爬虫脚本
    若爬取vip用户的网站需要加上cookie-登录信息。
"""
headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
response = requests.get(url=url, headers=headers)
"""
    print(response)
    返回状态码200-请求成功。
"""

# （2）获取数据 响应体的文本数据
wordData = json.loads(response.text)
# print(name)  检查输出内容没有问题

# （3）将请求到的数据存储为json文件方便查阅
with open('work.json', 'w', encoding='utf-8') as f:
    jsonJ = json.dumps(response.json(), ensure_ascii=False)
    f.write(jsonJ)

# （4）提取有效数据到列表中
'''
    提取数据的基本思路：
        1、通过浏览json文件得知：
            work.json文件的数据布局：status-状态码；message-操作信息；data-爬取数据；以及一些页面数据和操作数据
            很快我们直接定位到data下去解析我们需要的数据即可。
        2、到data下获取目标数据
            我们需要的"工作id", "工作更新时间", "工作岗位名称", "工作岗位最低工资", "工作岗位最高工资", "工作岗位要求经验", 
            "工作岗位要求学历", "工作岗位招收人数", "工作岗位具体地址","公司名称", "公司所属类型", "公司成立模式", "公司规模"等
            数据大部分分布在data下的”content“目录下，直接通过列表索引或者切片索引即可获取。
        3、将获取到的所有岗位数据根据id划分到每一个列表子目录下
            其中：找工作网站有1574条岗位招聘数据，共获取13个字段特征
                 找人才网站有10908条人才投递数据，共获取9个字段特征
        4、根据id排序划分到的总列表，将其保存到excel文件中方便后续解析数据
            其中：”找工作.xls“共有1574行，13列数据
                 ”找人才.xls“共有10908行，9列数据
'''
# （4.1）将所有获取带的数据存入wordData1列表
wordData1 = []
for i in wordData['data']['content']:
    w_id = i['id']  # 工作id
    wordData1.append(w_id)
    updateTime = i['updateTime']  # 工作更新时间
    wordData1.append(updateTime)
    positionName = i['positionName']  # 工作岗位名称
    wordData1.append(positionName)
    minimumWage = i['minimumWage']  # 工作岗位最低工资
    wordData1.append(minimumWage)
    maximumWage = i['maximumWage']  # 工作岗位最高工资
    wordData1.append(maximumWage)
    exp = i['exp']  # 工作岗位要求经验
    wordData1.append(exp)
    educationalRequirements = i['educationalRequirements']  # 工作岗位要求学历 0-不限 2-大专 3-本科 4-硕士 5-博士
    wordData1.append(educationalRequirements)
    count = i['count']  # 工作岗位招收人数
    wordData1.append(count)
    enterpriseAddress = i['enterpriseAddress']['detailedAddress']  # 工作岗位具体地址
    wordData1.append(enterpriseAddress)
    shortName = i['enterpriseExtInfo']['shortName']  # 公司名称
    wordData1.append(shortName)
    industry = i['enterpriseExtInfo']['industry']  # 公司所属类型
    wordData1.append(industry)
    econKind = i['enterpriseExtInfo']['econKind']  # 公司成立模式
    wordData1.append(econKind)
    personScope = i['enterpriseExtInfo']['personScope']  # 公司规模
    wordData1.append(personScope)
# print(wordData1)

# （4.2）将wordData1列表中的数据根据id划分为子列表
col_list = []
for col in range(0, 1574):
    col_list.append(wordData1[13*col:13+13*col])
print(col_list)


# （5）保存数据到excel中，文件名字为”找工作.xls“，表名字为”找工作“。
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('找工作', cell_overwrite_ok=True)
col = ("工作id", "工作更新时间", "工作岗位名称", "工作岗位最低工资", "工作岗位最高工资", "工作岗位要求经验", "工作岗位要求学历", "工作岗位招收人数", "工作岗位具体地址",
       "公司名称", "公司所属类型", "公司成立模式", "公司规模")
for i in range(0, 13):
    sheet.write(0, i, col[i])
for i in range(0, 1574):
    print("第%d条" % i)
    data = col_list[i]
    for j in range(0, 13):
        sheet.write(i + 1, j, data[j])
book.save('F:/找工作.xls')

'''
找工作网站中总共有1574条数据
'''
