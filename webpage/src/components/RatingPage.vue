<template>
  <div id="container">
    <rating-button v-for="i in [-1, 0, 1]" :key="i" :btnType="i" v-on:rating-click="ratingClick" class="btn" ></rating-button>
  </div>
</template>

<script>

import RatingButton from './RatingButton.vue'

function ratingClick(rating) {
  alert(`Pressed: ${rating}`)
}

export default {
  name: 'RatingPage',
  components: {
    RatingButton
  },
  methods: {
    ratingClick: ratingClick
  },
}
</script>

<style scoped>

#container {
  display: flex;
  justify-content: center;
  flex-direction: row-reverse;
}
  
</style>