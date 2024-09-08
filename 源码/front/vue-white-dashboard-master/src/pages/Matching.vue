<template>
  <div class="content" style="min-height: 100%">
    <el-row :gutter=15 style="height: 100%">
      <el-col :span="10">
        <el-card>
          <el-row>
            <h3>职位信息</h3>
          </el-row>
          <el-form ref="form" :model="form" label-width="80px" class="t-left">
            <el-form-item label="岗位名称" title="jobname">
              <el-input v-model="form.jobname" placeholder="请输入岗位名称"></el-input>
            </el-form-item>
            <el-form-item label="学历要求" title="education">
              <el-select v-model="form.education" placeholder="请选择学历" class="t-left">
                <el-option label="无" value="无"></el-option>
                <el-option label="高中" value="高中"></el-option>
                <el-option label="中专" value="中专"></el-option>
                <el-option label="大专" value="大专"></el-option>
                <el-option label="本科" value="本科"></el-option>
                <el-option label="硕士" value="硕士"></el-option>
                <el-option label="博士" value="博士"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="年龄" title="Min(Max)age">
              <el-row class="age">
                <el-input type="number" max="18" v-model="form.minAge" placeholder="最小年龄"></el-input><span>-</span><el-input
                  type="number" max="60" v-model="form.maxAge" placeholder="最大年龄"></el-input>
              </el-row>
              <!-- <el-select v-model="form.age" placeholder="请选择年龄段" class="t-left">
                <el-option label="20~25" value="20~25"></el-option>
                <el-option label="26~30" value="26~30"></el-option>
                <el-option label="31~35" value="31~35"></el-option>
                <el-option label="36~40" value="36~40"></el-option>
                <el-option label="41~45" value="41~45"></el-option>
                <el-option label="46~50" value="46~50"></el-option>
              </el-select> -->
            </el-form-item>
            <el-form-item label="工作经验" title="Min(Max)workTime">
              <el-select v-model="form.workTime" placeholder="请选择工作经验" class="t-left">
                <el-option label="无要求" value="0"></el-option>
                <el-option label="1年以上" value="1"></el-option>
                <el-option label="2年以上" value="2"></el-option>
                <el-option label="3年以上" value="3"></el-option>
                <el-option label="5年以上" value="5"></el-option>
                <el-option label="10年以上" value="10"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="岗位要求">
              <el-input type="textarea" :rows="3" v-model="form.desc" placeholder="请输入岗位要求" class="t-left"></el-input>
            </el-form-item>
            <el-form-item class="submit">
              <el-button type="primary" @click="onSubmit">提交</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="14" class="card-list">
        <el-card class="card-item" v-for="item in matchcont" :key="item">
          <el-row>
            <h4>{{ item.target }}</h4>
          </el-row>
          <el-rate v-model="value" disabled text-color="#ff9900" :score-template="'{{ item.score }}'">

          </el-rate>
          <el-row><span>{{ item.name }}</span><el-divider direction="vertical"></el-divider><span>{{ item.education
          }}</span><el-divider direction="vertical"></el-divider><span>{{ item.workExperience
}}年工作经验</span></el-row>
          <el-row><span>{{ item.company }}</span><el-divider direction="vertical"></el-divider><span>{{ item.target
          }}</span></el-row>
          <el-row><span>{{ item.university }}</span><el-divider direction="vertical"></el-divider><span>{{ item.major
          }}</span><el-divider direction="vertical"></el-divider><span>{{ item.schoolLevel }}院校</span></el-row>
          <el-row>
            <el-tag v-if="item.skill.act !== 0">行动力</el-tag>
            <el-tag v-if="item.skill.ai !== 0">人工智能</el-tag>
            <el-tag v-if="item.skill.c !== 0">C语言</el-tag>
            <el-tag v-if="item.skill.communicate !== 0">沟通能力</el-tag>
            <el-tag v-if="item.skill.computer !== 0">计算机</el-tag>
            <el-tag v-if="item.skill.english === '四级' || item.skill.english === '六级'">{{ item.skill.english }}</el-tag>
            <el-tag v-if="item.skill.excel !== 0">excel</el-tag>
            <el-tag v-if="item.skill.graphicDesign !== 0">平面设计能力</el-tag>
            <el-tag v-if="item.skill.mandarin !== 0">普通话</el-tag>
            <el-tag v-if="item.skill.officeSoftware !== 0">掌握办公软件</el-tag>
            <el-tag v-if="item.skill.ppt !== 0">ppt</el-tag>
            <el-tag v-if="item.skill.pr !== 0">剪辑</el-tag>
            <el-tag v-if="item.skill.python !== 0">python</el-tag>
            <el-tag v-if="item.skill.reward !== 0">{{ item.skill.reward }}个荣誉证书</el-tag>
            <el-tag v-if="item.skill.word !== 0">word</el-tag>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        jobname: "",
        education: "",
        minAge: 20,
        maxAge: 60,
        workTime: '',
        desc: "",
      },
      value: 5,
      matchcont: []
    };
  },
  methods: {
    onSubmit() {
      console.log(this.form)
      axios
        .post("http://localhost:5000/jobMatch", this.form, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(response => {
          this.matchcont = response.data
          console.log(this.matchcont[0].skill)


        })
        .catch(error => {
          console.error(error)
        })
    }
  }
};
</script>

<style>
.t-left {
  text-align: left !important;
}

h3,
h4 {
  font-weight: 700;
  color: #444 !important;
}

h4 {
  margin-bottom: 0 !important;
}

.el-form-item label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.submit .el-form-item__content {
  margin-left: 0 !important;
  text-align: center;
}

.el-tag {
  margin: 5px 10px 5px 0;
}

.card-item {
  margin-bottom: 10px;
}

.card-list {
  max-height: 540px;
  overflow: auto;
}

.age {
  display: flex;
}

.age span {
  margin: 0 10px;
}
</style>