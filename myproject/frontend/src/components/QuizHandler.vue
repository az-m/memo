<template>
  <div class="default-cursor">
    <b-container v-if="!showAnswers" class="pb-5">
      <b-card v-for="(q, i) in quizContent.question" :key="i" :title="q.text" class="mb-2">
        <b-list-group>
          <b-list-group-item v-for="(a, j) in q.answer" :key="j" @click="clicked(i, j)"
                             class="rounded-0" :class="{ active: j === activeInd[i] }">
            {{ a.text }}
          </b-list-group-item>
        </b-list-group>
      </b-card>
      <div>
        <b-button @click="onSubmit" variant="success" class="mt-2">Submit</b-button><br />
        <b-button @click="$router.push('home')" class="mt-2">Cancel</b-button>
      </div>
    </b-container>
    <b-container v-if="showAnswers" class="pb-5">
      <div class="text-center"><h3 class="mb-3">You got {{ numCorrect }} out of {{ activeInd.length }} correct</h3></div>
      <b-card v-for="(q, i) in quizContent.question" :key="i" :title="q.text" class="mb-2">
        <b-list-group>
          <b-list-group-item v-for="(a, j) in q.answer" :key="j" class="rounded-0"
                             :class="{ 'bg-success text-white': isCorrect(i, j), 'bg-danger text-white': !isCorrect(i, j) && (j === activeInd[i]) }">
            {{ a.text }}
          </b-list-group-item>
        </b-list-group>
      </b-card>
      <div>
        <b-button v-if="!complete" @click="onContinue" variant="success" class="mt-2">Continue</b-button><br />
        <b-button @click="backToQuiz" class="mt-2">Cancel</b-button>
      </div>
    </b-container>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "QuizHandler",
  data:() => ({
    quizContent: [],
    showAnswers: false,
    activeInd: [],
    partial: [],
    taskIndex: -1,
    score: 0,
    numCorrect: 0,
    complete: false
  }),

  props: [
    'taskID'
  ],

  created() {
    this.quizContent = require(`@/content/${this.userDetails.company_id}quizJSON`).quiz.find(el =>
        el.id === this.taskID)
    this.taskIndex = this.$store.getters.getTaskIndex
    this.complete = this.isComplete
    this.initResponseArrays()
    this.loadPartialArray()
  },

  computed: {
    ...mapState(['userDetails', 'taskList']),

    isPartial() {
      return (this.taskIndex !== -1 && this.taskList.tasks[this.taskIndex].partial.includes('n'))
    },

    isComplete() {
      return (this.taskIndex !== -1 && !this.taskList.tasks[this.taskIndex].partial.includes('n'))
    }

  },

  methods: {

    onSubmit() {
      if (!this.activeInd.includes(-1)) {
        this.activeInd.forEach((value, index) => {
          if (this.isCorrect(index, value)) {
            this.numCorrect += 1
          }
        })
      }
        this.showAnswers = true
    },

    addScore(i) {
      if (this.partial[i] !== "y") {
        this.score += 1
        this.partial[i] = "y"
      }
    },

    clicked(q, a) {
      this.$set(this.activeInd, q, a)
    },

    isCorrect(q, a) {
      return this.quizContent.question[q].answer[a].correct
    },

    initResponseArrays() {
      for (const q in this.quizContent.question) { // eslint-disable-line no-unused-vars
        this.activeInd.push(-1)
        this.partial.push("n")
      }
    },

    loadPartialArray() {
      if (this.isPartial) {
        this.partial = this.taskList.tasks[this.taskIndex].partial.split(",")
      }
    },

    onContinue() {
      if (!this.activeInd.includes(-1)) {
        this.activeInd.forEach((value, index) => {
          if (this.isCorrect(index, value)) {
            this.addScore(index)
          }
        })
      }
      const response = { score: this.score, partial: this.partial, feedback: [] }
      this.$emit('completeClicked', response)
    },

    backToQuiz() {
      this.activeInd.forEach((value, index) => {
        this.$set(this.activeInd, index, -1)
      })
      this.numCorrect = 0
      this.showAnswers = false
    }

  }


}
</script>

<style scoped>

.default-cursor { cursor: default; }

</style>