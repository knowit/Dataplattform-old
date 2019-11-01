<template>
  <div id="app">
    <!--<img alt="Vue logo" src="./assets/logo.png">-->
    <!--<HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <rating-button v-for="i in [-1, 0, 1]" :key="i" :btnType="i" v-on:rating-click="ratingClick" class="btn" ></rating-button>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import RatingButton from './components/RatingButton.vue'

export default {
  name: 'app',
  components: {
    RatingButton
  },

  methods: {
    ratingClick: (rating) => {
      alert(`You pressed ${rating}`)
    }
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.btn {
  display: inline-block;
  size: 42px;
}

</style>
