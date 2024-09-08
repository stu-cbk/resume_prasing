<template>
  <div class="content">
    <div class="upload">
      <el-upload
        class="upload-demo"
        drag
        :action="uploadUrl"
        :multiple="true"
        :on-success="handleSuccess"
        :on-error="handleError"
        :on-exceed="handleExceed"
      >
        <div class="el-upload__text"><em>单文件上传</em></div>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <!-- <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div> -->
      </el-upload>
      <el-button size="small" type="primary" @click="callApi">解析文件</el-button>
      <el-progress v-if="turnTar" :percentage="progress" />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      uploadUrl: "http://localhost:5000/singleData/upload",
      detail: "",
      turnTar: false,
      progress: 0,
    };
  },
  methods: {
    handleSuccess() {
      this.turnTar = true;
      console.log("跳转");
      this.$message.success("文件上传成功！");
    },
    handleError() {
      this.turnTar = false;
      this.$message.error("文件上传失败！");
    },
    callApi() {
      if (this.turnTar) {
        // Make an HTTP request to the API
        // Assuming you are using axios for making HTTP requests
        axios
          .post(
            "http://localhost:5000/singleData/dealFile",
            {},
            {
              onUploadProgress: (progressEvent) => {
                this.progress = Math.round(
                  (progressEvent.loaded / progressEvent.total) * 90
                );
              },
            }
          )
          .then((response) => {
            this.detail = response.data;
            localStorage.setItem("detail", JSON.stringify(this.detail));
            this.$router.push(`/singleData`);
          })
          .catch((error) => {
            // Handle any error that occurs during the API call
            console.error(error);
            // You can show an error message or perform other actions based on the error
          });
      }
      console.log("不跳转");
    },
  },
};
</script>
