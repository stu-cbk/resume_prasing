<!-- 项目经历 -->
<template>
  <div class="introBox">

    <div class="titleBox">
      <p class="line"></p>
      <p class="title">
        <span>项目经历</span>
      </p>
    </div>

    <div class="introCon">
      <ul class="projectBox">
        <li></li>
      </ul>
    </div>

  </div>
</template>

<script>
export default {
  methods: {
    open() {
      this.$alert(
        "<img src='https://img.timebk.cn/时光搜题/时光搜题小程序.jpg'>",
        "微信扫码使用",
        {
          dangerouslyUseHTMLString: true,
          center: true,
          showConfirmButton: false,
        }
      );
    },
  },
};
</script>

<style lang="scss" scoped>
</style>