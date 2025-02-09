<template>
  <div>
    <div v-if="question <= pollContent.question.length">
      <component :is="'question-panel'" :content="pollContent" :question="question" @addAnswer="addAnswer"></component>
      <b-button  @click="nextQuestion" variant="primary" class="mt-2">Next</b-button><br />
    </div>
    <div v-if="question > pollContent.question.length">
      <div v-if="!isComplete">
        Thank you for your feedback! Click 'Submit' to complete.<br />
        <b-button @click="onSubmit" variant="success" class="mt-2">Submit</b-button>
      </div>
      <div v-if="isComplete">
        You have already submitted your feedback.
      </div>
    </div>
    <b-button @click="$router.push('home')" class="mt-2">Cancel</b-button>
  </div>
</template>

<script>
import feedbackJSON from '@/content/feedbackJSON.json';
import QuestionPanel from '@/components/QuestionPanel';
import {mapState} from "vuex";

export default {
  name: "FeedbackHandler",
  data:() => ({
    pollContent: [],
    answerInd: [],
    question: 1,
    taskIndex: -1
  }),
  components: {
    'question-panel': QuestionPanel
  },

  props: [
    'taskID'
  ],

  created() {
    this.pollContent = feedbackJSON.poll.find(el => el.id === this.taskID)
    this.taskIndex = this.$store.getters.getTaskIndex
    for (const q in this.pollContent.question) { // eslint-disable-line no-unused-vars
        this.answerInd.push(-1)}
  },

  computed: {
    ...mapState(['taskList']),

    isComplete() {
      return (this.taskIndex !== -1)
    }
  },

  methods: {

    nextQuestion() {
      this.question += 1
    },

    addAnswer(i) {
      let j = this.question - 2
      this.$set(this.answerInd, j, i)
    },

    onSubmit() {
      const response = { score: 5, partial: [], feedback: this.answerInd}
      this.$emit('completeClicked', response)
    }

  }

}
</script>

<style scoped>

  .btn:focus,.btn:active {
     outline: none !important;
     box-shadow: none;
  }

</style>