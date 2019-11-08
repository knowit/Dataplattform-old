import Vue from "vue";
import VueRouter from "vue-router";
import StartPage from "../views/StartPage.vue";
import RatingPage from "../components/RatingPage";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "start-page",
    component: StartPage
  },
  {
    path: "/:eventCode",
    name: "rating-page",
    component: RatingPage
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

export default router;
