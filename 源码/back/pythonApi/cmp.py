import sys
sys.path.append("D:/resume/pythonApi/")
import re
from LAC import LAC
from collections import OrderedDict
from paddlenlp import Taskflow
import pandas as pd
from tqdm import tqdm
import NERModel.extract as extract
import jieba
unknown = 'UN'
informationPath="D:/resume/pythonApi/information_extraction"
trainPath = "D:/resume/pythonApi/训练数据/"
truthPath = "D:/resume/pythonApi/简历标注.xlsx"
# lac = LAC(mode="lac")

def searchNameByLAC(sentences: str):     
    # 进行xml形式处理
    sentences = '<w:t>' + sentences
    sentences = sentences.replace("\n", "</w:t><w:t>")
    #删除空格
    sentences = re.sub('</w:t><w:t> </w:t><w:t>','',sentences)
    # 装载LAC模型
    user_name_list = []
    lac_result = lac.run(sentences)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "PER":
            user_name_list.append(lac_result[0][index])

    # 将列表元素作为OrderedDict的键创建一个新字典
    d = OrderedDict.fromkeys(user_name_list)
    # 将OrderedDict的键转换为列表，即为去重后的列表
    user_name_list = list(d.keys())

    #对新提取的结果进行必要的过滤

    #删除实际内容小于1的字符串
    lst = [item for item in user_name_list if re.search(r'[^><\s]{2,}', item)]
    #删除实际内容包括英文的字符串
    res_lst = [item for item in lst if not re.search(r'[a-zA-Z0-9]', item)]

    res = ''

    if (len(res_lst) == 0): res = unknown
    else:
        result = re.findall(r'[\u4e00-\u9fff]+', res_lst[0])
        result = ''.join(result)
        res = result.strip()
    return res

def searchNameByUIE(sentences: str):     
    # 进行xml形式处理
    sentences = '<w:t>' + sentences
    sentences = sentences.replace("\n", "</w:t><w:t>")
    #删除空格
    sentences = re.sub('</w:t><w:t> </w:t><w:t>','',sentences)
    schema = ['姓名']
    func = Taskflow("information_extraction", schema=schema, task_path=informationPath)
    result = func(sentences)
    res = unknown
    if len(result) > 0:
        if '姓名' in result[0]:
            res = result[0]['姓名'][0]['text']
    return res

def searchNameByBERT(sentences:str):
    # sentences = re.sub(r'\s','',sentences)
    # print(sentences)
    senlist = re.findall(r'[\u4e00-\u9fff]+',sentences)
    sentences = ''.join(senlist)
    result = extract.information("姓名",sentences)
    if len(result) > 3:
        result = extract.information("姓名",result)
    return result

def searchDegreeByBERT(text):
    text = re.sub('\s','',text)
    senlist = re.findall(r'[\u4e00-\u9fff]+',text)
    sentences = ''.join(senlist)
    education_background_result = ""
    education_background = ['中专','大专','本科','本科生','本科专业','硕士','硕士专业','硕士生','博士','博士生']
    tex = list(jieba.cut(text))
    if text.find('职业技术学院')!=-1 or text.find('职业学院')!=-1 or text.find('专科学校')!=-1:
        education_background_result = '大专'
    for j in range(len(education_background)):
        if education_background[j] in tex:
            education_background_result = education_background[j][0:2]
    if education_background_result == '':
        education_background_result = extract.information("学历",sentences)
        education_background_result = education_background_result[:2]
    if re.search(r'大学|学士',education_background_result):
        education_background_result = '本科'
    if re.search(r'大学|学士',sentences) and education_background_result not in ['本科','硕士','博士']:
        education_background_result = '本科'
    return education_background_result

# 提取历史职位
def searchOffice(text):
    schema = ['职务']
    func = Taskflow("information_extraction", schema=schema, task_path=informationPath)
    result = func(text.replace('\n',''))
    res = []
    if len(result) > 0:
        if '职务' in result[0]:
            for t in result[0]['职务']:
                res.append(t['text'])
    target = r'求\s*职\s*(?:目\s*标\s*|意\s*向\s*|方\s*向\s*)[:：/]{0,1}\s*(\S{0,15})\s'
    res = re.findall(target,text) + res
    job = []
    for j in res:
        j = re.sub(' ','',j)
        if '党员' in j:
            continue
        if j not in job:
            job.append(j)        
    return job[0]
    
