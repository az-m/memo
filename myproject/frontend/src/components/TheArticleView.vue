<template>
<div>
  <b-container class="pb-5">
    <div class="mb-4">
      <b-img v-if="imgURL" :src="imgURL" fluid center></b-img>
    </div>
    <h3>{{ ARTICLE_JSON.heading }}</h3>
    <div v-html="ARTICLE_JSON.content" class="mt-4"></div>
    <p class="font-weight-bold">{{ ARTICLE_JSON.CTA }}</p>
    <div v-if="!isComplete" class="mt-3">
      <h4>Do the task</h4>
      <b-button @click="$router.push('task')" variant="primary" class="mt-2">Task</b-button>
    </div>
    <b-button @click="$router.go(-1)" class="mt-4">Back</b-button>
  </b-container>
</div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "TheArticleView",
  data: () => ({
    taskID: '',
    ARTICLE_JSON: null,
  }),


  created() {
    this.taskID = this.$store.getters.getTask
    this.ARTICLE_JSON = require(`@/content/${this.userDetails.company_id}articleJSON.json`).article.find(el =>
        el.id === this.$store.state.workingID.article)
  },

  mounted() {
    if (this.$store.getters.getTask === '') {
      this.$store.dispatch('makeWorkingID', this.taskID)
    }
  },

  computed: {
    ...mapState(['userDetails', 'taskList']),

    isComplete() {
      let i = this.$store.getters.getTaskIndex
      return (i !== -1 && this.taskList.tasks[i].completed)
    },

    imgURL() {
      if (this.ARTICLE_JSON.image !== "") {
        return require(`@/content/heroimages/${this.ARTICLE_JSON.image}.jpg`) }
      else {
        return null
      }
    }
  }
}
</script>

<style scoped>

</style>