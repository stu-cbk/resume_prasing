<template>
  <div class="content with-background">
    <div id="app">
      <v-app>
        <v-main>
          <v-data-table
            :headers="headers"
            :items="desserts"
            :items-per-page="15"
            class="elevation-1"
          >
            <template v-slot:item.操作="{ item }">
              <v-btn @click="viewDetails(item.id)">详情</v-btn>
            </template>
          </v-data-table>
        </v-main>
      </v-app>
    </div>
  </div>
</template>
  
<script>
import axios from "axios";

export default {
  data() {
    return {
      headers: [
        { text: "序号", align: "start", value: "id" },
        { text: "姓名", value: "name", sortable: false },
        { text: "年龄", value: "age" },
        { text: "工作年限", value: "workExperience" },
        { text: "最高学历", value: "mostEducation", sortable: false },
        { text: "毕业院校", value: "university", sortable: false },
        { text: "操作", value: "操作", sortable: false },
      ],
      desserts: [],
      count: 0,
    };
  },
  mounted() {
    this.fetchData();
    this.refreshTable(); // 第一次刷新
    setTimeout(() => {
      this.refreshTable(); // 第二次刷新，使用setTimeout延迟执行
    }, 1000);
  },
  methods: {
    fetchData() {
      axios
        .get("http://localhost:8181/api/resume/showBasicData")
        .then((response) => {
          // 处理基本数据的响应
          const basicData = response.data.data;

          // 调用其他接口获取最高学历和毕业院校数据
          return axios
            .get("http://localhost:8181/api/resume/showEducationalData")
            .then((response) => {
              // 处理最高学历和毕业院校数据的响应
              const educationalData = response.data.data;

              // 调用另一个接口获取工作年限数据
              return axios
                .get("http://localhost:8181/api/resume/showWorkData")
                .then((response) => {
                  // 处理工作年限数据的响应
                  const workData = response.data.data;

                  // 组合数据
                  const processedData = basicData.map((item, index) => ({
                    id: item.id,
                    name: item.name,
                    age: item.age,
                    mostEducation: educationalData[index].education,
                    university: educationalData[index].university,
                    workExperience: workData[index].workExperience,
                  }));

                  this.desserts = processedData;
                  console.log(this.desserts);
                })
                .catch((error) => {
                  console.error(error);
                });
            })
            .catch((error) => {
              console.error(error);
            });
        })
        .catch((error) => {
          console.error(error);
        });
    },

    viewDetails(id) {
      this.$router.push(`/details/${id}`);
    },
  },
};
</script>
  
<style>
.with-background {
  background-image: url("../assets/img/beijing.jpg");
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
  