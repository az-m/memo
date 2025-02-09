<template>
  <div>
    <b-container v-if="thisWeek.length !== 0">
     <b-card-group deck class="mt-4">
       <b-card :title="a.title" title-tag="h6" v-for="a in thisWeek" :key="a.id" @click="onClick(a.id)"
               :class="{ 'border-success': !$store.getters.getComplete(a.id)}">
         <b-card-text>{{ a.text }}</b-card-text>
       </b-card>
     </b-card-group>
    </b-container>
    <b-container v-if="thisWeek.length === 0">
      <b-card>
        There are no tasks allocated for week {{ $store.state.thisWeek }}
      </b-card>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "ThisWeeksTasks",
  props: [
    'thisWeek'
  ],

  methods: {
    onClick(i) {
      this.$store.dispatch('makeWorkingID', i)
      this.$router.push('article')
    }
  }

}
</script>

<style scoped>

</style>
