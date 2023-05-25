import json
import requests
import urllib.request
import xlwt
import os
import pandas as pd

# 定义文件路径
path = 'F:/c题爬虫/'

# 打开文件,r是读取,encoding是指定编码格式
# 首先获取爬取好的work.json文件，因为以下爬取的网站页面需要该文件中每个岗位的具体id
with open(path + 'work.json', 'r', encoding='utf-8') as fp:
    # print(type(fp))  # 输出结果是 <class '_io.TextIOWrapper'> 一个文件类对象
    # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
    data = json.load(fp)
    # print(type(data))  # 输出结果是 <class 'dict'> 一个python对象,json模块会根据文件类对象自动转为最符合的数据类型,所以这里是dict
fp.close()

# 获取所有岗位id，并将id存储到列表“work_id”中存储
'''
    https://www.5iai.com/api/enterprise/job/public?id=1613439183576236032
    岗位详情的页面
    “1613439183576236032”：这一串就是岗位id
    直接获取岗位id去爬取岗位详情页面的岗位所需技能
'''
word_id = []
word_label = []
a = ['None']  # 给予空值列表，若不是列表而是字符串的话后期存储会出现问题
for i in data['data']['content']:
    w_id = i['id']  # 工作id
    word_id.append(w_id)

# 拼接字符串url-访问链接去爬取岗位详情页面的数据
for j in range(len(word_id)):
    id_url = "https://www.5iai.com/api/enterprise/job/public?id=" + str(word_id[j])
    response = requests.get(url=id_url)  # 获取页面
    path = str(j) + '.json'  # 拼接存储json文件的路径

    # 将获取到的岗位详情信息存储到json文件中方便读取
    with open(path, 'w', encoding='utf-8') as f:
        jsonJ = json.dumps(response.json(), ensure_ascii=False)
        f.write(jsonJ)
        # 获取json文件数据
        wordLabel = json.loads(response.text)

        # 获取目标数据 - 岗位要求具备的技能
        '''
            由于在爬取岗位详情页面的过程中发现在第91个页面后出现大量的完全空页
            也就是说页面并没有出现任何信息，但不能使用空值判断
            则通过代码观察min(os.path.getsize(path))发现完全空页的文件大小在44-48字节之中
            那么直接对文件大小进行判断
            文件大于50字节且拥有关键的目标值才对其进行处理
            否则均给空值
            
        '''
        aaa = os.path.getsize(path)
        if aaa > 50:
            if wordLabel['data']['skillsList']:
                label_name = wordLabel['data']['skillsList']
                if label_name:
                    aa = []
                    for i in label_name:
                        aa.append(i['labelName'])
                    word_label.append(aa)
                else:
                    word_label.append(a)
            else:
                word_label.append(a)
        else:
            word_label.append(a)
print(word_label)

# 保存数据
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('岗位技能', cell_overwrite_ok=True)
col = "岗位技能"
for i in range(0, 1):
    sheet.write(0, i, col[i])
for i in range(0, len(word_id)):
    print("第%d条" % i)
    data = word_label[i]
    for j in range(0, 1):
        sheet.write(i + 1, j, data[j])
book.save('F:/找工作_岗位技能.csv')

# 合并文件
gangwei = pd.read_csv('F:/c题爬虫/找工作_岗位技能.csv')
work = pd.read_csv('F:/c题爬虫/找工作.csv')
df = pd.concat([gangwei, work], axis=0)  # 按行合并两个文件按数据
df.to_csv('F:/c题爬虫/找工作.csv')
