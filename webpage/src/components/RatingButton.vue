<template>
  <div id="div">
    <button id="button" :style="style" v-on:click="click">{{ btnText }}</button>
  </div>
</template>

<script>
export default {
  props: {
    btnType: {
      validator: function(value) {
        return [-1, 0, 1].indexOf(value) !== -1;
      }
    }
  },

  computed: {
    style: function() {
      if (this.btnType === -1) {
        return "background-color: #FF615F";
      } else if (this.btnType === 0) {
        return "background-color: #FFFB5F";
      } else if (this.btnType === 1) {
        return "background-color: #5FFF8E";
      } else {
        return "";
      }
    },
    btnText: function() {
      if (this.btnType === -1) {
        return ":(";
      } else if (this.btnType === 0) {
        return ":|";
      } else if (this.btnType === 1) {
        return ":)";
      } else {
        return "";
      }
    }
  },
  methods: {
    click: function() {
      this.$emit("rating-click", this.btnType);
    }
  }
};
</script>

<style scoped>
#button {
  font-size: 18pt;
  height: 9em;
  width: 9em;
  /* padding: 48px; */
  border-radius: 50%;
  border: none;
  margin: 1em;
}
</style>