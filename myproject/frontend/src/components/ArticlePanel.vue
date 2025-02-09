<template>
<div>
  <b-col v-if="shuffled.length !== 0" lg="8" offset-lg="1" class="pt-5">
    <b-button variant="primary" @click="allChannel(channel)">{{ channel.title }}</b-button>
    <b-row>
      <b-container v-for="a in num_items" :key="a" @click="onClick(shuffled[a-1].id)">
        <b-card no-body class="overflow-hidden mt-3" bg-variant="light" border-variant="dark">
              <b-row no-gutters align-v="center">
                <b-col sm="10">
                  <b-card-body :title="shuffled[a-1].title">
                    <b-card-text>
                      {{ shuffled[a-1].text }}
                    </b-card-text>
                  </b-card-body>
                </b-col>
                <b-col>
                  <b-icon v-if="$store.getters.getComplete(shuffled[a-1].id)" icon="check2-circle" variant="success" scale="3"></b-icon>
                  <b-icon v-if="$store.getters.getPartial(shuffled[a-1].id)" icon="check2-circle" variant="warning" scale="3"></b-icon>
                </b-col>
              </b-row>
            </b-card>
      </b-container>
    </b-row>
  </b-col>
  <b-col v-if="shuffled.length === 0" lg="8" offset-lg="1" class="pt-5">
    <b-button disabled>{{ channel.title }}</b-button>
      <b-card class="mt-3">
        There are no articles in {{ channel.title }}
      </b-card>
  </b-col>
</div>
</template>

<script>
export default {
  name: "ArticlePanel",
  data: () => ({
    num_items: 4,
    shuffled: []
  }),
  props: [
      'channel',
      'articles'
  ],

  created() {
    this.shuffleArray(this.articles)
    this.shuffled = this.articles
  },

  activated() {
    this.$forceUpdate()
  },

  methods: {
    shuffleArray(array) {
      // uses Durstenfeld shuffle
      for (let i = array.length - 1; i > 0; i-- ) {
        const j = Math.floor(Math.random() * ( i + 1));
        [array[i], array[j]] = [array[j], array[i]]
      }
    },

    allChannel(c) {
      this.$store.commit('setSelectedChannel', c)
      this.$router.push('channel')
    },

    onClick(i) {
      this.$store.dispatch('makeWorkingID', i)
      this.$router.push('article')
    }
  }

}
</script>

<style scoped>

</style>