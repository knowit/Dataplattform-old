<template>
  <div id="div">
    <img src="../assets/app-logo.svg" />
    <div id="input">
      <code-input></code-input>
      <button id="ok-button">OK</button>
    </div>
  </div>
</template>

<script>
import CodeInput from "./CodeInput.vue";

export default {
  components: {
    CodeInput
  },
  data() {
    return {
      code: ""
    };
  },
  methods: {
    reverseCode: function() {
      this.code = "hehe";
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
  font-size: 25px;
  padding: 11px 13px;
  background: #e3e3e3 0% 0% no-repeat padding-box;
  border: 2px solid #e3e3e3;
  border-radius: 8px;
  opacity: 1;
  text-align: center;
  font: Regular 28px/32px Arial;
  letter-spacing: 0;
  color: #afafaf;
  margin-left: 8px;
}
</style>