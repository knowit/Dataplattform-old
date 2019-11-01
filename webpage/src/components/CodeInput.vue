<template>
  <div id="container">
    <input
      class="input-field"
      maxlength="1"
      v-on:keyup="back($event,n)"
      v-on:input="next($event, n)"
      v-model="text[n]"
      ref="input"
      v-for="n in 5"
      :key="n"
      v-on:focus="$event.target.select()"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: []
    };
  },

  methods: {
    next(event, n) {
      if (this.text[n] && this.text[n] !== " " && n < 5) {
        this.$refs.input[n].focus();
      }
    },
    back(event, n) {
      if (
        event.key === "Backspace" &&
        (!this.text[n] || this.text[n] === "") &&
        n > 1
      ) {
        this.$refs.input[n - 2].focus();
      }
    }
  }
};
</script>

<style scoped>
.input-field {
  font-size: 25px;
  padding: 11px 45px;
  background: #ffffff 0% 0% no-repeat padding-box;
  border: 2px solid #e3e3e3;
  border-radius: 8px;
  opacity: 1;
  text-align: center;
  font: Regular 28px/32px Arial;
  letter-spacing: 0;
  color: #707070;
  width: 1em;
}
</style>