<template>
<div>
  <p>There was a network error</p>
  <p>{{ err }}</p>
  <div>
    <b-button @click="retry" variant="success" class="mt-2">Retry</b-button><br />
    <b-button @click="$emit('reset')" variant="primary" class="mt-2 mb-2">Reset task</b-button>
  </div>
  <div v-if="hideSpinner === false">
    <b-spinner variant="primary" label="Spinning"></b-spinner>
  </div>
</div>
</template>

<script>
export default {
  name: "NetworkError",
  data:() => ({
    hideSpinner: true
  }),
  props: [
    'err'
  ],
  methods: {
    retry() {
      this.showSpinner()
      this.$emit('resubmit')
    },

    showSpinner() {
      this.hideSpinner = false
      setTimeout(()=> { this.hideSpinner = true}, 1000)
    },

  }
}

</script>

<style scoped>
.btn:focus,.btn:active {
     outline: none !important;
     box-shadow: none;
  }
</style>