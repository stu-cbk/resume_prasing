<!-- 开源项目 -->
<template>
  <div class="introBox">

    <div class="titleBox">
      <p class="line"></p>
      <p class="title">
        <span>开源项目</span>
      </p>
    </div>

    <div class="introCon" v-for="item in array">
      <ul class="projectBox">
        <li class="projectTitle">
          <p class="bold projectTitleLeft">
            <a href="javascript:void (0)" @click="openImg(item.open.name, item.open.url)" v-if="item.open.type == 0">
              {{ item.name }}
            </a>
            <a target="_blank" :href="item.open.url" v-if="item.open.type == 1">
              {{ item.name }}
            </a>
          </p>
          <p class="projectTitleRight">
            <a :target="item.url.gitee == '' ? '' : '_blank'"
              :href="item.url.gitee == '' ? 'javascript:void(0)' : item.url.gitee">
              <i class="sg sg-gitee-fill-round"></i>
            </a>
            <a :target="item.url.github == '' ? '' : '_blank'"
              :href="item.url.github == '' ? 'javascript:void(0)' : item.url.github">
              <i class="sg sg-github-fill"></i>
            </a>
            <span>|</span>
            <a href="javascript:void (0)" @click="openImg(item.open.name, item.open.url)"
              v-if="item.open.type == 0">线上体验</a>
            <a target="_blank" :href="item.open.url" v-if="item.open.type == 1">线上体验</a>
          </p>
        </li>
        <li v-for="itemb in item.text" v-html="itemb"></li>
      </ul>
    </div>

  </div>
</template>
<!-- npm i element-ui -S -->
<script>
export default {
  data() {
    return {
      array: [
        {
          name: "时光搜题小程序 - 微信小程序原生",
          url: {
            gitee: '',
            github: '',
          },
          open: {
            type: 0, // 0为打开弹窗二维码；1为用新窗口打开链接
            name: '时光搜题小程序',
            url: 'https://img.timebk.cn/时光搜题/时光搜题小程序.jpg',
          },
          text: [
            '答案查询小程序，查题积分制，可结合流量主实现积分奖励',
            '主要功能 <span span class= "keyW1" > 从服务器获取配置</span>、<span class="keyW1">完整的前后端登录流程</span>、 <span class= "keyW1" > 自定义查题接口</span >、<span class="keyW1">搜题记录</span>(可删) 等',
            '积分功能 <span class="keyW1">看广告加积分</span>、<span class="keyW1">查题扣积分</span>',
            '额外功能 <span class="keyW1">抖音无水印解析</span>(需服务器反向代理)、<span class="keyW1">工具箱</span>(可根据模板自行添加)',
          ]
        },
        {
          name: "个人简历 - Vue2 + Element UI",
          url: {
            gitee: 'https://gitee.com/time-demon/personal-resume',
            github: 'https://github.com/time-demon/personal-resume',
          },
          open: {
            type: 0, // 0为打开弹窗二维码；1为用新窗口打开链接
            name: '个人简历',
            url: 'https://img.timebk.cn/时光搜题/个人简历Vue.png',
          },
          text: [
            '漂亮的原创个人简历Vue2源码，提供模块化模板',
            '没错，就是您当前看到的这个在线简历',
            '额外功能 <span class="keyW1">简历PDF下载</span>(有的样式因为依赖本身的问题会不正常)',
          ]
        },
        {
          name: "API管理系统 - jQuery + Layui",
          url: {
            gitee: 'https://gitee.com/time-demon/api-system',
            github: 'https://github.com/time-demon/api-system',
          },
          open: {
            type: 1, // 0为打开弹窗二维码；1为用新窗口打开链接
            name: 'API管理系统',
            url: 'http://apisys.timebk.cn/',
          },
          text: [
            '管理第三方API或自己写的后端API，很漂亮的UI界面',
            '主要功能 <span class="keyW1">在线检测接口是否可用</span>、<span class="keyW1">增删改查</span>、<span class="keyW1">是否在前台可见</span>、<span class="keyW1">自定义对接方式【GET/POST】</span>、<span class="keyW1">自定义返回码</span> 等',
          ]
        },
      ]
    }
  },
  methods: {
    openImg(title, img) {
      let _this = this;
      this.$alert(
        `<img src="${img}">`,
        `${title}`,
        {
          dangerouslyUseHTMLString: true,
          center: true,
          showConfirmButton: false
        }
      )
    },
  },
};
</script>

<style lang="scss" scoped>
.introCon {
  padding: 15px 10px 5px 30px !important;

}
</style>