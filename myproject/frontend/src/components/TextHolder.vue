<template>
  <div>
    <b-container>
      <h3>{{ taskContent.heading }}</h3>
      <div v-html="taskContent.content" class="mt-4"></div>
      <div>
      <b-button v-if="!complete" @click="onSubmit" variant="success" class="mt-2">Done</b-button><br />
      <b-button @click="$router.go(-1)" class="mt-2">Back</b-button>
      </div>
    </b-container>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "TextHolder",
  data:() => ({
    taskContent: null,
    taskIndex: -1,
    complete: false
  }),

  props: [
    'taskID'
  ],

  created() {
    this.taskContent = require(`@/content/${this.userDetails.company_id}textJSON.json`).task.find(el =>
        el.id === this.taskID)
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
    onSubmit() {
      const response = { score: 5, partial: [], feedback: []}
      this.$emit('completeClicked', response)
    }
  }

}
</script>

<style scoped>

</style>