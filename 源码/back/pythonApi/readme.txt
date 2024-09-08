代码结构

--pythonApi
   |
   --information_extration  paddlenlp的一个信息抽取模型
   --NERModel  模型训练
       |
       --data 训练集和验证级
       --huggingface 存储bert模型
       --model 存储训练后的模型
       --conlleval.py 评估函数
       --extract.py 抽取文档信息
       --models.py 训练模型
       --ner.py 使用模型
       --utils.py 工具类

   --PythonSDK 移动云接口 用于抽取不同格式文件中的文字
   --uploads 暂时存储上传文件的地方
   |
   --cmp.py 比较模型性能
   --matchJob.py 岗位匹配函数
   --readFile.py 抽取不同格式文件的文字并进行命名实体识别
   --run.py 入口函数
   --stopwords.txt 停用词
   --university.txt 大学名称
