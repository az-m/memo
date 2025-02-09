<template>
  <div>
    <b-container>
      <h3>{{ taskContent.title }}</h3>
      <div v-html="taskContent.intro" class="mt-4"></div>
      <div v-html="taskContent.CTA" class="font-weight-bold"></div>
      <b-container class="align-middle"
                   :class="{ 'timer-text-number': seconds !== 'Stop!', 'timer-text-done': seconds === 'Stop!'}">
        {{ seconds }}
      </b-container>
      <div class="text-center">
        <div v-if="!started">
          <b-button @click="start_count" variant="success">Start</b-button>
        </div>
        <div v-if="started && seconds !== 'Stop!'">
          <b-button @click="pause_resume">{{ buttonText }}</b-button>
          <b-button v-if="buttonText === 'Resume'" @click="reset" class="ml-2">Reset</b-button>
        </div>
        <div v-if="seconds === 'Stop!'">
          <b-button @click="restart" variant="success">Restart</b-button>
        </div>
      </div>
      <div>
      <b-button v-if="!complete && seconds === 'Stop!'" @click="onSubmit" variant="success" class="mt-2">Continue</b-button><br />
      <b-button @click="$router.push('home')" class="mt-2">Cancel</b-button>
      </div>
    </b-container>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "TimerHolder.vue",
  data:() => ({
    taskContent: null,
    duration: 0,
    seconds: 0,
    started: false,
    paused: false,
    buttonText: 'Pause',
    taskIndex: -1,
    complete: false
  }),

  props: [
    'taskID'
  ],

  created() {
    this.taskContent = require(`@/content/${this.userDetails.company_id}timerJSON.json`).task.find(el =>
        el.id === this.taskID)
    this.duration = this.taskContent.duration
    this.seconds = this.taskContent.duration
    this.taskIndex = this.$store.getters.getTaskIndex
    this.complete = this.isComplete
  },

  computed: {
    ...mapState(['userDetails', 'taskList']),

    isComplete() {
      return (this.taskIndex !== -1)
    }

  },

  methods: {

    start_count() {
      this.started = true
      this.countdown()
    },

    async countdown() {
      for (let i = this.duration; i > -1; i--) {
        if (!this.paused) {
          if (i > 0) {
            this.seconds = i
          } else {
            this.seconds = "Stop!"
          }
          await this.waitfor(1000)
        }
      }
    },

    waitfor(ms) {
      return new Promise(resolve => {
        setTimeout(()=> { resolve('') }, ms);
      })
    },

    onSubmit() {
      const response = { score: 5, partial: [], feedback: []}
      this.$emit('completeClicked', response)
    },

    pause_resume() {
      this.paused = !this.paused
      if (this.buttonText === 'Resume') {
        this.duration = this.seconds
        this.countdown()
      }
      this.buttonText = this.buttonText === 'Pause' ? 'Resume' : 'Pause'
    },

    reset() {
      this.started = false
      this.paused = false
      this.buttonText = 'Pause'
      this.duration = this.taskContent.duration
      this.seconds = this.taskContent.duration
    },

    restart() {
      this.paused = false
      this.buttonText = 'Pause'
      this.duration = this.taskContent.duration
      this.seconds = this.taskContent.duration
      this.start_count()
    }

  }
}
</script>

<style scoped>

  .timer-text-number {
    font-size: 10em;
    text-align: center;
    min-height: 240px;
  }

   .timer-text-done {
    font-size: 5em;
    text-align: center;
    min-height: 240px;
  }

</style>