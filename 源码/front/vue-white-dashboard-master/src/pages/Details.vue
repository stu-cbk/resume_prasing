<template>
  <div class="content">
    <div class="topUser">
      <img v-if="gender === '男'" src="../assets/img/anime3.png" width="70" height="70">
      <img v-else src="../assets/img/anime6.png" width="70" height="70">
      <div class="topUser_right">
        <div class="topUser_right_top">
          <div class="name">{{ userName }}</div>
          <div class="namebq">{{ university }}</div>
          <div class="namebq">{{ capacity }}</div>
        </div>
        <div class="topUser_right_bottom">
          <div class="item" style="margin-left: 0;">
            <i class="el-icon-user-solid"></i>
            <span> {{ year }}</span>
          </div>
          <div class="item">
            <i class="el-icon-remove"></i>
            <span> {{ gender }}</span>
          </div>
          <div class="item">
            <i class="el-icon-phone"></i>
            <span> {{ number }}</span>
          </div>
          <div class="item">
            <i class="el-icon-message"></i>
            <span> {{ emit }}</span>
          </div>
          <div class="item">
            <i class="el-icon-message"></i>
            <span> {{ Working }}工作经验</span>
          </div>
          <div class="item">
            <i class="el-icon-suitcase-1"></i>
            <span> {{ education }}</span>
          </div>
        </div>
      </div>
    </div>
    <el-tabs class="table-tab" v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="中文简历" name="first">
        <div class="userInfo">
          <div class="title">
            <div class="info">基本信息 <div class="pos"></div>
            </div>
           
          </div>
          <div class="lists">
            <ul>
              <li><span class="label">姓名: </span>&nbsp{{ userName }}</li>
              <li><span class="label">手机: </span>&nbsp{{ number }}</li>
              <li><span class="label">籍贯: </span>&nbsp{{ native }}</li>
              <li><span class="label">专业:</span>&nbsp{{ speciality }}</li>
              <li><span class="label">工作时长:</span>&nbsp{{ Working }}</li>
              <li><span class="label">政治面貌:</span>&nbsp{{ outlook }}</li>
            </ul>
            <ul style="margin-left: 300px;">
              <li><span class="label">年龄: </span>&nbsp{{ year }}</li>
              <li><span class="label">邮箱: </span>&nbsp{{ emit }}</li>
              <li><span class="label">性别: </span>&nbsp{{ gender }}</li>
              <li><span class="label">学历:</span>&nbsp{{ education }}</li>
              <li><span class="label">毕业院校:</span>&nbsp{{ institutions }}</li>
              <li><span class="label">毕业院校类别:</span>&nbsp{{ category }}</li>
            </ul>
          </div>
        </div>
        <div>
          <div class="title">
            <div class="info">教育信息 <div class="pos"></div>
            </div>
          </div>
          <div class="nameusdate">
            <div>{{ institutions }}</div>
            <div class="date">{{ date }}</div>
          </div>
          <div class="lists">
            <ul>
              <li><span class="label">开始时间: </span>&nbsp{{ startDate }}</li>
              <li><span class="label">结束时间: </span>&nbsp{{ ennDate }}</li>
              <li><span class="label">学位:</span>&nbsp{{ education }}</li>
              <li><span class="label">专业:</span>&nbsp{{ speciality }}</li>
              <li><span class="label">学校级别:</span>&nbsp{{ category }}</li>
            </ul>
          </div>
        </div>
        <div>
          <div class="title">
            <div class="info">
              工作信息
              <div class="pos"></div>
            </div>
          </div>
          <div class="lists">
            <ul>
              <li><span class="label">求职岗位: </span>&nbsp;{{ targetjob }}</li>
              <li>
                <span class="label">历史岗位: </span
                >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ hisjob }}
              </li>
              <li><span class="label">历史公司: </span>&nbsp;{{hiscomp }}</li>
            </ul>
          </div>
        </div>
        <div>
          <div class="title">
            <div class="info">技能信息 <div class="pos"></div>
            </div>
          </div>
          <div class="lists">
            <ul>
              <li><span class="label">普通话水平: </span>&nbsp{{ pth }}</li>
              <li><span class="label">英语水平: </span>&nbsp&nbsp&nbsp&nbsp&nbsp{{ elevel }}</li>
              <li><span class="label">编程语言: </span>&nbsp{{ comcap }}</li>
              <li><span class="label">平面设计能力:</span>&nbsp{{ designcap }}</li>
              <li><span class="label">办公软件掌握:</span>&nbsp{{ mastercap }}</li>
              <li><span class="label">剪辑能力:</span>&nbsp{{ prcap }}</li>
              <li><span class="label">沟通\逻辑思维\执行\AI能力:</span>&nbsp{{ othercap }}</li>
            </ul>
          </div>
        </div>
        <div class="hr"></div>
      </el-tab-pane>
      <el-tab-pane label="候选人画像" name="second">
        <div class="title">
          <div class="info">简历亮点 <div class="pos"></div>
          </div>
         
         
        </div>
        <div class="Highlights">
          <div class="titLabel">
            <div class="image">
              <i class="el-icon-thumb"></i>
            </div>
            <p style="color: black;">简历亮点 x {{ Lnum }}</p>
          </div>
          <ul>
            <li v-if="titLabel1">{{ titLabel1 }}</li>
            <li v-if="titLabel2">{{ titLabel2 }}</li>
            <li v-if="titLabel3">{{ titLabel3 }}</li>
            <li v-if="titLabel4">{{ titLabel4 }}</li>
            <li v-if="titLabel5">{{ titLabel5 }}</li>
            <li v-if="titLabel6">{{ titLabel6 }}</li>
            <li v-if="titLabel7">{{ titLabel7 }}</li>
            <li v-if="titLabel8">{{ titLabel8 }}</li>
          </ul>
        </div>

        <div class="title">
          <div class="info">候选人标签 <div class="pos"></div>
          </div>
        </div>
        <div style="margin-left: 10px;">
          <div class="titles">基本标签</div>
          <div class="labels">
            <el-tooltip v-for="item in tooltipList" :content="item.content" placement="top">
              <el-button type="primary" plain round>{{ item.label }}</el-button>
            </el-tooltip>
          </div>
        </div>
        <div style="margin-left: 10px;">
          <div class="titles">教育背景标签</div>
          <div class="labels">
            <el-tooltip v-for="item in tooltipList2" :content="item.content" placement="top">
              <el-button type="warning" plain round>{{ item.label }}</el-button>
            </el-tooltip>
          </div>
        </div>

        <div style="margin-left: 10px;">
          <div class="titles">技能标签</div>
          <div class="labels">
            <el-tooltip v-for="item in tooltipList3" :content="item.content" placement="top">
              <el-button style="background: #5bda92;border-color:#5bda92 ;" type="success" round>{{ item.label
              }}</el-button>
            </el-tooltip>
          </div>
        </div>


        <div class="title" style="margin-top:  10px;">
          <div class="info">职位甄别 <div class="pos"></div>
          </div>
        </div>
        <ve-radar-chart :data="chartData" :legend="legend" :settings="settings" />
        <div class="title" style="margin-top:  10px;">
          <div class="info">能力展示 <div class="pos"></div>
          </div>
        </div>
        <div ref="chart2" style="width: 600px; height: 600px; margin-left: 35%"></div>
      </el-tab-pane>

      <el-tab-pane label="提取信息" name="third">
        <div class="title">
            <div class="info">提取信息 <div class="pos"></div>
            </div>
        </div>
        <div class="lists" style="padding:8px;border:1px solid #96c2f1;background:#eff7ff;width:60%">
          {{ txt }}
        </div>
      </el-tab-pane>
      
    </el-tabs>
  </div>
