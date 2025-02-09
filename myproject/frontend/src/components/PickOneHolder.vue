<template>
  <div class="default-cursor">
  <b-container>
      <h3>{{ pollContent.heading }}</h3>
      <div v-html="pollContent.intro" class="mt-4"></div>
      <b-container class="mt-4 pb-4">
        <b-list-group>
          <b-list-group-item v-for="(o, i) in pollContent.options" :key="i" @click="clicked(i)"
                             class="rounded-0" :class="{ active: i === activeInd }">
            {{ o.text }}
          </b-list-group-item>
        </b-list-group>
        <p class="font-weight-bold">{{ pollContent.CTA }}</p>
      </b-container>
      <div>
        <b-button v-if="!complete" @click="onSubmit" variant="success" class="mt-3">Done</b-button><br />
        <b-button @click="$router.push('home')" class="mt-2">Cancel</b-button>
      </div>
    </b-container>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "PickOneHolder",
  data:() => ({
    pollContent: [],
    taskIndex: -1,
    activeInd: -1,
    complete: false
  }),

  props: [
    'taskID'
  ],

  created() {
    this.pollContent = require(`@/content/${this.userDetails.company_id}pickoneJSON.json`).task.find(el =>
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
    clicked(i) {
      this.activeInd = i
    },

    onSubmit() {
      const response = { score: 5, partial: [], feedback: []}
      this.$emit('completeClicked', response)
    }
  }

}
</script>

<style scoped>
.default-cursor { cursor: default; }
</style>