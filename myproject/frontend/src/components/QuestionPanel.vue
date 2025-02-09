<template>
  <div class="default-cursor">
    <b-card :title="toDisplay.text">
      <b-list-group v-for="a in toDisplay.answer" :key="a.pos" @click="clicked(a.pos)">
        <b-list-group-item class="rounded-0" :class="{ active: a.pos === activeInd }">
          {{ a.text }}
        </b-list-group-item>
      </b-list-group>
    </b-card>
  </div>
</template>

<script>


export default {
  name: "QuestionPanel",
  data:() => ({
    toDisplay: [],
    activeInd: -1
  }),
  props: [
      'content',
      'question'
  ],

  created() {
    this.toDisplay = this.content.question.find(el => el.no === this.question)
  },

  watch: {
    question: function () {
      this.$emit('addAnswer', this.activeInd)
      this.toDisplay = this.content.question.find(el => el.no === this.question)
      this.activeInd = -1
    }
  },

  destroyed() {
    this.$emit('addAnswer', this.activeInd)
  },


  methods: {

    clicked(i) {
      this.activeInd = i
    }

  }
}
</script>

<style scoped>
 .default-cursor { cursor: default; }
</style>