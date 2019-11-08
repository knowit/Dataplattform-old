import Vue from "vue";
import VueRouter from "vue-router";
import StartPage from "../views/StartPage.vue";
import RatingPage from "../views/RatingPage.vue";
import Finished from '../views/Finished.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "start-page",
    component: StartPage
  },
  {
    path: "/finished",
    name: "finished",
    component: Finished
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
