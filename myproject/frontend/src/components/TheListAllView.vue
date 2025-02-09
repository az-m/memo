<template>
  <div>
    <b-container class="pb-5">
      <h1>{{ $store.state.selectedChannel.title }}</h1>
      <b-card no-body class="mt-4">
        <b-tabs card justified>
          <b-tab title="Articles" class="pt-4">
            <b-container fluid="true" v-for="a in ARTICLE_JSON" :key="a.id" @click="onClickArticle(a.id)">
              <b-card no-body class="overflow-hidden mb-3" bg-variant="light" border-variant="dark">
                <b-row no-gutters align-v="center">
                  <b-col sm="10">
                    <b-card-body :title="a.title">
                      <b-card-text>
                        {{a.text }}
                      </b-card-text>
                    </b-card-body>
                  </b-col>
                  <b-col>
                    <b-icon v-if="$store.getters.getComplete(a.id)" icon="check2-circle" variant="success" scale="3"></b-icon>
                    <b-icon v-if="$store.getters.getPartial(a.id)" icon="check2-circle" variant="warning" scale="3"></b-icon>
                  </b-col>
                </b-row>
              </b-card>
            </b-container>
          </b-tab>
          <b-tab title="Tasks" class="pt-4">
            <b-container fluid="true" v-for="t in TASKS_JSON" :key="t.id" @click="onClickTask(t.id)">
              <b-card no-body class="overflow-hidden mb-3" bg-variant="light" border-variant="dark">
                <b-row no-gutters align-v="center">
                  <b-col sm="10">
                    <b-card-body :title="t.title">
                      <b-card-text>
                        {{t.text }}
                      </b-card-text>
                    </b-card-body>
                  </b-col>
                  <b-col>
                    <b-icon v-if="$store.getters.getComplete(t.id)" icon="check2-circle" variant="success" scale="3"></b-icon>
                    <b-icon v-if="$store.getters.getPartial(t.id)" icon="check2-circle" variant="warning" scale="3"></b-icon>
                  </b-col>
                </b-row>
              </b-card>
            </b-container>
          </b-tab>
        </b-tabs>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "TheListAllView",

  data: () => ({
    ARTICLE_JSON: null,
    TASKS_JSON: null
  }),


  created() {
    let article_response = require(`@/content/${this.userDetails.company_id}articlewidgetJSON.json`)
    let task_response = require(`@/content/${this.userDetails.company_id}taskwidgetJSON.json`)
    this.ARTICLE_JSON = article_response.article.filter(el => el.id.slice(0, 2) === this.$store.state.selectedChannel.short)
    this.TASKS_JSON = task_response.task.filter(el => el.id.slice(0, 2) === this.$store.state.selectedChannel.short)
  },

  computed: {
    ...mapState(['userDetails'])
  },

  methods: {
    onClickArticle(i) {
      this.$store.dispatch('makeWorkingID', i)
      this.$router.push('article')
    },
    onClickTask(i) {
      this.$store.dispatch('makeWorkingID', i)
      this.$router.push('task')
    },
  }
}
</script>

<style scoped>

</style>