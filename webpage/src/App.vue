<template>
  <div id="app">
    <!--<img alt="Vue logo" src="./assets/logo.png">-->
    <!--<HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <rating-page></rating-page>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import RatingPage from './components/RatingPage.vue'

export default {
  name: 'app',
  components: {
    RatingPage
  },

  methods: {
    ratingClick: (rating) => {
      alert(`You pressed ${rating}`)
    }
  },
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');
#app {
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

:root {
  --btn-blue: #4573E3;
}

</style>
