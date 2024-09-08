<template>
  <card type="user">
    <div class="author">
      <div class="block block-one"></div>
      <div class="block block-two"></div>
      <div class="block block-three"></div>
      <div class="block block-four"></div>
      <a href="#">
        <img class="avatar" alt="..." v-if="user.gender === '男'" src="../../assets/img/anime3.png" />
        <img class="avatar" alt="..." v-else src="../../assets/img/anime6.png" />
        <h5 class="title">{{ user.gender }}</h5>
      </a>
      <p class="description">
        {{ user.title }}
      </p>
    </div>
    <p class="card-description">
      {{ user.description }}
    </p>

  </card>
</template>
<script>
import { Card } from "@/components/index";


export default {
  components: {
    Card,

  },
  props: {
    user: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
};
</script>
<style></style>
