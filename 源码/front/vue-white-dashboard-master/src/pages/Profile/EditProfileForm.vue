<template>
  <card>
    <template slot="header">
      <h5 class="title">详细信息</h5>
    </template>
    <div class="row">
      <div class="col-md-5 pr-md-1 text-left">
        <base-input
          label="姓名"
          placeholder="Username"
          v-model="model.Username"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-3 px-md-1 text-left">
        <base-input
          label="性别"
          placeholder="gender"
          v-model="model.gender"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-4 pl-md-1 text-left">
        <base-input
          label="政治面貌"
          placeholder="identity"
          v-model="model.identity"
          disabled
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-2 pr-md-1 text-left">
        <base-input
          label="年龄"
          v-model="model.age"
          placeholder="age"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-2 px-md-1 text-left">
        <base-input
          label="工作年限"
          v-model="model.workExperimence"
          placeholder="workTime"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-2 px-md-1 text-left">
        <base-input
          label="英语等级"
          v-model="model.english"
          placeholder="english"
          disabled
        >
        </base-input>
      </div>

      <div class="col-md-6 pl-md-1 text-left">
        <base-input
          label="现居住地"
          v-model="model.origin"
          placeholder="origin"
          disabled
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-2 pr-md-1 text-left">
        <base-input
          label="学历"
          v-model="model.education"
          placeholder="edu"
          disabled
        >
        </base-input>
      </div>

      <div class="col-md-5 px-md-1 text-left">
        <base-input
          label="专业"
          v-model="model.major"
          placeholder="major"
          disabled
        >
        </base-input>
      </div>
      
      <div class="col-md-5 pl-md-1 text-left">
        <base-input
          label="毕业院校"
          v-model="model.university"
          placeholder="university"
          disabled
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-3 pr-md-1 text-left">
        <base-input
          label="目标工作"
          v-model="model.targetjob"
          placeholder="targetjob"
          disabled
        >
        </base-input>
      </div>

      <div class="col-md-5 px-md-1 text-left">
        <base-input
          label="曾所在公司"
          v-model="model.companies"
          placeholder="companies"
          disabled
        >
        </base-input>
      </div>
    </div>



    <div class="row">
      <div class="col-md-6 text-left">
        <base-input
          label="手机号码"
          v-model="model.phone"
          placeholder="phone"
          disabled
        >
        </base-input>
      </div>
      
      <div class="col-md-6 pl-md-1 text-left">
        <base-input
          label="邮箱"
          type="email"
          placeholder="@email.com"
          v-model="model.email"
          disabled
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-8 text-left">
        <base-input>
          <label>历史工作</label>
          <textarea
            rows="4"
            cols="80"
            class="form-control"
            placeholder="Here can be your works"
            v-model="model.jobs"
            disabled
          >
          </textarea>
        </base-input>
      </div>
    </div>
    <!-- <template slot="footer">
      <div class="row">
        <div class="col-md-4 pr-md-1 text-left">
          <base-button type="success" fill>上一个</base-button>
        </div>
        <div class="col-md-4">
          <base-button type="success" fill>人才画像</base-button>
        </div>
        <div class="col-md-2 px-md-1 text-right">
          <base-button type="success" fill>下一个</base-button>
        </div>
      </div>
    </template> -->
  </card>
</template>
<script>
import { Card, BaseInput } from "@/components/index";

// import BaseButton from "@/components/BaseButton";

export default {
  components: {
    Card,
    BaseInput,
    // BaseButton,
  },
  props: {
    model: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
};
</script>
<style>
</style>
