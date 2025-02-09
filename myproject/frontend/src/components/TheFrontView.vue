<template>
<div>
  <div>
    <ThisWeeksTasks :thisWeek="thisWeek" />
  </div>
  <b-container fluid="true" class="pb-5">
  <div v-for="c in channels" :key="c.short">
    <ArticlePanel :channel="c" :articles="selectArticles(c)" />
  </div>
  </b-container>
</div>
</template>

<script>
import ThisWeeksTasks from "@/components/ThisWeeksTasks";
import ArticlePanel from "@/components/ArticlePanel";
import {mapState} from "vuex";

export default {
  name: "TheFrontView",
  components: {
    ThisWeeksTasks,
    ArticlePanel
  },

  data: () => ({
    ARTICLE_JSON: null,
    channels: [
      {short: 'WW', title: 'Working well'},
      {short: 'TF', title: 'Thoughts and feelings'},
      {short: 'BH', title: 'Body health'},
      {short: 'RC', title: 'Relationships'},
      {short: 'JY', title: 'Joy'}
    ]
  }),

  created() {
    this.ARTICLE_JSON = require(`@/content/${this.userDetails.company_id}articlewidgetJSON.json`)
  },

  computed: {
    ...mapState(['userDetails']),

    thisWeek() {
      return this.ARTICLE_JSON.article.filter(el => Number(el.id.slice(2, 5)) === this.$store.getters.getWeek)
    },

    selectArticles() {
      let temp_list = this.ARTICLE_JSON.article.filter(el => Number(el.id.slice(2, 5)) !== this.$store.getters.getWeek)
      return (cat) => temp_list.filter(el => el.id.slice(0, 2) === cat.short)
    }
  }

}

</script>

<style scoped>

</style>