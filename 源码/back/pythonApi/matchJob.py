import jieba.analyse as ana
import re
import pymysql
import Levenshtein
import jieba

class Extractor(object):
    def __init__(self):
        ana.set_stop_words("D:/resume/pythonApi/stopwords.txt")
    def extract(self,text):
        text = re.sub(r'[0-9]',';',text)
        text = re.sub(r' ','',text)
        seg_list = ana.extract_tags(text)
        return seg_list
class KeyWords(object):
    def __init__(self,mandarin, english, computer, c, java, python,
                 graphicDesign, officeSoftware, word, excel, ppt, pr, communicate,
                 act, logic, ai, reward):
        self.mandarin = mandarin
        self.english = english
        self.computer = computer
        self.c = c
        self.java = java
        self.python = python
        self.graphicDesign = graphicDesign
        self.officeSoftware = officeSoftware
        self.word = word
        self.excel = excel
        self.ppt = ppt
        self.pr = pr
        self.communicate = communicate
        self.act = act
        self.logic = logic
        self.ai = ai
        self.reward = reward

    def to_dict(self):
        return {
            'mandarin': self.mandarin,
            'english': self.english,
            'computer': self.computer,
            'c': self.c,
            'java': self.java,
            'python': self.python,
            'graphicDesign': self.graphicDesign,
            'officeSoftware': self.officeSoftware,
            'word': self.word,
            'excel': self.excel,
            'ppt': self.ppt,
            'pr': self.pr,
            'communicate': self.communicate,
            'act': self.act,
            'logic': self.logic,
            'ai': self.ai,
            'reward': self.reward
        }

class Resumer(object):
    def __init__(self,id,name,age,education,university,schoolLevel,workExperience,targetJob,text,target,company,skill:KeyWords):
        self.id = id
        self.name = name
        self.age = age

        self.education = education
        self.university = university 
        self.schoolLevel = schoolLevel

        self.workExperience = workExperience
        self.targetJob = targetJob
        self.text = text
        self.target = target
        self.company = company
        
        self.skill = skill

        self.score = 0

    def to_dict(self):
        return {
            'id': self.id,
            'name':self.name,
            'age': self.age,
            'education': self.education,
            'university': self.university,
            'schoolLevel': self.schoolLevel,
            'workExperience': self.workExperience,
            'targetJob': self.targetJob,
            'target': self.target,
            'company': self.company,
            'skill': self.skill.to_dict(),
            'score': self.score
        }
 

class Job(object):
    def __init__(self,jobName,ageMax,ageMin,education,workMinTime,text,tfidf:Extractor):
        self.jobName = jobName
        self.education = education
        self.ageMax = ageMax
        self.ageMin = ageMin
        self.workMinTime = workMinTime
        self.text = text
        self.keyWords = tfidf.extract(text)

class MySQL(object):
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.result1 = self.implement("""SELECT id,name,age,text FROM `basic_information`""")
        self.result2 = self.implement("""SELECT id,education,university,schoolLevel FROM `educational_information`""")
        self.result3 = self.implement("""SELECT id,targetJob,workExperience,companies,engineer,finance,design,manager,market,hospital,edit,elseJob FROM `work_information`""")
        self.result4 = self.implement("""SELECT * FROM `skill_information`""")
        self.cursor.close()                     
        self.db.close()
    def connect(self):
        # 连接MySQL数据库
        try:
            db = pymysql.connect(
                host="localhost",
                port=3306,
                user='root',
                passwd='123456',
                db='resume_manager',
                charset='utf8'
                )
            return db
        except Exception:
            raise Exception("数据库连接失败")

    def implement(self,sql):
        # sql4 = """SELECT * FROM `skill_information`"""
        try:
            self.cursor.execute(sql)          
            result = self.cursor.fetchall()                  
            self.db.commit()                 
        except Exception:
            self.db.rollback()                 
            print("查询失败")
        return result

def jobNameScore(jobname,text,jobs):
    '''岗位名匹配'''
    # synlst = synonyms.nearby(jobname,10)[0]
    synlst = jieba.lcut(jobname)
    synlst =  [jobname,] + synlst
    score = 0
    score1 = 80
    for job in synlst:
        if re.search(job,text):
            score += score1
            break
        score1 = max(score1 - 10,50)
    sim = 0
    for job in jobs:
        sim = max(sim,Levenshtein.jaro(job,jobname))
    score += int(20 * sim)
    return score

