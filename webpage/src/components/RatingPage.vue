<template>
  <div id="container">
    <div id="rating-btn-container" v-if="step===1">
      <rating-button
        v-for="i in [1, 0, -1]"
        :key="i"
        :btnType="i"
        v-on:rating-click="step++"
        class="rating-btn"
      ></rating-button>
    </div>
    <div id="txt-container" v-if="step===2">
      <textarea v-model="text" id="feedback"></textarea>
      <div id="nav-btn-container">
        <button class="nav-btn back-btn" @click="step--">Back</button>
        <button class="nav-btn next-btn" @click="step++">Next</button>
      </div>
    </div>
  </div>
</template>

<script>
import RatingButton from "./RatingButton.vue";

export default {
  name: "RatingPage",
  components: {
    RatingButton
  },
  data() {
    return {
      text: "",
      step: 1
    };
  },
  methods: {
    ratingClick(rating) {
      alert(`Pressed: ${rating}`);
      this.step++;
    }
  }
};
</script>

<style scoped>
#container {
  display: flex;
  justify-content: center;
}

#feedback {
  color: #707070;
  border-radius: 2px;
  border-style: none;
  resize: none;
  height: 15em;
  width: 50em;
}

#nav-btn-container {
  display: flex;
  justify-content: flex-end;
}

.rating-btn {
  font-size: 18pt;
  height: 9em;
  width: 9em;
  /* padding: 48px; */
  border-radius: 50%;
  border: none;
  margin: 1em;
}

.nav-btn {
  font-size: 14px;
  padding: 1em 3em;
}

.next-btn {
  background-color: var(--btn-blue);
}

.back-btn {
  background-color: rgba(0,0,0,0);
}
</style>