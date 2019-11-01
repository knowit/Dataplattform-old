<template>
  <div id="div">
    <button id="button" :style="style" onClick="click">
      {{ btnText }}
    </button>
  </div>
</template>

<script>
export default {
  props: {
    btnType: {
      validator: function (value) {
        return [-1, 0, 1].indexOf(value) !== -1
      }
    }
  },

  computed: {
    style: function() {
      if (this.btnType === -1) {
        return 'background-color: red'
      }
      else if (this.btnType === 0) {
        return 'background-color: yellow'
      }
      else if (this.btnType === 1) {
        return 'background-color: green'
      }
      else {
        return ''
      }
    },
    btnText: function() {
      if (this.btnType === -1) {
        return ':('
      }
      else if (this.btnType === 0) {
        return ':|'
      }
      else if (this.btnType === 1) {
        return ':)'
      }
      else {
        return ''
      }
    }
  },
  methods: {
    click: () => {
      // eslint-disable-next-line
      console.log(`Clicked ${this.btnType}`)
    }
  },
}
</script>

<style scoped>

#button {
  font-size: 18pt;
  padding: 15px 32px;
}

</style>