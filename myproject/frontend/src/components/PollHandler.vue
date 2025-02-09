<template>
  <div class="default-cursor">
    <b-container v-if="showQuestions" class="pb-5">
      <h3>{{ pollContent.title }}</h3>
      <div v-html="pollContent.intro" class="mt-4"></div>
      <b-card v-for="(q, i) in pollContent.question" :key="i" :title="q.text" title-tag="h5" class="mb-2">
        <b-form-group>
          <b-form-radio v-for="(a, j) in q.answer" :key="j" :value="a.points" v-model="answerArr[i]">
            {{ a.text }}
          </b-form-radio>
        </b-form-group>
      </b-card>
      <b-button @click="onSubmit" variant="success" class="mt-2">Check your score</b-button>
    </b-container>
    <b-container v-if="!showQuestions">
      <b-row>
        <b-col sm="8" md="6" offset-sm="2" offset-md="3" class="mt-5 text-center">
          <div v-if="pollContent.showscore">
            <h4>You scored</h4>
            <h3>{{ score }}%</h3>
            <div v-html="message" class="mt-2"></div>
          </div>
          <div v-if="!pollContent.showscore" v-html="message" class="mt-2 text-left"></div>
          <div>
            <b-button v-if="!complete" @click="onContinue" variant="success" class="mt-2">Done</b-button><br />
            <b-button @click="$router.push('home')" class="mt-2">Cancel</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "PollHandler",
  data:() => ({
    pollContent: [],
    answerArr: [],
    score: 0,
    message: '',
    taskIndex: -1,
    complete: false,
    showQuestions: true
  }),

  props: [
    'taskID'
  ],

  created() {
    this.pollContent = require(`@/content/${this.userDetails.company_id}pollJSON.json`).poll.find(el =>
        el.id === this.taskID)
    this.taskIndex = this.$store.getters.getTaskIndex
    this.complete = this.isComplete
  },

  computed: {
    ...mapState(['userDetails', 'taskList']),

    isComplete() {
      return (this.taskIndex !== -1)
    },

    getMax() {
      let q = [], a = []
      this.pollContent.question.forEach(function (element) {
        a = element.answer.map(object => object.points)
        q.push(Math.max(...a))
      })
      return q.reduce((part, n) => part + n, 0)
    }
  },

  methods: {

    onSubmit() {
      const x = this.answerArr.reduce((part, n) => part + n, 0)
      this.score = Math.round(x / this.getMax * 100)
      this.pollContent.response.forEach((element) => {
        if (this.score >= element.threshold.lower && this.score < element.threshold.upper) {
         this.message = element.message }
        })
      this.showQuestions = false
    },

    onContinue() {
      const response = { score: 5, partial: [], feedback: []}
      this.$emit('completeClicked', response)
    }
  }
}

</script>

<style scoped>
  .default-cursor { cursor: default; }
</style>