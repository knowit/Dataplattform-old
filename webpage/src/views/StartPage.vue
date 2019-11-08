<template>
  <div id="div">
    <img src="../assets/app-logo.svg" />
    <div id="input">
      <code-input v-model="code"></code-input>
      <button id="ok-button" v-bind:class="{ active: isActive}" v-on:click="handleClick">Neste</button>
    </div>
  </div>
</template>

<script>
import CodeInput from "@/components/CodeInput.vue";
import router from "../router";

export default {
  components: {
    CodeInput
  },
  data() {
    return {
      code: "",
      isActive: false
    };
  },
  methods: {
    handleClick() {
      if (this.isActive) {
        router.push(this.code);
      }
    }
  },

  watch: {
    code: function() {
      this.isActive = this.code.length === 5;
    }
  }
};
</script>

<style scoped>
#input {
  margin-top: 22px;
}
#input-field:focus {
  outline: 0;
}

#ok-button:focus {
  outline: 0;
}

#ok-button {
  width: 91%;
  padding: 11px 13px;
  background: #949494 0% 0% no-repeat padding-box;
  border: none;
  border-radius: 2px;
  opacity: 1;
  text-align: center;
  font: Regular 12px/14px Roboto;
  letter-spacing: 0;
  color: #ffffff;
  margin-top: 10px;
}
.active {
  background-color: #4573e3 !important;
}
</style>