</template>

<script>
import axios from 'axios';
import echarts from 'echarts';

export default {
  data() {
    return {
      id: null,
      activeName: 'first', //选项卡 
      userName: '张吉惟 B',
      university: "国内985/211 E",
      capacity: "英语能力良好 Sd",
      year: "25岁 B",
      gender: "女 B",
      number: "13899999999 B",
      emit: "zhangjiwei@163.com B",
      experience: "4年工作经验 Wd",
      education: "本科 E",

      native: "北京海淀区 B",
      birthday: "1998-11-20 N",
      speciality: "国际经济与贸易 E",
      Working: "4年 W",
      outlook: "党员 B",
      start: "2019 N",
      institutions: "北京师范大学 E",
      level: "初级 N",
      category: "985 211 E",
      date: "2015.01 - 2019.01 E",
      startDate: "2015.01 Ed",
      ennDate: "2019.01 Ed",
      location: "北京",
      cat: "20 N",
      course: "N 国际贸易理论与实务，国际经济与贸易，政治经济学，西方经济学，计量经济学，国际经济学，国际结算，国际金融",

      pth: "Ps，Ai，PPT，Word，Excel，运营，经济学，国际贸易，行政管理，国际金融，政治经济学",
      elevel: "PPT，Excel",
      comcap: "",
      designcap: "英语",
      mastercap: "",
      prcap: "国家级一等奖学金，全国大学生英语竞赛一等奖",
      othercap: "本人",
      targetjob:"Java工程师",
      hisjob:"Java工程师",
      hiscomp:"美团",

      Lnum: 0,
      titLabel1: "",
      titLabel2: "",
      titLabel3: "",
      titLabel4: "",
      titLabel5: "",
      titLabel6: "",
      titLabel7: "",
      titLabel8: "",

      txt:"张吉惟",


      tooltipList: [],
      tooltipList2: [],
      tooltipList3: [],

      chartData: {},
      legend: { show: false },
      settings: {
        radius: 120,
        splitNumber: 3,
        shape: 'circle',
        splitArea: {
          areaStyle: {
            color: ['rgba(114, 172, 209, 0.2)', 'rgba(114, 172, 209, 0.4)', 'rgba(114, 172, 209, 0.6)', 'rgba(114, 172, 209, 0.8)', 'rgba(114, 172, 209, 1)'],
            shadowColor: 'rgba(0, 0, 0, 0.3)',
            shadowBlur: 10
          }
        }
      },
      chartData: {
        dimensions: [
          { name: '工程师', max: 100 },
          { name: '行政/管理/人事', max: 100 },
          { name: '设计师', max: 100 },
          { name: '医疗/护理', max: 100 },
          { name: '市场/运营/产品/营销', max: 100 },
          { name: '文员/编辑/助理', max: 100 },
          { name: '财务', max: 100 },
          { name: '其他', max: 100 }
        ],
        measures: [{ name: '能力展示', data: [30, 60, 90, 100, 10, 20] }]
      }
    };
  },
  created() {
    this.id = this.$route.params.id
    console.log(this.$route.params.id)
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    // handleClick(tab, event) {
    //   console.log(tab, event);
    // },
    fetchData() {
      axios
        .get('http://localhost:8181/api/resume/showBasicData')
        .then((response) => {
          const allBasicData = response.data.data;
          const tar1 = allBasicData.find(data => data.id == this.id);
          if (tar1) {
            console.log(tar1);
          } else {
            console.log("Not found");
          }
          this.userName = tar1.name;
          this.year = tar1.age;
          this.gender = tar1.gender;
          this.number = tar1.phone;
          this.emit = tar1.email;
          this.native = tar1.origin;
          this.outlook = tar1.identity;
          this.txt = tar1.text;

          return axios
            .get('http://localhost:8181/api/resume/showEducationalData')
            .then((response) => {
              // console.log(response.data.data)
              const allEduData = response.data.data;
              const tar2 = allEduData.find(data => data.id == this.id);

              if (tar2) {
                console.log(tar2);
              } else {
                console.log("Not found");
              }
              this.education = tar2.education;
              this.speciality = tar2.major;
              this.university = tar2.schoolLevel + '院校';
              this.category = tar2.schoolLevel;
              this.date = tar2.schoolTime;
              this.startDate = tar2.schoolTime.split(/[-]/)[0];
              this.ennDate = tar2.schoolTime.split(/[-]/)[1];
              this.institutions = tar2.university;

              this.tooltipList2 = [
                { label: `${tar2.education}学历`, content: "学历" },
                { label: tar2.major, content: "专业" },
                { label: `${tar2.schoolLevel}工程院校`, content: "学校等级标签" }
              ]

              return axios
                .get('http://localhost:8181/api/resume/showWorkData')
                .then((response) => {
                  const allWorkData = response.data.data;
                  const tar3 = allWorkData.find(data => data.id == this.id);
                  if (tar3) {
                    console.log(tar3);
                  } else {
                    console.log("Not found");
                  }
                  this.Working = tar3.workExperience + '年';
                  this.targetjob = tar3.targetJob;
                  this.hisjob = tar3.jobs;
                  this.hiscomp = tar3.companies;

                  const value1 = []
                  value1.push(parseInt(tar3.engineer));
                  value1.push(parseInt(tar3.finance));
                  value1.push(parseInt(tar3.design));
                  value1.push(parseInt(tar3.manager));
                  value1.push(parseInt(tar3.market));
                  value1.push(parseInt(tar3.hospital));
                  value1.push(parseInt(tar3.edit));
                  value1.push(parseInt(tar3.elseJob));

                  this.chartData.measures[0].data = value1;
                  this.tooltipList = [
                    { label: tar1.gender, content: '性别' },
                    { label: `${tar1.age}岁`, content: '年龄' },
                    { label: tar1.identity, content: '政治面貌' },
                    { label: `${tar3.workExperience}年经验`, content: '工作经验' },
                  ];

                  return axios
                    .get('http://localhost:8181/api/resume/showSkillData')
                    .then((response) => {
                      const allSkillData = response.data.data;
                      let english = 0;
                      const tar = allSkillData.find(data => data.id == this.id);
                      if (tar) {
                        console.log(tar);
                      } else {
                        console.log("Not found");
                      }

                      this.tooltipList3 = [
                        { label: tar2.major, content: "专业技能" },
                      ]

                      if (tar.english === '六级') {
                        this.capacity = '英语优秀，六级水平'
                        english = 6;
                        this.tooltipList3.push({ label: '六级', content: '英语技能' });
                      }
                      else if (tar.english === '四级') {
                        this.capacity = '英语良好，四级水平'
                        english = 4;
                        this.tooltipList3.push({ label: '四级', content: '英语技能' });
                      }
                      else {
                        this.capacity = '英语一般'
                      }


                      if (tar.mandarin >= 9) {
                        this.pth = "优秀";
                      } else if (tar.mandarin >= 5) {
                        this.pth = "良好";
                      } else {
                        this.pth = "一般";
                      }
                      this.elevel = this.capacity;
                      if (tar.c !== 0) {
                        this.comcap += 'C语言 '
                        this.tooltipList3.push({ label: 'C语言', content: '编程技能' });
                      }
                      if (tar.java !== 0) {
                        this.comcap += 'java '
                        this.tooltipList3.push({ label: 'java', content: '编程技能' });
                      }
                      if (tar.python !== 0) {
                        this.comcap += 'python'
                        this.tooltipList3.push({ label: 'python', content: '编程技能' });
                      }
                      if (this.comcap === '') this.comcap = '无编程能力'

                      if (tar.graphicDesign >= 9) {
                        this.designcap = "优秀";
                        this.tooltipList3.push({ label: '优秀', content: '平面设计技能' });
                      } else if (tar.graphicDesign >= 5) {
                        this.designcap = "良好";
                        this.tooltipList3.push({ label: '良好', content: '平面设计技能' });
                      } else {
                        this.designcap = "一般";
                      }

                      if (tar.word !== 0) {
                        this.mastercap += 'word '
                        this.tooltipList3.push({ label: 'word', content: '办公技能' });
                      }
                      if (tar.excel !== 0) {
                        this.mastercap += 'excel '
                        this.tooltipList3.push({ label: 'excel', content: '办公技能' });
                      }
                      if (tar.ppt !== 0) {
                        this.mastercap += 'powerpoint '
                        this.tooltipList3.push({ label: 'ppt', content: '办公技能' });
                      }
                      if (this.mastercap === '') this.mastercap = '对办公软件不掌握'

                      if (tar.pr >= 9) {
                        this.prcap = "优秀";
                        this.tooltipList3.push({ label: 'pr', content: '剪辑技能' });
                      } else if (tar.pr >= 5) {
                        this.prcap = "良好";
                        this.tooltipList3.push({ label: 'pr', content: '剪辑技能' });
                      } else {
                        this.prcap = "一般";
                      }

                      if (tar.communicate === 1) {
                        this.othercap += '善于交际,喜欢与人沟通，'
                        this.tooltipList3.push({ label: '沟通', content: '沟通' });
                      }
                      // else if(tar.communicate >= 5) this.othercap += '沟通尚可，'
                      else this.othercap += '不善言辞，沟通能力较弱，'

                      if (tar.logic === 1) {
                        this.othercap += '思维缜密，逻辑严谨，'
                        this.tooltipList3.push({ label: '逻辑', content: '逻辑' });
                      }
                      // else if(tar.logic >= 5) this.othercap += '逻辑周到，'
                      else this.othercap += '逻辑思维能力较弱，'

                      if (tar.act === 1) {
                        this.othercap += '执行能力强，不拖拉，'
                        this.tooltipList3.push({ label: '执行力', content: '执行力' });
                      }
                      // else if (tar.act >= 5) this.othercap += '能按时完成任务，'
                      else this.othercap += '拖拉，执行力弱，'

                      if (tar.ai === 1) {
                        this.othercap += '有优秀的AI能力'
                        this.tooltipList3.push({ label: 'AI能力', content: '人工智能' });
                      }
                      // else if (tar.ai >= 5) this.othercap += "AI能力完备"
                      else this.othercap += 'AI能力欠佳'

                      const chartContainer = this.$refs.chart2;
                      const chart = echarts.init(chartContainer);
                      const officeSoftware = tar.officeSoftware;
                      const mandarin = tar.mandarin;
                      const computer = parseInt(tar.computer);
                      const graphicDesign = parseInt(tar.graphicDesign);

                      // console.log(computer, graphicDesign)
                      const option = {
                        dataset: {
                          source: [
                            ['score', 'amount', 'product'],
                            [officeSoftware, officeSoftware, '软件办公能力'],
                            [mandarin, mandarin, '普通话'],
                            [computer, computer, '计算机'],
                            [english, english, '英语'],
                            [graphicDesign, graphicDesign, '平面设计能力'],
                          ]
                        },
                        grid: { containLabel: true },
                        xAxis: { name: 'score' },
                        yAxis: { type: 'category' },
                        visualMap: {
                          orient: 'horizontal',
                          left: 'center',
                          min: 0,
                          max: 20,
                          text: ['最高分', '最低分'],
                          // Map the score column to color
                          dimension: 0,
                          inRange: {
                            color: ['#65B581', '#FFCE34', '#FD665F']
                          }
                        },
                        series: [
                          {
                            type: 'bar',
                            encode: {
                              // Map the "amount" column to X axis.
                              x: 'amount',
                              // Map the "product" column to Y axis
                              y: 'product'
                            }
                          }
                        ]
                      };
                      chart.setOption(option);

                      var mergedData = { ...tar1, ...tar2, ...tar3, ...tar };
                      // console.log(mergedData)
                      return axios
                        .post('http://localhost:8181/api/resume/lightResume', mergedData, {
                          headers: {
                            'Content-Type': 'application/json;chartset=UTF-8'
                          }
                        })
                        .then((response) => {
                          // console.log(response.data.data)
                          const Linfo = response.data.data
                          this.Lnum = Linfo.length;
                          this.titLabel1 = Linfo[0];
                          this.titLabel2 = Linfo[1];
                          this.titLabel3 = Linfo[2];
                          this.titLabel4 = Linfo[3];
                          this.titLabel5 = Linfo[4];
                          this.titLabel6 = Linfo[5];
                          this.titLabel7 = Linfo[6];
                          this.titLabel8 = Linfo[7];
                          // console.log('渲染条形图前', this.id)

                        })
                        .catch((error) => {
                          console.error(error);
                        });
                    })
                })
            })
        })
    },
  }
};
</script>

