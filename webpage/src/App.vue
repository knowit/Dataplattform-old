<template>
  <div id="app">
    <!--<img alt="Vue logo" src="./assets/logo.png">-->
    <!--<HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <!-- <rating-button
      v-for="i in [-1, 0, 1]"
      :key="i"
      :btnType="i"
      v-on:rating-click="ratingClick"
      class="btn"
    ></rating-button>-->
    <start-page></start-page>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
//import RatingButton from "./components/RatingButton.vue";
import StartPage from "./components/StartPage.vue";

export default {
  name: "app",
  components: {
    //RatingButton,
    StartPage
  },

  methods: {
    ratingClick: rating => {
      alert(`You pressed ${rating}`);
    }
  }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Roboto&display=swap");
#app {
  font-family: "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

html {
  background-color: #f1f0ed;
  height: 100vh;
}

body {
  height: 100%;
  margin: 0;
}
</style>