def searchJobByBERT(text:str):
    sentences = re.sub(r'\s','',text)
    sentences = re.sub(r'党员','',sentences)
    result = extract.information("职称",sentences)
    if result == 'UN':
        target = r'求\s*职\s*(?:目\s*标\s*|意\s*向\s*|方\s*向\s*)[:：/]{0,1}\s*(\S{0,15})\s'
        if re.search(target,text):
            result = re.findall(target,text)[0]
    return result


def get_chinese_universities(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        universities = [line.strip() for line in file.readlines()]
    return universities

def extract_university_name(sentence, universities):
    escaped_universities = [re.escape(university) for university in universities]
    # 为大学名称创建正则表达式模式
    pattern = r"(?<![.])({})(?![.])".format("|".join(escaped_universities))
    # 从输入句子中查找匹配的大学名称
    matches = re.findall(pattern, sentence)
    return matches

schoolNamesFile = "D:/resume/pythonApi/大学名录.txt"

# 提取毕业院校
#schema = ['毕业院校']
#func = Taskflow("information_extraction", schema=schema, task_path=informationPath)
#universities = get_chinese_universities(schoolNamesFile)
def searchSchool(text):
    '''
    text = re.sub('\n','',text)
    education_graduate_school_result = ""
    result = extract_university_name(text,universities)
    if len(result) > 0:
        education_graduate_school_result = result[0]
    else:
    '''
    text = re.sub('\s','',text)
    result = func(text)
    if len(result) > 0:
        if '毕业院校' in result[0]:
            education_graduate_school_result = result[0]['毕业院校'][0]['text']
        else:
            education_graduate_school_result = unknown
    else:
        education_graduate_school_result = unknown
    return education_graduate_school_result


def searchWorkYears(text,age,degree):
    '''提取工作时长'''
    text = re.sub(r'\s','',text)
    target1 = r'(20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?[-到–一——]+20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?)'
    target2 = r'(20\d{2}(?:年(?:0\d|1[0-2]|\d)?月?)?[-到–一——]+20\d{2}(?:年(?:0\d|1[0-2]|\d)?月?)?)'
    target3 = r'\S{0,30}?(?:实习|兼职)\S{0,30}?'
    target5 = r'\S{0,30}?(?:大学|学院|学校|教育背景|校园|社长|主席|社团)\S{0,30}?'
    target6 = r'20\d{2}[年.]{1}(?:0\d|1[0-2]|\d)?月?[-到–一——]*[至今]{1,2}'
    target7 = r'((?:0\d|1[0-2]|\d)\.20\d{2})'
    target8 = r'(20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?)(20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?)'
    if re.search(target7,text):
        tmp = re.findall(target7,text)
        for line in tmp:
            line1 = re.split(r'[.]',line)[1] + '.' + re.split(r'[.]',line)[0]
            text = re.sub(line,line1,text)
        text = re.sub(target8,r'\1' + '-' + r'\2',text)
    if re.search(target6,text):
        tmp = re.findall(target6,text)[0]
        tmp = re.sub(r'[-到–一——]*[至今]{1,2}','-2023.4',tmp)
        text = re.sub(target6,tmp,text)
    times = re.findall(target1,text) + re.findall(target2,text)
    times = sorted(list(set(times)))
    border = 2023
    if degree == '本科':
        border -= (age - 22)
    elif degree == '硕士':
        border -= (age - 25)
    elif degree == '博士':
        border -= (age - 28)
    elif degree == '大专':
        border -= (age - 21)
    elif degree == '中专':
        border -= (age - 18)
    months = 0
    acc = [] 
    useless = []
    for i in range(len(times)):
        line = times[i]
        year1,year2,month1,month2 = 0,0,0,0
        line1 = re.sub(r'年','.',line)
        line1 = re.sub(r'月','',line1)
        yearS,yearE = re.findall(r'20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?',line1)
        if yearS[-1] == '.':
            yearS = yearS[:-1]
        if yearE[-1] == '.':
            yearE = yearE[:-1]
        if '.' in yearS:
            year1,month1 = yearS.split('.')
        if '.' in yearE:
            year2,month2 = yearE.split('.')
        tmp = (int(year2) - int(year1)) * 12 + (int(month2) - int(month1))
        if int(year2) <= border:
            useless.append(line)
            continue
        elif int(year1) > border:
            if re.search(target3 + line,text) or re.search(line + target3,text):
                useless.append(line)
                continue
        else:
            if re.search(target5 + line,text) or re.search(line + target5,text):
                useless.append(line)
                continue
            if re.search(target3 + line,text) or re.search(line + target3,text):
                useless.append(line)
                continue
        break
    for line in times:
        if line not in useless:
            acc.append(line)
    yearS = yearE = ''
    if len(acc) > 0:
        line1 = re.sub(r'年','.',acc[0])
        line1 = re.sub(r'月','',line1)
        line2 = re.sub(r'年','.',acc[-1])
        line2 = re.sub(r'月','',line2)
        yearS = re.findall(r'20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?',line1)[0]
        yearE = re.findall(r'20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?',line2)[1]
    year1,year2,month1,month2 = 0,0,0,0
    if '.' in yearS:
        year1,month1 = yearS.split('.')
    if '.' in yearE:
        year2,month2 = yearE.split('.')
    if month1 == '':
        month1 = 0
    if month2 == '':
        month2 = 0
    months = (int(year2) - int(year1)) * 12 + (int(month2) - int(month1))
    if months % 12 == 0:
        return int(months / 12)
    else:
        return int(months / 12) + 1

# 提取年龄
def searchAge(datatext):
    datatext = re.sub(r'\s','',datatext)
    if re.search(r'年龄[:：]{0,1}([1-5]\d{1})',datatext):
        age = re.findall(r'年龄[:：]{0,1}([1-5]\d{1})',datatext)[0]
        return int(age)
    elif re.search(r'[1-5]\d{1}岁',datatext):
        age = re.findall(r'[1-5]\d{1}岁',datatext)[0]
        age = re.sub(r'[岁\s]',"",age)
        return int(age)
    else:
        births = re.findall(r"(?:19|20)\d{2}", datatext)
        births = list(map(int,births))
        births.sort()
        age = 2023 - births[0] + 1 if len(births) > 0 else 2000
        if (age < 18 or age > 60) and re.search(r'(?:18|[2-5]\d)\D',datatext):
            age = re.findall(r'(?:18|[2-5]\d)\D',datatext)[0]
            age = re.sub(r'\D','',age)
        return int(age)

jobs = {
    "产品运营":{
        "name":["产品运营"],
        "work":2,
        "degree":"无",
        "age":18,
    },
    "平面设计师":{
        "name":["平面设计师","平面设计"],
        "work":1,
        "degree":"大专",
        "age":18,
    },
    "财务":{
        "name":["财务","会计"],
        "work":0,
        "degree":"本科",
        "age":18,
    },
    "市场营销":{
        "name":["市场营销"],
        "work":10,
        "degree":"本科",
        "age":18,
    },
    "项目主管":{
        "name":["项目主管","总监","市场管理"],
        "work":3,
        "degree":"本科",
        "age":18,
    },
    "开发工程师":{
        "name":["开发工程师"],
        "work":3,
        "degree":"本科",
        "age":18,
    },
    "文员":{
        "name":["文员","助理"],
        "work":1,
        "degree":"大专",
        "age":25,
    },
    "电商运营":{
        "name":["电商运营"],
        "work":2,
        "degree":"无",
        "age":18,
    },
    "人力资源管理":{
        "name":["人力资源管理"],
        "work":2,
        "degree":"大专",
        "age":18,
    },
    "风控专员":{
        "name":["金融","国际贸易"],
        "work":5,
        "degree":"硕士",
        "age":18,
    },
}
degrees = {"无":-2,"高中":0,"中专":-1,"大专":1,"本科":2,"硕士":3,"博士":4}

def main():
    anslist = [['简历名','正确结果','系统提取结果'],]
    df1 = pd.read_excel(truthPath)
    data1 = df1.values
    cnt1 = 0
    for i in tqdm(range(1,101)):
        jlist = []
        tmpPath = trainPath + str(i) + ".txt"
        text = ''
        with open(tmpPath,'r',encoding="utf-8") as f:
            text = f.read()
        text = ''.join(re.findall(r'[\u4e00-\u9fff]+',text))
        for k,v in jobs.items():
            if v["work"] > data1[i-1,5]:
                continue
            if v["age"] > data1[i-1,2]:
                continue
            if degrees[v["degree"]] > degrees[data1[i-1,3]]:
                continue
            for name in v["name"]:
                if re.search(name,text):
                    jlist.append(k)
                    break 
        slist = str(data1[i-1,6]).split('、')
        
        for s in slist:
            if s in jlist:
                cnt1 += 1
                break
        if len(jlist) == 0 and 'nan' in slist:
            cnt1 += 1
        jstr = '、'.join(jlist)
        anslist.append([i,data1[i-1,6],jstr])
    anslist.append(["正确率",100,cnt1])
    dataframe = pd.DataFrame(anslist)
    dataframe.to_excel("D:/resume/pythonApi/岗位提取结果.xlsx",sheet_name="data",header=0,index=False)

main()  