def ageScore(ageMax,ageMin,age):
    if ageMax < age or ageMin > age:
        return 0
    score = 50
    if age < 35:
        score = 100
    elif age < 40:
        score = 80
    elif age < 50:
        score = 60
    return score

def workTimeScore(workMinTime,workTime):
    if workMinTime > workTime:
        return 0
    score = 50
    if workTime > 5:
        score = 100
    elif workTime > 3:
        score = 80
    elif workTime > 1:
        score = 60
    return score

def eduScore(jedu,redu,rdegree):
    e = {'无':-2,'高中':-1,'中专':0,'大专':1,'本科':2,'硕士':3,'博士':4}
    if redu not in e:
        redu = '高中'
    if e[jedu] > e[redu]:
        return 0
    score = 50
    if e[redu] == 4:
        score = 80
    elif e[redu] == 3:
        score = 60
    if rdegree == '985':
        score += 20
    elif rdegree == '211':
        score += 10
    return score

def skillScore(skills,text):
    count = 0
    for k in skills:
        if re.search('(?i)' + k,text): # 忽略大小写
            count += 1
    score = 0
    if len(skills) > 0:
        score = int(100 * count / len(skills))
    return score

def jobMatch(job:Job,resumer:Resumer):
    '''岗位匹配'''
    jobS = jobNameScore(job.jobName,resumer.text,resumer.targetJob)
    ageS = ageScore(job.ageMax,job.ageMin,resumer.age)
    workS = workTimeScore(job.workMinTime,resumer.workExperience)
    eduS = eduScore(job.education,resumer.education,resumer.schoolLevel)
    skillS = skillScore(job.keyWords,resumer.text)
    score = jobS * 0.454 + ageS * 0.092 + workS * 0.158 + eduS * 0.228 + skillS * 0.068
    if ageS == 0 or workS == 0 or eduS == 0:
        score = 0
    return int(score)


def main(job:Job,tfidf:Extractor):
    a = MySQL()
    resumers = []
    print(len(a.result1) == len(a.result3))
    for i in range(len(a.result1)):
        rid = a.result1[i][0]
        rname = a.result1[i][1]
        rage = a.result1[i][2]
        rtext = a.result1[i][3]
        redu = a.result2[i][1]
        runi = a.result2[i][2]
        rlevel = a.result2[i][3]
        rtarget = a.result3[i][1] if len(a.result3[i][1]) != 0 else "不确定岗位"
        rworktime = a.result3[i][2]
        rcompany = a.result3[i][3].split(" ")[0] if len(a.result3[i][3]) != 0 else "某公司"
        rskill = KeyWords(a.result4[i][2],a.result4[i][3],a.result4[i][4],a.result4[i][5],a.result4[i][6],
                          a.result4[i][7],a.result4[i][8],a.result4[i][9],a.result4[i][10],a.result4[i][11],
                          a.result4[i][12],a.result4[i][13],a.result4[i][14],a.result4[i][15],a.result4[i][16],
                          a.result4[i][17],a.result4[i][18])
        rjob = [rtarget,]
        maxi = 2
        maxNum = a.result3[i][2]
        for j in range(4,12):
            if maxNum < a.result3[i][j]:
                maxi = j
                maxNum = a.result3[i][j]
        
        if a.result3[i][4] == 90 or (maxi ^ 2) == 0:
            rjob += ["工程","技术"]
        if a.result3[i][5] == 90 or (maxi ^ 3) == 0:
            rjob += ["财务","会计","税务","精算","审计","出纳"]
        if a.result3[i][6] == 90 or (maxi ^ 4) == 0:
            rjob += ["设计师",'设计']
        if a.result3[i][7] == 90 or (maxi ^ 5) == 0:
            rjob += ["行政管理","经理","总监","主管","管理","行政","人事"]
        if a.result3[i][8] == 90 or (maxi ^ 6) == 0:
            rjob += ["运营","营销","市场","客服","产品","销售","推广"]
        if a.result3[i][9] == 90 or (maxi ^ 7) == 0:
            rjob += ["医疗","卫生","护理","保健","制药","生物","医护"]
        if a.result3[i][10] == 90 or (maxi ^ 8) == 0:
            rjob += ["文员","编辑","助理","职员","接待员","办事员","打杂"]
        if len(rjob) == 0:
            rjob.append('其他')
        
        r = Resumer(rid,rname,rage,redu,runi,rlevel,rworktime,rjob,rtext,rtarget,rcompany,rskill)
        r.score = jobMatch(job,r)
        resumers.append(r)
    resumers.sort(key=lambda x:x.score,reverse=True)
    return resumers[:20]