<style scoped>
.container {
  height: 100vh;
}

.topUser {
  display: flex;
  align-items: center;
}

.topUser_right {}

.topUser_right_top {
  display: flex;
  align-items: center;
  margin-left: 20px;
}

.name {
  font-size: 25px;
  font-weight: 600;
}

.namebq {
  padding: 0 6px;
  height: 22px;
  line-height: 22px;
  background: #effafb;
  color: #115f85;
  margin-left: 10px;
}

.topUser_right_bottom {
  display: flex;
  margin-left: 20px;
}

.topUser_right_bottom .item {
  color: #8e9098;
  font-size: 15px;
  font-weight: 500;
  margin-left: 15px;
}

::v-deep .table-tab .el-tabs__nav-scroll {
  padding-left: 10px;
}

::v-deep .table-tab .el-tabs__active-bar {
  height: 4px;
  background: #6e73d4;
}

.userInfo {}

.title {
  display: flex;
  justify-content: space-between;
}

.title .info {
  position: relative;
  font-size: 25px;
  font-weight: 500;
  z-index: 10;
}

.pos {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 110px;
  height: 25px;
  background: #e8eafd;
  z-index: -1;
}

.lists {
  display: flex;
  margin-top: 20px;
}

.lists ul {}

.lists ul li {
  text-align: left;
  margin-bottom: 8px;
}

.lists ul li .label {
  color: #bbbbbd;
}

.lists ul li::marker {
  color: #746ecc;
}

.nameusdate {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
}

.nameusdate div {
  font-size: 20px;
  font-weight: 600;
}

.nameusdate .date {
  font-size: 15px;
  color: #acacac;
  font-weight: 400;

}

.hr {
  width: 100%;
  height: 4px;
  background: #c8c7cd;
}

.Highlights {
  margin-top: 25px;
}

.titLabel {
  margin-left: 12px;
  display: flex;
  align-items: center;
}

.titLabel .image {
  width: 25px;
  height: 25px;
  background: #3076da;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
}

.titLabel p {
  color: black;
  font-size: 20px;
  font-weight: 500;
  margin-left: 10px;
  margin-bottom: 0;
}

.Highlights ul {
  margin-top: 15px;
}

.Highlights ul li {
  text-align: left;
  color: #9e9e9e;
}

.Highlights ul li::marker {
  color: #3076da;
}

.Highlights .tow li::marker {
  color: #24c26b;
}

.titles {
  margin-top: 30px;
  font-size: 20px;
  font-weight: 500;
  text-align: left;
}

.labels {
  margin-top: 15px;
  text-align: left;

}
</style>
