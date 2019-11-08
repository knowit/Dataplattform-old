<template>
  <button id="button" :class="style" v-on:click="click"></button>
</template>

<script>
export default {
  data() {
    return {
      style: {
        negative: this.btnType === -1,
        neutral: this.btnType === 0,
        positive: this.btnType === 1
      }
    };
  },

  props: {
    btnType: {
      validator: function(value) {
        return [-1, 0, 1].indexOf(value) !== -1;
      }
    }
  },

  // computed: {
  //   btnText: function() {
  //     if (this.btnType === -1) {
  //       return ":(";
  //     } else if (this.btnType === 0) {
  //       return ":|";
  //     } else if (this.btnType === 1) {
  //       return ":)";
  //     } else {
  //       return "";
  //     }
  //   }
  // },
  methods: {
    click: function() {
      this.$emit("rating-click", this.btnType);
    }
  }
};
</script>

<style scoped>

#button {
  border: 2px solid #FFF;
  opacity: 1;
  outline: none;
  backdrop-filter: blur(50px);
}

.negative {
  background-color: #ff615f;
}

.neutral {
  background-color: #fffb5f;
}

.positive {
  background-color: #5fff8e;
}
</style>