<template>
  <div class="content with-background">
    <div class="row">
      <div class="col-1"></div>
      <div class="col-10">
        <div class="card-container">
          <Card shadow>
            <div class="resume-section-header">
              <div class="small-line-left-archieve"></div>
              <h4 class="section-word">学历信息</h4>
              <div class="small-line-right-archieve"></div>
            </div>
            <div>
              <el-row :gutter="20">
                <el-col :span="4">
                  <div>
                    <el-statistic
                      group-separator=","
                      :value="value1"
                      :title="title1"
                    ></el-statistic>
                  </div>
                </el-col>
                <el-col :span="4">
                  <div>
                    <el-statistic
                      group-separator=","
                      :value="value2"
                      :title="title2"
                    ></el-statistic>
                  </div>
                </el-col>
                <el-col :span="4">
                  <div>
                    <el-statistic
                      group-separator=","
                      decimal-separator="."
                      :value="value3"
                      :title="title3"
                    >
                      <template slot="prefix">
                        <i class="el-icon-s-flag" style="color: red"></i>
                      </template>
                      <template slot="suffix">
                        <i class="el-icon-s-flag" style="color: blue"></i>
                      </template>
                    </el-statistic>
                  </div>
                </el-col>
                <el-col :span="4">
                  <div>
                    <el-statistic :value="value4" :title="title4">
                      <template slot="suffix">
                        <span @click="toggleLike" class="like">
                          <i
                            class="el-icon-star-on"
                            style="color: red"
                            v-show="like"
                          ></i>
                          <i
                            class="el-icon-star-off"
                            v-show="!like"
                          ></i>
                        </span>
                      </template>
                    </el-statistic>
                  </div>
                </el-col>
                <el-col :span="4">
                  <div>
                    <el-statistic
                      group-separator=","
                      :value="value5"
                      :title="title5"
                    ></el-statistic>
                  </div>
                </el-col>
              </el-row>
            </div>
            <div class="resume-section-header">
              <div class="small-line-left-archieve"></div>
              <h4 class="section-word">其他信息</h4>
              <div class="small-line-right-archieve"></div>
            </div>
            <v-tabs v-model="activeTab">
              <v-tab @click="activeTab = 0">毕业院校</v-tab>
              <v-tab @click="activeTab = 1">工作时长</v-tab>
              <v-tab @click="activeTab = 2">年龄</v-tab>
            </v-tabs>

            <div class="card-body">
              <ve-donut-chart
                v-if="activeTab === 0"
                :data="chartData1"
                :settings="chartSettings1"
              />
              <ve-donut-chart
                v-if="activeTab === 1"
                :data="chartData2"
              />
              <ve-pie-chart
                v-if="activeTab === 2"
                :data="chartData3"
                :settings="chartSettings3"
              />
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Card } from "@/components/index";
import axios from 'axios';

export default {
  components: {
    Card,
  },
  data() {
    return {
      like: true,
      title1: "博士",
      title2: "硕士",
      title3: "本科",
      title4: "专科",
      title5: "其他",

      activeTab: 0,
      chartData1: {},
      chartData2: {},
      chartData3: {},
      chartSettings1: {
        radius: ["35%", "55%"],
      },
      chartSettings3: {
        selectedMode: "single",
      },
    };
  },
  created() {
    // Fetch data from the backend API and assign it to the appropriate variables
    this.fetchChartData();
  },
  methods: {
    fetchChartData() {
      // Make an API call to fetch the data
      axios.get("http://localhost:8181/api/resume/classifyData")
        .then(response => {
          console.log(response)
          const data = response.data.data;
          this.value1 = data.education['博士'];
          this.value2 = data.education['硕士'];
          this.value3 = data.education['本科'];
          this.value4 = data.education['专科'];
          this.value5 = data.education['其他'];
          
          // console.log(data.education);

          // Update chartData1 with university data
          this.chartData1 = {
            dimensions: {
              name: "渠道",
              data: Object.keys(data.university),
            },
            measures: [
              {
                name: "PV",
                data: Object.values(data.university),
              },
            ],
          };

          // Update chartData2 with work experience data
          this.chartData2 = {
            dimensions: {
              name: "渠道",
              data: Object.keys(data.workExperience),
            },
            measures: [
              {
                name: "PV",
                data: Object.values(data.workExperience),
              },
            ],
          };

          // Update chartData3 with age data
          this.chartData3 = {
            dimensions: {
              name: "渠道",
              data: Object.keys(data.age),
            },
            measures: [
              {
                name: "PV",
                data: Object.values(data.age),
              },
            ],
          };
        })
        .catch(error => {
          console.error(error);
        });
    },
    toggleLike() {
      this.like = !this.like;
    },
  },
};
</script>

<style lang="scss">
.like {
  cursor: pointer;
  font-size: 25px;
  display: inline-block;
}

.resume-section-header {
  margin-top: 30px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
}

.resume-section-header .section-word:after {
  content: "";
  position: absolute;
  top: 20px;
  left: 15px;
  width: 110%;
  height: 20px;
  background: rgba(103, 137, 229, 0.16);
}

.resume-section-header .section-word {
  text-align: center;
  color: #32325d;
  font-weight: 400;
  line-height: 30px;
  font-size: 24px;
  margin-bottom: 0;
  position: relative;
}

.tab-item {
  color: blue;
}

.with-background {
  background-image: url("../assets/img/beijing.jpg");
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
