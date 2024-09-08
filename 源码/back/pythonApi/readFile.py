import sys
sys.path.append("D:/resume/pythonApi/")
import json
import os
from bs4 import BeautifulSoup
import win32com.client
import pdfplumber
from zipfile import ZipFile
from ecloud import CMSSEcloudOcrClient
import re
from LAC import LAC
from collections import OrderedDict
import jieba
from paddlenlp import Taskflow
import pythoncom
import NERModel.extract as extract

# import Levenshtein
# import synonyms
# from synonyms import *

accesskey = 'd86f24b06bb44b4bb64b70a27340065a' 
secretkey = 'd3be4d031fd8447ea32d226cfb122e97'
url = 'https://api-wuxi-1.cmecloud.cn:8443'

unknown = 'UN'

def similarity(str1,str2):
    if str1 in str2 or str2 in str1:
        return 1
    else:
        count = 0
        for s in str1:
            if s in str2:
                count += 1
        return count / min(len(str1),len(str2))
    
def request_webimage(imagePath):
    requesturl = '/api/ocr/v1/general'
    try:
        ocr_client = CMSSEcloudOcrClient(accesskey, secretkey, url)
        response = ocr_client.request_ocr_service_file(requestpath=requesturl, imagepath= imagePath)
        text = json.loads(response.text)
        if text['errorcode'] == 'AIO.1005':
            return []
        else:
            datalist1 = text['items']
            text = ''
            for data in datalist1:
                text += (data['itemstring'] + '\n')
            return text 
    except ValueError as e:
        print(e)

def extract_university_name(sentence, universities):
    escaped_universities = [re.escape(university) for university in universities]
    # 为大学名称创建正则表达式模式
    pattern = r"(?<![.])({})(?![.])".format("|".join(escaped_universities))
    # 从输入句子中查找匹配的大学名称
    matches = re.findall(pattern, sentence)
    return matches

class ReadFile(object):
    '''抽取单个文件的信息 转化为字符串存储'''
    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.text = ''
        listname = os.path.splitext(self.file_dir)
        if listname[1] in [".doc", ".docx",".pdf",".png",".txt",".jpg",".jpeg"]:
            try:
                if listname[1] == ".doc":
                    self.__doc2docx()
                self.text = self.__extract_text()
            except Exception as e:
                print(e)
                return
    
    def __doc2docx(self):
        '''doc转docx'''
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.AppLication")
        try:
            doc = word.Documents.Open(self.file_dir)
            new_path = os.path.splitext(self.file_dir)[0] + '.docx'
            doc.SaveAs(new_path, 16)  # 16 表示将文件保存为 docx 格式
            doc.Close()
            os.remove(self.file_dir)
            self.file_dir = new_path
            pythoncom.CoUninitialize()
            return self.file_dir
        except Exception as e:
            print("Error:", e)
            return None
        
    def __extract_text(self):
        '''抽取文本内容'''
        text = ''
        listname = os.path.splitext(self.file_dir)
        if listname[1] == '.docx':
            document = ZipFile(self.file_dir)
            xml = document.read("word/document.xml")
            wordObj = BeautifulSoup(xml.decode("utf-8"),features='xml')
            #用来删除fallback标签，实现内容去重
            fallback_tags = wordObj.find_all("mc:Fallback")
            for fallback_tag in fallback_tags:
                fallback_tag.decompose()
            texts = wordObj.findAll("w:t")
            for t in texts:
                text += (t.text + '\n')
        elif listname[1] == '.pdf':
            with pdfplumber.open(self.file_dir) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() if page.extract_text() else ""
        elif listname[1] == '.png' or listname[1] == '.jpg' or listname[1] == '.jpeg':
            text = request_webimage(self.file_dir)
        elif listname[1] == '.txt':
            with open(self.file_dir,'r',encoding='utf-8') as f:
                text = f.read()
        return text


