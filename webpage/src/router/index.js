import Vue from "vue";
import VueRouter from "vue-router";
import StartPage from "../views/StartPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "start-page",
    component: StartPage
  },
  {
    path: "/:eventCode"
  }
];

const router = new VueRouter({
  routes
});

export default router;
