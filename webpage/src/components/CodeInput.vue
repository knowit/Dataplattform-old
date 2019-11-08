<template>
  <div id="container">
    <input
      class="input-field"
      maxlength="1"
      v-on:keyup="back($event,n)"
      v-on:input="next($event, n)"
      v-model="text[n-1]"
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

  watch: {
    text: function(newText) {
      this.$emit("input", newText.join("").toUpperCase());
    }
  },

  methods: {
    next(event, n) {
      if (this.text[n - 1] && this.text[n - 1] !== " " && n < 5) {
        this.$refs.input[n].focus();
      }
    },
    back(event, n) {
      if (
        event.key === "Backspace" &&
        (!this.text[n - 1] || this.text[n - 1] === "") &&
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
  width: 1.3em;
  height: 1.3em;
  font: Regular 20px/24px Roboto;
  font-size: 25px;
  margin-right: 5px;
  margin-left: 5px;
  background: #ffffff 0% 0% no-repeat padding-box;
  border: none;
  border-radius: 2px;
  opacity: 1;
  text-align: center;
  letter-spacing: 0;
  color: #707070;
  text-transform: uppercase;
}
</style>