class Extractor(object):
    '''提取字符串里的信息 姓名 年龄 学历 毕业院校 工作时长 性别 职位 政治面貌 籍贯 专业 工作单位 联系方式(电话 email) 技能 证书 介绍 教育时间'''
    def __init__(self, text, chinese_universities, lac:LAC,information):
        self.chinese_universities = chinese_universities
        self.information_extraction = information
        self.lac = lac

        self.text = text
        #self.name,self.school,self.office,self.origin,self.major,self.company = self.searchpaddlenlp(text)
        self.name = self.searchName(text)
        self.age = self.searchAge(text)
        self.degree = self.searchDegree(text)
        self.school = self.searchSchool(text)
        self.workTime = self.searchWorkYears(text,self.age,self.degree)
        self.gender = self.searchGender(text)
        self.office = self.searchOffice(text)
        self.id = self.searchId(text)
        self.origin = self.searchOrigin(text)
        self.major = self.searchMajor(text)
        self.company = self.searchCompany(text)
        self.calls = self.searchCall(text)
        self.skills = self.searchSkill(text)
        self.rewardNums = self.searchReward(text)
        self.access = self.searchAccess(text)
        self.schoolTime = self.searchSchoolTime()
        self.schoolLevel = self.JudgeSchool()
        self.jobs = self.classifyJob()
        

    # 提取姓名
    def searchName(self,sentences: str) -> list:
        # 进行xml形式处理
        sentences = '<w:t>' + sentences
        sentences = sentences.replace("\n", "</w:t><w:t>")
        #删除空格
        sentences = re.sub('</w:t><w:t> </w:t><w:t>','',sentences)
        schema = ['姓名']
        func = Taskflow("information_extraction", schema=schema, task_path=self.information_extraction)
        result = func(sentences)
        if len(result) > 0:
            if '姓名' in result[0]:
                result = result[0]['姓名'][0]['text']
        else:     
            senlist = re.findall(r'[\u4e00-\u9fff]+',sentences)
            sentences1 = ''.join(senlist)
            result = extract.information("姓名",sentences1)
            if len(result) > 3:
                result = extract.information("姓名",result)
        return result
    
    # 提取年龄
    def searchAge(self,datatext):
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
    
    # 提取学历
    def searchDegree(self,text):
        text = re.sub('\n','',text)
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
        elif education_background_result not in ['本科','硕士','博士']:
            education_background_result = '高中'
        return education_background_result
    
    # 提取毕业院校
    def searchSchool(self,text):
        schema = ['毕业院校']
        text = re.sub('\n','',text)
        education_graduate_school_result = ""
        result = extract_university_name(text, self.chinese_universities)
        if len(result) > 0:
            education_graduate_school_result = result[0]
        else:
            func = Taskflow("information_extraction", schema=schema, task_path=self.information_extraction)
            result = func(text)
            if len(result) > 0:
                if '毕业院校' in result[0]:
                    education_graduate_school_result = result[0]['毕业院校'][0]['text']
                else:
                    education_graduate_school_result = unknown
            else:
                education_graduate_school_result = unknown
        return education_graduate_school_result
    
    def searchWorkYears(self,text,age,degree):
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
        
    # 提取性别
    def searchGender(self,text):
        if re.search('女',text):
            return '女'
        else:
            return '男'
    
    # 提取历史职位
    def searchOffice(self,text):
        schema = ['职务']
        func = Taskflow("information_extraction", schema=schema, task_path=self.information_extraction)
        result = func(text.replace('\n',''))
        sentences = re.sub(r'\s','',text)
        res = []
        if len(result) > 0:
            if '职务' in result[0]:
                for t in result[0]['职务']:
                    res.append(t['text'])
        else:
            r = extract.information("职称",sentences)
            res.append(r)
        target = r'求\s*职\s*(?:目\s*标\s*|意\s*向\s*|方\s*向\s*)[:：/]{0,1}\s*(\S{0,15})\s'
        res = re.findall(target,text) + res
        job = []
        for j in res:
            j = re.sub(' ','',j)
            if '党员' in j:
                continue
            if j not in job:
                job.append(j)        
        return job
    
    # 提取政治面貌
    def searchId(self,text):
        if re.search('党员',text):
            return '党员'
        else:
            return '群众'
    
    # 提取籍贯
    def searchOrigin(self,text):
        target = r'(?:籍\s*贯\s*)[:：/]{0,1}\s*(\S{0,10})\s'
        res = ''
        if re.search(target,text):
            res = re.findall(target,text)[0]
        else:
            schema = ['籍贯']
            func = Taskflow("information_extraction", schema=schema, task_path=self.information_extraction)
            result = func(text.replace('\n',''))
            if len(result) > 0:
                if '籍贯' in result[0]:
                    res = result[0]['籍贯'][0]['text']
                else:
                    res = unknown
            else:
                res = unknown
        if res == unknown:
            sf = '河北省、山西省、辽宁省、吉林省、黑龙江省、江苏省、浙江省、安徽省、福建省、江西省、山东省、\
            河南省、湖北省、湖南省、广东省、海南省、四川省、贵州省、云南省、陕西省、甘肃省、青海省、台湾省、\
                内蒙古自治区、广西壮族自治区、西藏自治区、宁夏回族自治区、新疆维吾尔自治区、北京市、天津市、上海市、重庆市、香港、澳门'.split('、')
            alltext = ''.join(re.findall(r'[\u4e00-\u9fff]+',text))
            for s in sf:
                if re.search(s[:2],alltext):
                    res = s
                    break
        return res
    
    # 提取专业
    def searchMajor(self,text):
        schema = ['专业']
        func = Taskflow("information_extraction", schema=schema, task_path=self.information_extraction)
        result = func(text.replace('\n',''))
        res = ""
        if len(result) > 0:
            if '专业' in result[0]:
                res = result[0]['专业'][0]['text'].replace(' ','')
            else:
                res = unknown
        else:
            sentences = re.sub(r'\s','',text)
            result = extract.information("专业",sentences)
        return res
    
    # 提取任职过的公司
    def searchCompany(self,text):
        schema = ['工作单位']
        func = Taskflow("information_extraction", schema=schema, task_path=self.information_extraction)
        result = func(text.replace('\n',''))
        res = []
        if len(result) > 0:
            if '工作单位' in result[0]:
                for t in result[0]['工作单位']:
                    res.append(t['text'])
        else:
            sentences = re.sub(r'\s','',text)
            result = extract.information("公司",sentences)
            res.append(result)
        job = []
        for j in res:
            j = re.sub(' ','',j)
            if '学校' in j or '学院' in j or '大学' in j:
                continue
            if j not in job:
                job.append(j)
        return job
    
    # 提取联系方式(邮箱 + 电话)
    def searchCall(self,text):
        calls = {}
        text = re.sub(r'[\s-]','',text)
        target1 = r'(1(?:3[0-9]|5[0-3,5-9]|7[1-3,5-8]|8[0-9])\d{8})'
        target2 = r'([0-9a-zA-Z_]+@[0-9a-zA-Z_]+\.(?:com|cn|me|net))'
        target3 = r'(20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?[-到–一——]*20\d{2}(?:\.(?:0\d|1[0-2]|\d)?)?)'
        target4 = r'(20\d{2}(?:年(?:0\d|1[0-2]|\d)?月?)?[-到–一——]*20\d{2}(?:年(?:0\d|1[0-2]|\d)?月?)?)'
        phone = re.findall(target1,text)
        text = re.sub(target1,'',text)
        text = re.sub(target3,'',text)
        text = re.sub(target4,'',text)
        email = re.findall(target2,text)
        if len(phone) > 0:
            calls['phone'] = phone[0]
        else:
            alltext = ''.join(re.findall(r'[\d]+',text))
            phone = re.findall(target1,alltext)
            if len(phone) > 0:
                calls['phone'] = phone[0]
            else:
                calls['phone'] = unknown
        if len(email) > 0:
            calls['email'] = email[0]
        else:
            alltext = ''.join(re.findall(r'[0-9_a-zA-Z@\.]+',text))
            email = re.findall(target2,alltext)
            if len(email) > 0:
                calls['email'] = email[0]
            else:
                calls['email'] = unknown
        return calls    
    
    # 提取个人技能
    def searchSkill(self,text):
        # 技能
        skills = {}
        text = re.sub(r'\s','',text)
        # 普通话技能
        skills['mandarin'] = 0
        mandarin = [['普通话一级甲等',10],['普通话一级乙等',8],['普通话二级甲等',6],['普通话二级乙等',4],['普通话三级甲等',2],['普通话三级乙等',1]]
        for m in mandarin:
            if (re.search(m[0],text)):
                skills['mandarin'] = m[1]
                break
        # 计算机技能
        computer = [['计算机四级', 5],['计算机三级', 3] ,['计算机二级', 2],['计算机一级',1]]
        skills['C'] = 0
        skills['Java'] = 0
        skills['Python'] = 0
        skills['computer'] = 0
        # C语言
        if re.search(r'[cC](?:\+\+|#|)',text):
            skills['C'] = 1
            skills['computer'] += 5
        # Java语言
        if re.search('java|Java',text):
            skills['Java'] = 1
            skills['computer'] += 5
        # Python语言
        if re.search('Python|python',text):
            skills['Python'] = 1
            skills['computer'] += 5
        for c in computer:
            if (re.search(c[0],text)):
                skills['computer'] += c[1]
                break
        # 英语技能
        skills['english'] = ''
        target1 = r'(CET-6|CET-4\/6|英语六级|英语四、六级|英语四\/六级|英语6级|英语4、6级|英语4/6级)'
        target2 = r'(CET-4|英语四级|英语4级)'
        if re.search(target1,text):
            skills['english'] = '六级'
        elif re.search(target2,text):
            skills['english'] = '四级'
        # 平面设计能力
        skills['平面设计'] = 0
        if re.search('平面设计',text):
            skills['平面设计'] += 2
        if re.search('Photoshop|photoshop|[pP][Ss]',text):
            skills['平面设计'] += 2
        if re.search('CorelDraw|corelDraw',text):
            skills['平面设计'] += 2
        if re.search('Illustrator|illustrator',text):
            skills['平面设计'] += 2
        if re.search('Indesign|indesign',text):
            skills['平面设计'] += 2
        # 办公软件掌握程度
        skills['办公软件'] = 0
        skills['word'] = 0
        skills['excel'] = 0
        skills['ppt'] = 0
        if re.search('办公软件',text):
            skills['办公软件'] += 2
        if re.search('Office|office',text):
            skills['办公软件'] += 2
        if re.search('Word|word',text):
            skills['办公软件'] += 2
            skills['word'] = 1
        if re.search('Excel|excel',text):
            skills['办公软件'] += 2
            skills['excel'] = 1
        if re.search('[pP]ower[pP]oint|ppt',text):
            skills['办公软件'] += 2
            skills['ppt'] = 1
        # 剪辑能力
        skills['剪辑'] = 0
        if re.search('剪辑|视频',text):
            skills['剪辑'] += 4
        if re.search('会声会影|绘声绘色',text):
            skills['剪辑'] += 3
        if re.search('Pr',text):
            skills['剪辑'] += 3
        # 沟通能力
        skills['沟通'] = 0
        if re.search('沟通|表达|协调',text):
            skills['沟通'] = 1
        # 执行能力
        skills['执行'] = 0
        if re.search('执行',text):
            skills['执行'] = 1
        # 逻辑思维能力
        skills['逻辑'] = 0
        if re.search('逻辑|规律',text):
            skills['逻辑'] = 1
        # AI能力
        skills['人工智能'] = 0
        if re.search('[aA][iI]|人工智能',text):
            skills['人工智能'] = 1
        return skills
    
    # 提取奖项证书的数量 - 根据岗位要求提取
    def searchReward(self,text):
        text = re.sub(r'\n',' ',text)
        target = r'(\S*(?:奖学金|证书|一等奖|二等奖|三等奖|优秀奖|优秀学生|三好学生|金奖|银奖|铜奖))'
        res = re.findall(target,text)
        return len(res) 
    
    # 提取自我评价 - 根据岗位要求提取
    def searchAccess(self,text):
        textlist = re.split('\n',text)
        res = ''
        for i in range(len(textlist)):
            if re.search(r'本人',textlist[i]):
                res += textlist[i]
                break
            if re.search(r'评\s*价|介\s*绍|总\s*结',textlist[i]):
                if i > 0 : res += textlist[i - 1]
                res += '。'
                if i < len(textlist) - 1: res += textlist[i + 1]
                break
            if re.search(r'尊敬的',textlist[i]):
                for j in range(i,len(textlist)):
                    res += textlist[j]
                    res += '\n'
                break
        return res  
    
    # 推测受教育的时间
    def searchSchoolTime(self):
        birth = 2023 - self.age + 1
        start = end = birth
        if self.degree == '博士':
            start = birth + 25
            end = start + 4
        elif self.degree == '硕士':
            start = birth + 22
            end = start + 3
        elif self.degree == '本科':
            start = birth + 18
            end = start + 4
        elif self.degree == '大专':
            start = birth + 18
            end = start + 3
        elif self.degree == '中专':
            start = birth + 16
            end = start + 3
        return str(start) + '-' + str(end)
    
    # 根据学校名判断是否是985 211
    def JudgeSchool(self):
        s985 = "清华大学、北京大学、厦门大学、中国科学技术大学、南京大学、复旦大学、天津大学、浙江大学、西安交通大学、\
                东南大学、上海交通大学、山东大学、中国人民大学、吉林大学、电子科技大学、四川大学、华南理工大学、兰州大学、\
                西北工业大学、同济大学、哈尔滨工业大学、南开大学、华中科技大学、武汉大学、中国海洋大学、湖南大学、\
                北京理工大学、重庆大学、大连理工大学、中山大学、北京航空航天大学、东北大学、北京师范大学、中南大学、\
                中国农业大学、国防科技大学、西北农林科技大学、华东师范大学、中央民族大学"
        l985 = s985.replace(' ','').split('、')
        s211 = "清华大学、北京大学、中国人民大学、北京交通大学、北京工业大学、北京航空航天大学、北京理工大学、北京科技大学、\
                北京化工大学、北京邮电大学、中国农业大学、北京林业大学、中国传媒大学、中央民族大学、北京师范大学、中央音乐学院、\
                对外经济贸易大学、北京中医药大学、北京外国语大学、中国地质大学（北京）、中国矿业大学（北京）、中国石油大学（北京）、\
                中国政法大学、中央财经大学、华北电力大学、北京体育大学、上海外国语大学、复旦大学、华东师范大学、上海大学、华东大学、\
                上海财经大学、华东理工大学、同济大学、上海交通大学、南开大学、天津大学、天津医科大学、河北工业大学、重庆大学、西南大学、\
                太原理工大学、内蒙古大学、大连理工大学、东北大学、辽宁大学、大连海事大学、吉林大学、延边大学、东北师范大学、哈尔滨工业大学\
                哈尔滨工程大学、东北农业大学、东北农林大学、南京大学、东南大学、苏州大学、南京师范大学、中国矿业大学、中国医药大学、河海大学、\
                南京理工大学、江南大学、南京农业大学、南京航空航天大学、浙江大学、中国科学技术大学、安徽大学、合肥工业大学、厦门大学、福州大学、\
                南昌大学、山东大学、中国海洋大学、中国石油大学、武汉大学、华中科技大学、武汉理工大学、中南财经政法大学、华中师范大学、华中农业大学、\
                中国地质大学、湖南大学、中南大学、湖南师范大学、中山大学、暨南大学、华南理工大学、华南师范大学、广西大学、四川大学、西南交通大学、\
                电子科技大学、四川农业大学、西南财经大学、云南大学、贵州大学、西北大学、西安交通大学、西北工业大学、长安大学、西北农林科技大学、\
                陕西师范大学、西安电子科技大学、兰州大学、海南大学、西藏大学、新疆大学、石河子大学、第二军医大学、第四军医大学、国防科技大学"
        l211 = s211.replace(' ','').split('、')
        if self.school in l985:
            return "985"
        elif self.school in l211:
            return "211"
        else:
            return "其他"
    
    # 根据理想职位进行职务分类
    def classifyJob(self):
        jobs = {"engineer":30,"finance":30,"design":30,"manager":30,"market":30,"hospital":30,"edit":30,"else":30}

        engineer = ["工程","技术"]
        target =  20
        point = 0
        for o in self.office:
            sim = 0
            for e in engineer:
                sim = max(similarity(e, o),sim)
            if sim < 0.01:
                continue
            else:
                point += int(target * sim)
        jobs["engineer"] += min(point,60)

        finance = ["财务","会计","税务","精算","审计","出纳"]
        target =  20
        point = 0
        for o in self.office:
            sim = 0
            for f in finance:
                sim = max(similarity(f, o),sim)
            if sim < 0.01:
                target = max(10,target - 10)
                continue
            else:
                point += int(target * sim)
        jobs["finance"]  += min(point,60)

        design = ["设计师",'设计']
        target =  20
        point = 0
        for o in self.office:
            sim = 0
            for d in design:
                sim = max(similarity(d, o),sim)
            if sim < 0.01:
                continue
            else:
                point += int(target * sim)
        jobs['design'] += min(point,60)

        manager = ["行政管理","经理","总监","主管","管理","行政","人事"]
        target =  20
        point = 0
        for o in self.office:
            sim = 0
            for m in manager:
                sim = max(similarity(m, o),sim)
            if sim < 0.01:
                continue
            else:
                point += int(target * sim)
        jobs["manager"] += min(point,60)

        market = ["运营","营销","市场","客服","产品","销售","推广"]
        target =  20
        point = 0
        for o in self.office:
            sim = 0
            for m in market:
                sim = max(similarity(m, o),sim)
            if sim < 0.01:
                continue
            else:
                point += int(target * sim)
        jobs["market"] += min(point,60)

        hospital = ["医疗","卫生","护理","保健","制药","生物","医护"]
        target = 20
        point = 0
        for o in self.office:
            sim = 0
            for h in hospital:
                sim = max(similarity(h, o),sim)
            if sim < 0.01:
                continue
            else:
                point += int(target * sim)
        jobs["hospital"] += min(point,60)

        edit = ["文员","编辑","助理","职员","接待员","办事员","打杂"]
        target = 20
        point = 0
        for o in self.office:
            sim = 0
            for e in edit:
                sim = max(similarity(e, o),sim)
            if sim < 0.01:
                continue
            else:
                point += int(target * sim)
        jobs["edit"] += min(point,60)

        flag = 0
        for v in jobs.values():
            if v != 30:
                flag = 1
                break
        if flag == 0:
            jobs["else"] += 30
        
        return jobs


    def searchpaddlenlp(self,sentences: str):
        # 进行xml形式处理
        jobtext = sentences
        sentences = '<w:t>' + sentences
        sentences = sentences.replace("\n", "</w:t><w:t>")
        #删除空格
        sentences = re.sub('</w:t><w:t> </w:t><w:t>','',sentences)
        schema = ['姓名','毕业院校','职务','籍贯','专业','工作单位']
        func = Taskflow("information_extraction", schema=schema, task_path=self.information_extraction)
        result = func(sentences)
        name = "刘鑫"
        school = "华中科技大学"
        job = []
        jiguan = "上海市"
        zhuanye = "计算机科学与技术"
        danwei = []
        if len(result) > 0:
            if '姓名' in result[0]:
                name = result[0]['姓名'][0]['text']
            if '毕业院校' in result[0]:
                school = result[0]['毕业院校'][0]['text']
            if '职务' in result[0]:
                for t in result[0]['职务']:
                    x = re.sub(' ','',t['text'])
                    if x != '党员':
                        job.append(x)
            if '专业' in result[0]:
                zhuanye = result[0]['专业'][0]['text'].replace(' ','')
            if '工作单位' in result[0]:
                for t in result[0]['工作单位']:
                    danwei.append(t['text'])
        return name,school,job,jiguan,zhuanye,danwei


        







    

