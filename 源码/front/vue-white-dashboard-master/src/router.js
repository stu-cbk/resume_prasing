import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Statistics from "@/pages/Statistics.vue";
import Details from "@/pages/Details.vue";
import SingleData from "@/pages/SingleData.vue";

// import Icons from "@/pages/Icons.vue";
import Matching from "@/pages/Matching.vue"

import UploadFile from "@/pages/UploadFile.vue";
import singleloadFile from "@/pages/singleloadFile.vue";
// import Makeshow from "@/pages/Makeshow.vue";
// import Maps from "@/pages/Maps.vue";
// import Notifications from "@/pages/Notifications.vue";
// import UserProfile from "@/pages/UserProfile.vue";
import TableList from "@/pages/TableList.vue";
// import Typography from "@/pages/Typography.vue";
import UpgradeToPRO from "@/pages/UpgradeToPRO.vue";

const routes = [
  {
    path: "/",
    component: DashboardLayout,
    redirect: "singleDataFile",
    children: [
      {
        path: "statistics",
        name: "Data Statistics",
        component: Statistics,
      },
      {
        path: "multiData",
        name: "File Upload",
        component: UploadFile,
      },
      {
        path: "singleDataFile",
        name: "File Upload",
        component: singleloadFile,
      },
      // {
      //   path: "makeshow",
      //   name: "showmake",
      //   component: Makeshow,
      // },

      // {
      //   path: "icons",
      //   name: "icon",
      //   component: Icons,
      // },
      {
        path: "matchjob",
        name: "matchjob",
        component: Matching,
      },


      // {
      //   path: "maps",
      //   name: "Maps",
      //   component: Maps,
      // },
      // {
      //   path: "notifications",
      //   name: "Notifications",
      //   component: Notifications,
      // },
      // {
      //   path: "user",
      //   name: "User Profile",
      //   component: UserProfile,
      // },
      {
        path: "table",
        name: "Data Show",
        component: TableList,
      },
      // {
      //   path: "typography",
      //   name: "Typography",
      //   component: Typography,
      // },
      {
        path: 'details/:id',
        name: 'Details',
        component: Details,
      },
      {
        path: "upgradeToPro",
        name: "Upgrade to PRO",
        component: UpgradeToPRO,
      },
      {
        path: 'singleData',
        name: 'SingleData',
        component: SingleData,
      },
    ],
  },
];

export default routes;
