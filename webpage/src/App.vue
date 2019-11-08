<template>
  <div id="app">
    <start-page></start-page>
  </div>
</template>

<script>
import StartPage from "./components/StartPage.vue";

export default {
  name: "app",
  components: {
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
