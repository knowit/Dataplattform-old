<template>
  <div id="container">
    <div id="logo">
      <img src="@/assets/app-logo.svg" />
      <p id="event-name">{{eventName}}</p>
    </div>
    <div id="rating-btn-container" v-if="step===1">
      <rating-button
        v-for="i in [1, 0, -1]"
        :key="i"
        :btnType="i"
        @rating-click="step++"
        class="rating-btn"
      ></rating-button>
    </div>
    <div id="feedback-container" v-if="step===2">
      <label for="feedback">Hva likte du? Hva kunne vært bedre? (Valgfritt)</label>
      <br />
      <textarea v-model="text" id="feedback"></textarea>
      <div id="nav-btn-container">
        <button class="nav-btn back-btn" @click="step--">Tilbake</button>
        <button class="nav-btn next-btn" @click="finish">Ferdig</button>
      </div>
    </div>
  </div>
</template>

<script>
import RatingButton from "@/components/RatingButton.vue";
import router from "../router";

export default {
  name: "RatingPage",
  components: {
    RatingButton
  },
  data() {
    return {
      text: "",
      step: 1,
      eventName: "Test test test"
    };
  },
  methods: {
    ratingClick(rating) {
      alert(`Pressed: ${rating}`);
      this.step++;
    },
    finish() {
      router.push("finished");
    }
  },
  beforeRouteLeave(to, from, next) {
    if (this.step === 2 && to.name !== "finished") {
      this.step--;
      return next(false);
    }
    next();
  }
};
</script>

<style scoped>
#container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
}

#feedback-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

#feedback {
  color: #707070;
  border-radius: 2px;
  border-style: none;
  resize: none;
  height: 15em;
  width: 48em;
  padding: 2em;
  font: 400 14px "Roboto", sans-serif;
}

#nav-btn-container {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

#logo {
  position: relative;
  top: -128px;
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
  font: 400 12px "Roboto", sans-serif;
  margin-left: 2em;
  margin-top: 1em;
  border-radius: 2px;
}

.next-btn {
  background-color: var(--btn-blue);
  border: none;
  color: #fff;
}

.back-btn {
  background-color: rgba(0, 0, 0, 0);
  border: 2px solid #949494;
  color: #696969;
}

#event-name {
  color: #707070;
  font: 400 19px "Roboto", sans-serif;
  letter-spacing: 0;
}
</style>