<template>
  <div class="introBox">

    <div class="titleBox">
      <p class="line"></p>
      <p class="title">
        <span>专业技能</span>
      </p>
    </div>

    <div class="introCon">
      <ul>
        <li v-for="item in sills" v-html="item"></li>
      </ul>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      sills: [
        '熟练 <span class="keyW1">HTML5</span>、<span class="keyW1">CSS3</span>、<span class="keyW1">JS</span>、<span class="keyW1">ES6</span> 等前端基础',
        '熟悉使用<span class="keyW1">vue框架</span>、<span class="keyW1">vue-router</span>、<span class="keyW1">vue-cli脚手架</span>、<span class="keyW1">Element-UI</span>进行MVVM模式下的项目搭建与前后端交互',
        '熟悉<span class="keyW1">JQuery</span>+<span class="keyW1">Layui</span>开发项目，有<span class="keyW1">API管理系统</span>上线',
        '熟悉<span class="keyW1">axios</span>二次封装、请求前后拦截',
        '熟悉<span class="keyW1">微信小程序</span>原生开发，有<span class="keyW1">时光搜题</span>线上完整项目上线',
        '熟练<span class="keyW1">Node.js</span>结合<span class="keyW1">MongoDB</span>开发后端接口并部署到服务器，实现个人开源项目的云端数据',
        '熟悉使用<span class="keyW1">Git</span>控制工具，已将多个个人开源项目发布到Github和Gitee',
        '熟悉在各场景下运用css常用预处理器<span class="keyW1">sass</span>',
        '了解前端打包工具<span class="keyW1">webpack</span>，浅接触下一代前端打包工具<span class="keyW1">Vite</span>，包管理<span class="keyW1">npm</span>、<span class="keyW1">cnpm</span>、<span class="keyW1">yarn</span>',
      ]
    }
  }
};
</script>

<style lang="scss" scoped>

</style>