<template>
  <div class="wrapper">
    <!-- <div class="wrapper" :class="{'nav-open': $sidebar.showSidebar}"> -->

    <side-bar :background-color="backgroundColor">
      <!-- <mobile-menu slot="content"></mobile-menu> -->
      <!--侧边栏的设计-->

      <sidebar-link to="/singleDataFile">
        <i class="tim-icons icon-cloud-upload-94"></i>

        <template v-if="!isRTL">
          <p>文件上传</p>
        </template>

        <template v-else>
          <p>لوحة القيادة</p>
        </template>
      </sidebar-link>

      <sidebar-link to="/matchjob">
        <i class="tim-icons icon-zoom-split"></i>

        <template v-if="!isRTL">
          <p>岗位匹配</p>
        </template>

        <template v-else>
          <p>ملف تعريفي للمستخدم</p>
        </template>
      </sidebar-link>

      <sidebar-link to="/table">
        <i class="tim-icons icon-puzzle-10"></i>

        <template v-if="!isRTL">
          <p>数据展示</p>
        </template>

        <template v-else>
          <p>قائمة الجدول</p>
        </template>
      </sidebar-link>

      <sidebar-link to="/statistics">
        <i class="tim-icons icon-chart-pie-36"></i>

        <template v-if="!isRTL">
          <p>数据统计</p>
        </template>

        <template v-else>
          <p>لوحة القيادة</p>
        </template>
      </sidebar-link>
    </side-bar>

    <sidebar-share :background-color.sync="backgroundColor"></sidebar-share>

    <div class="main-panel" :data="backgroundColor">
      <top-navbar></top-navbar>
      <!--顶部导航栏-->

      <dashboard-content @click.native="toggleSidebar"></dashboard-content>
      <!--仪表板内容-->

      <!-- <content-footer></content-footer> -->
      <!--内容页脚-->
    </div>
  </div>
</template>

<style lang="scss"></style>

<script>
import TopNavbar from "./TopNavbar.vue";
import DashboardContent from "./DashboardContent.vue";
import SidebarShare from "./SidebarSharePlugin.vue";
import MobileMenu from "./MobileMenu.vue";
import SideBar from "@/components/SidebarPlugin/SideBar.vue";
import SidebarLink from "@/components/SidebarPlugin/SidebarLink.vue";

export default {
  components: {
    TopNavbar,
    DashboardContent,
    // eslint-disable-next-line vue/no-unused-components
    MobileMenu,
    SideBar,
    SidebarLink,
    SidebarShare,
  },
  data() {
    return {
      backgroundColor: "blue",
    };
  },
  computed: {
    isRTL() {
      return this.$rtl.isRTL;
    },
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
  },
};
</script>
