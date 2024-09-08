<template>
  <div :class="$store.state.isMobile ? 'myInforBox myInforBox_mobile' : 'myInforBox'">
    <div class="topBox">
      <div class="leftBox">
        <span class="nameCn">{{myiInfo.name}}</span>
        <span class="nameEn">{{myiInfo.nameEn}}</span>
      </div>
      <div class="rightBox">
        <span class="post">期望职业：{{myiInfo.jobWant}} {{myiInfo.moneyWant}}</span>
        <!-- <img class="portrait" src="https://q1.qlogo.cn/g?b=qq&nk=1937966358&s=100" alt="" /> -->
      </div>
    </div>
    <div class="bottomBox">
      <div class="leftBox">
        <p>性别&nbsp;&nbsp;{{myiInfo.gender}}</p>
        <p>学历&nbsp;&nbsp;{{myiInfo.edu}}</p>
        <p>现居&nbsp;&nbsp;{{myiInfo.address}}</p>
        <p>电话&nbsp;&nbsp;{{myiInfo.phone}}</p>
        <p class="block">邮箱&nbsp;&nbsp;{{myiInfo.email}}</p>
      </div>
      <div class="rightBox">
        <p>
          <a target="_blank" :href="myiInfo.github">
            <span>我的Github</span>&nbsp;&nbsp;<i class="sg sg-github-fill"></i>
          </a>
        </p>
        <p>
          <a target="_blank" :href="myiInfo.gitee">
            <span>我的Gitee</span>&nbsp;&nbsp;<i class="sg sg-gitee-fill-round"></i>
          </a>
        </p>
        <p>
          <a target="_blank" :href="myiInfo.blog">
            <span>我的个人博客</span>&nbsp;&nbsp;<i class="sg sg-dingyue"></i>
          </a>
        </p>
        <p>
          <a target="_blank" :href="myiInfo.csdn">
            <span>我的CSDN</span>&nbsp;&nbsp;<i class="sg sg-csdn1"></i>
          </a>
        </p>
        <p>
          <a target="_blank" :href="myiInfo.juejin">
            <span>我的稀土掘金</span>&nbsp;&nbsp;<i class="sg sg-signal"></i>
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    myiInfo: {}
  },
}
</script>

<style lang="scss" scoped>
.topBox {
  border-bottom: 1px solid #fff;
  padding: 10px 0;
  display: flex;
  vertical-align: top;
  justify-content: space-between;
  align-items: center;

  >.leftBox {
    >.nameCn {
      font-size: 50px;
      letter-spacing: 2px;
    }

    >.nameEn {
      font-size: 25px;
      padding-left: 30px;
    }
  }

  >.rightBox {
    display: flex;
    vertical-align: top;
    align-items: center;


    >.post {
      font-weight: 300;
      font-size: 25px;
      padding-right: 20px;
    }

    >.portrait {
      border-radius: 50%;
      width: auto;
      height: 50px;
    }
  }
}

.bottomBox {
  line-height: 30px;
  padding: 15px 0 0 0;
  display: flex;
  vertical-align: top;
  justify-content: space-between;

  >.rightBox {
    text-align: right;
    font-size: 14px;
    letter-spacing: .5px;

    >p {
      >a {
        padding-left: 10px;

        >i {
          font-size: 12px;
          background: #fff;
          color: #00bdc4;
          border-radius: 50%;
          padding: 2px;
          font-weight: bold;
        }
      }
    }
  }
}

.myInforBox_mobile {

  >.topBox {
    display: block;
    text-align: center;

    >.leftBox {
      padding-bottom: 15px;
    }

    >.rightBox {
      justify-content: center;

      >.post {
        display: none;
      }
    }

  }

  >.bottomBox {
    display: block;

    >.leftBox {
      display: grid;
      grid-template-columns: repeat(auto-fill, 50%);

      >.block {
        width: max-content;
      }
    }

    >.rightBox {
      display: none;
    }
  }
}
</style>