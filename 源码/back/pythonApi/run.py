from flask import Flask,request,json
from flask_cors import CORS
from LAC import LAC
import readFile
import matchJob
import os
from werkzeug.utils import secure_filename
from paddlenlp import Taskflow

app = Flask(__name__)
CORS(app)
# 临时存储文件的路径
app.config['UPLOAD_FOLDER'] = 'D:/resume/pythonApi/uploads'
# 调用函数来删除文件夹中的所有文件
app.config['single'] = 'D:/resume/pythonApi/uploads/single/'
app.config['multi'] = 'D:/resume/pythonApi/uploads/multi/'
# 允许的文件类型的集合
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'docx','doc'])
# 上传文件限制为最大200MB，
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
# 从本地文件中读取大学名称
schoolNamesFile = "D:/resume/pythonApi/大学名录.txt"
# 读取LAC语言模型
lac = LAC(mode="lac")
# 设置taskflow模型地址
informationPath="D:/resume/pythonApi/information_extraction"
# 进度变量设置值

def delete_files_in_folder(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print("文件夹不存在。")
        return
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 删除子文件夹中的所有文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    print("所有文件已删除。")
folder_path = app.config['UPLOAD_FOLDER']
delete_files_in_folder(folder_path)
os.makedirs(app.config['single'], exist_ok=True)
os.makedirs(app.config['multi'], exist_ok=True)

def get_chinese_universities(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        universities = [line.strip() for line in file.readlines()]
    return universities

@app.route('/singleData/upload',methods=['POST'])
def singleUpload():
    uploaded_files = request.files.getlist("file")
    #print(request.files.getlist("file"))
    delete_files_in_folder(app.config['single'])
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        destination_file = os.path.join(app.config['single'], filename)
        file_type = file.mimetype
        if file_type == 'text/plain':  # 处理文本文件（.txt）
            with open(destination_file, 'w',encoding="utf-8") as f:
                f.write(file.read().decode('utf-8'))
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  # 处理Word文档（.docx）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        elif file_type == 'application/msword':  # 处理旧版Word文档（.doc）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        elif file_type == 'application/pdf':  # 处理PDF文件（.pdf）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        elif file_type == 'image/png' or file_type == 'image/jpg' or file_type == 'image/jpeg':  # 处理图像文件（.png）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        else:
            print("Unsupported file type:", file_type)
    return 'upload'

def get_file_paths(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths
@app.route('/singleData/dealFile',methods=['POST'])
def singleDataUpload():
    #current_dir = os.path.dirname(os.path.abspath(__file__))
    #print(current_dir)
    uploaded_files = get_file_paths(app.config['single'])
    print(uploaded_files)
    #uploaded_files1 = []
    #for file in uploaded_files:
        #file = os.path.join(current_dir,file)
        #uploaded_files1.append(file)
    chinese_universities = get_chinese_universities(schoolNamesFile)
    text = ''
    for file in uploaded_files:
        #print(file)
        text += readFile.ReadFile(file).text
        text += '\n'
    #print(text)
    information = readFile.Extractor(text,chinese_universities,lac,informationPath)
    dic = {
        'name': information.name,
        'age':information.age,
        'education':information.degree,
        'university':information.school,
        'workExperience':information.workTime,
        'gender':information.gender,
        'targetJob':information.office[0] if len(information.office) > 0 else '',
        'jobs':" ".join(information.office),
        'identity':information.id,
        'origin':information.origin,
        'major':information.major,
        'companies':" ".join(information.company),
        'phone':information.calls['phone'],
        'email':information.calls['email'],
        'english':information.skills['english'],
        'schoolTime':information.schoolTime,
        'reward':information.rewardNums,
        'mandarin':information.skills['mandarin'],
        'computer':information.skills['computer'],
        'c':information.skills['C'],
        'java':information.skills['Java'],
        'python':information.skills['Python'],
        'graphicDesign':information.skills['平面设计'],
        'officeSoftware':information.skills['办公软件'],
        'word':information.skills['word'],
        'excel':information.skills['excel'],
        'ppt':information.skills['ppt'],
        'pr':information.skills['剪辑'],
        'communicate':information.skills['沟通'],
        'act':information.skills['执行'],
        'logic':information.skills['逻辑'],
        'ai':information.skills['人工智能'],
        'schoolLevel':information.schoolLevel,
        'engineer':information.jobs['engineer'],
        'finance':information.jobs['finance'],
        'design':information.jobs['design'],
        'manager':information.jobs['manager'],
        'market':information.jobs['market'],
        'hospital':information.jobs['hospital'],
        'edit':information.jobs['edit'],
        'elseJob':information.jobs['else'],
        'text':text
    }
    return json.dumps(dic,ensure_ascii=False)

@app.route('/multiData/upload',methods=['POST'])
def multiUpload():
    uploaded_files = request.files.getlist("file")
    #print(uploaded_files)
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        destination_file = os.path.join(app.config['multi'], filename)
        file_type = file.mimetype
        if file_type == 'text/plain':  # 处理文本文件（.txt）
            with open(destination_file, 'w',encoding="utf-8") as f:
                f.write(file.read().decode('utf-8'))
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  # 处理Word文档（.docx）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        elif file_type == 'application/msword':  # 处理旧版Word文档（.doc）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        elif file_type == 'application/pdf':  # 处理PDF文件（.pdf）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        elif file_type == 'image/png' or file_type == 'image/jpg' or file_type == 'image/jpeg':  # 处理图像文件（.png）
            with open(destination_file, 'wb') as f:
                f.write(file.read())
        else:
            print("Unsupported file type:", file_type)
    return 'upload'

@app.route('/multiData/dealFile',methods=['POST'])
def multiDataUpload():
    #current_dir = os.path.dirname(os.path.abspath(__file__))
    uploaded_files = get_file_paths(app.config['multi'])
    print(uploaded_files)
    #uploaded_files1 = []
    #for file in uploaded_files:
        #file = os.path.join(current_dir,file)
        #uploaded_files1.append(file)
    chinese_universities = get_chinese_universities(schoolNamesFile)
    diclist = []
    for file in uploaded_files:
        text = readFile.ReadFile(file).text
        information = readFile.Extractor(text,chinese_universities,lac,informationPath)
        dic = {
            'name': information.name,
            'age':information.age,
            'education':information.degree,
            'university':information.school,
            'workExperience':information.workTime,
            'gender':information.gender,
            'targetJob':information.office[0] if len(information.office) > 0 else '',
            'jobs':" ".join(information.office),
            'identity':information.id,
            'origin':information.origin,
            'major':information.major,
            'companies':" ".join(information.company),
            'phone':information.calls['phone'],
            'email':information.calls['email'],
            'english':information.skills['english'],
            'schoolTime':information.schoolTime,
            'reward':information.rewardNums,
            'mandarin':information.skills['mandarin'],
            'computer':information.skills['computer'],
            'c':information.skills['C'],
            'java':information.skills['Java'],
            'python':information.skills['Python'],
            'graphicDesign':information.skills['平面设计'],
            'officeSoftware':information.skills['办公软件'],
            'word':information.skills['word'],
            'excel':information.skills['excel'],
            'ppt':information.skills['ppt'],
            'pr':information.skills['剪辑'],
            'communicate':information.skills['沟通'],
            'act':information.skills['执行'],
            'logic':information.skills['逻辑'],
            'ai':information.skills['人工智能'],
            'schoolLevel':information.schoolLevel,
            'engineer':information.jobs['engineer'],
            'finance':information.jobs['finance'],
            'design':information.jobs['design'],
            'manager':information.jobs['manager'],
            'market':information.jobs['market'],
            'hospital':information.jobs['hospital'],
            'edit':information.jobs['edit'],
            'elseJob':information.jobs['else'],
            'text':text
        }
        diclist.append(dic)
    delete_files_in_folder(app.config['multi'])
    return json.dumps(diclist,ensure_ascii=False)

def Ingeter(string:str):
    dights = ''
    for char in string:
        if char.isdigit():
            dights += char
        else:
            break
    if dights:
        number = int(dights)
    else:
        number = 0
    return number


@app.route('/jobMatch',methods=['POST'])
def jobMatch():
    jobname = request.form.get('jobname')  # 获取jobname字段的值
    education = request.form.get('education')  # 获取education字段的值
    minAge = int(request.form.get('minAge'))  # 获取minAge字段的值，并转换为整数
    maxAge = int(request.form.get('maxAge'))  # 获取maxAge字段的值，并转换为整数
    workTime = Ingeter(request.form.get('workTime'))  # 获取workTime字段的值
    desc = request.form.get('desc')  # 获取desc字段的值
    tfidf = matchJob.Extractor()
    job = matchJob.Job(jobname,maxAge,minAge,education,workTime,desc,tfidf)
    resumes = matchJob.main(job,tfidf)
    resumesDic = []
    for resume in resumes:
        resumesDic.append(resume.to_dict())
    return json.dumps(resumesDic,ensure_ascii=False)


if __name__ == '__main__':
    # 这里host是你的后端地址，这里写0.0.0.0， 表示的是这个接口在任何服务器上都可以被访问的到，只需要前端访问该服务器地址就可以的，
    # 当然你也可以写死，如222.222.222.222， 那么前端只能访问222.222.222.222, port是该接口的端口号,
    # debug = True ,表示的是，调试模式，每次修改代码后不用重新启动服务
    app.run(host='0.0.0.0', port=5000, debug=True)