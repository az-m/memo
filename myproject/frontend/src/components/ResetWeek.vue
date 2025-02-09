<template>
<div>
  <b-container class="mt-4">
  <h3>Reset week</h3>
  <p>Returns you to Week 1 - does not reset your task progress.</p>
  <b-button variant="success" @click="resetWeek">Reset week</b-button>
  </b-container>
</div>
</template>

<script>
import {mapState} from "vuex";
import axios from 'axios';

export default {
name: "ResetWeek.vue",

  computed: {
    ...mapState(['userDetails']),
    getRoot() {
      return process.env.VUE_APP_API_ROOT
    }
  },

  methods: {
    async resetWeek() {

      const token = await this.$auth.getTokenSilently()
      const config = {headers: {Authorization: `Bearer ${token}`}}

      const todayDate = new Date().toJSON().slice(0,10)
      const payload = {start_date: todayDate}

      let userURL = `${this.getRoot}users/`

      axios.patch(userURL, payload, config).then((response) => {
          this.$store.commit('setUser', response.data)
          this.$store.commit('setWeek')
          this.$router.push('/home')
      }).catch(err => {
        this.onUpdateError(err)
      })

    }
  }
}

</script>

<style scoped>

</style>