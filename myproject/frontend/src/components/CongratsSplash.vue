<template>
  <div>
    <b-container>
      <b-row>
        <b-col sm="8" md="6" offset-sm="2" offset-md="3" class="mt-5 text-center">
          <div v-if="xp > 0">
            <h2>Well done you!</h2>
            <h3>You earned {{ xp }} XP</h3>
          </div>
          <div v-if="xp === 0">
            <h3>You did not earn any XP this time</h3>
          </div>
          <div v-if="$store.state.levelUpFlag">
            <strong>You leveled up! You are now level {{ $store.state.userDetails.user_level }}</strong>
          </div>
          <h4 class="mt-4">Check your progress</h4>
          <b-button @click="$router.push('profile')" variant="success" class="mt-2">Profile</b-button>
          <div v-if="redo">
            <h4 class="mt-4">Try the quiz again</h4>
            <b-button @click="$emit('redoQuiz')" variant="primary" class="mt-2">Retake Quiz</b-button>
          </div>
          <div>
            <b-button @click="$router.push('home')" variant="primary" class="mt-4">Home</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "CongratsSplash",
  props: [
    'redo',
    'xp'
  ],
  destroyed() {
    if (this.$store.state.levelUpFlag) {
      this.$store.commit('toggleFlag')
    }
  }
}
</script>

<style scoped>

</style>