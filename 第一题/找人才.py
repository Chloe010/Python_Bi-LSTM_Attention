import json
import requests
import numpy as np
import pandas as pd
import xlwt

# 爬取找人才网站的相关页面
# 准备网址路径
url = "https://www.5iai.com/api/resume/baseInfo/public/es?pageSize=10910&pageNumber=1&function=&skills=&workplace=&keyword="
headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
# 获取链接
response = requests.get(url=url, headers=headers)
personData = json.loads(response.text)

# 将爬取到的数据保存到json文件中
with open('person.json', 'w', encoding='utf-8') as f:
    jsonJ = json.dumps(response.json(), ensure_ascii=False)
    f.write(jsonJ)
    
'''
    查看json文件可知：
    "totalElements": "10908"-“找人才”网站总共10908条应聘者数据
    "totalPages": 1091-总共爬取网页分页1091页。
'''

# 获取json文件中的目标数据并保存到列表中
personData1 = []
for i in personData['data']['content']:
    p_id = i['id']  # 人才id
    personData1.append(p_id)
    username = i['username']  # 姓名
    personData1.append(username)
    gender = i['gender']  # 性别 0-男 1-女
    personData1.append(gender)
    exp = i['exp']  # 工作经验
    personData1.append(exp)
    expectPosition = i['expectPosition']  # 应聘工作岗位
    personData1.append(expectPosition)
    willSalaryStart = i['willSalaryStart']  # 最低薪资期望
    personData1.append(willSalaryStart)
    willSalaryEnd = i['willSalaryEnd']  # 最高薪资期望
    personData1.append(willSalaryEnd)
    city = i['city']  # 所在城市
    personData1.append(city)
    updateTime = i['updateTime']  # 上传时间
    personData1.append(updateTime)

    '''
        关于“个人技能”字段的爬取，由于不是每一位应聘者都会拥有，而且拥有的技能的数量也不等，所以以下我做了很多判断：
        根据代码统计：len(labelName['labelName'].max()),
        应聘者拥有技能数额最多是8个，最少是0个。
        需要根据“labelName”字段的长度去做不同的存储操作，防止存储过程中多存或者漏存的现象
        保证数据的准确性。
    '''

    labelName = i['skillMedalList']  # 个人技能
    if labelName:
        if len(labelName) == 0:
            personData1.append('None')
        elif len(labelName) == 1:
            a = labelName[0]['labelName']
            skillMedalList = [a]
            personData1.append(skillMedalList)
        elif len(labelName) == 2:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            skillMedalList = [a, b]
            personData1.append(skillMedalList)
        elif len(labelName) == 3:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            c = labelName[2]['labelName']
            skillMedalList = [a, b, c]
            personData1.append(skillMedalList)
        elif len(labelName) == 4:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            c = labelName[2]['labelName']
            d = labelName[3]['labelName']
            skillMedalList = [a, b, c, d]
            personData1.append(skillMedalList)
        elif len(labelName) == 5:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            c = labelName[2]['labelName']
            d = labelName[3]['labelName']
            e = labelName[4]['labelName']
            skillMedalList = [a, b, c, d, e]
            personData1.append(skillMedalList)
        elif len(labelName) == 6:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            c = labelName[2]['labelName']
            d = labelName[3]['labelName']
            e = labelName[4]['labelName']
            f = labelName[5]['labelName']
            skillMedalList = [a, b, c, d, e, f]
            personData1.append(skillMedalList)
        elif len(labelName) == 7:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            c = labelName[2]['labelName']
            d = labelName[3]['labelName']
            e = labelName[4]['labelName']
            f = labelName[5]['labelName']
            g = labelName[6]['labelName']
            skillMedalList = [a, b, c, d, e, f, g]
            personData1.append(skillMedalList)
        elif len(labelName) == 9:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            c = labelName[2]['labelName']
            d = labelName[3]['labelName']
            e = labelName[4]['labelName']
            f = labelName[5]['labelName']
            g = labelName[6]['labelName']
            h = labelName[7]['labelName']
            skillMedalList = [a, b, c, d, e, f, g, h]
            personData1.append(skillMedalList)
        elif len(labelName) == 10:
            a = labelName[0]['labelName']
            b = labelName[1]['labelName']
            c = labelName[2]['labelName']
            d = labelName[3]['labelName']
            e = labelName[4]['labelName']
            f = labelName[5]['labelName']
            g = labelName[6]['labelName']
            h = labelName[7]['labelName']
            i = labelName[8]['labelName']
            j = labelName[9]['labelName']
            skillMedalList = [a, b, c, d, e, f, g, h, i, j]
            personData1.append(skillMedalList)
    else:
        personData1.append('None')
'''
    由于数据在列表中虽然是顺序，但并没有如字典那般对应到每一个应聘者，
    则按照每一个应聘者均拥有10个特征字段的特性
    将每10个特征分别拆开存储到另外一个列表中，也就是对应到每个应聘者。
'''
col_list = []
for col in range(0, 10908):
    col_list.append(personData1[10 * col:10 + 10 * col])
# print(col_list)  # 检查输出结果无误

# 保存到文件中
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
# 设置表名
sheet = book.add_sheet('找人才', cell_overwrite_ok=True)
# 设置列名
col = ("人才id", "姓名", "性别", "工作经验", "应聘工作岗位", "最低薪资期望", "最高薪资期望", "所在城市", "上传时间", "个人技能")
# 将列名先列式存储到文件中
for i in range(0, 10):
    sheet.write(0, i, col[i])

# 对目标数据进行存储
for i in range(0, 10908):
    print("第%d条" % i)
    data = col_list[i]
    for j in range(0, 10):
        sheet.write(i + 1, j, data[j])
# 文件保存
book.save('F:/找人才.csv')
