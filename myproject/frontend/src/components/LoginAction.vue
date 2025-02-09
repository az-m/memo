<template>
  <b-container fluid="true">
      <b-row>
        <b-col sm="6" md="4" offset-sm="3" offset-md="4" class="mt-5">
          <div class="text-center">
            <div v-if="hideSpinner === false">
              <b-spinner variant="primary" label="Spinning"></b-spinner>
            </div>
            <div v-if="errorMessage !== ''">
              <p>{{ errorMessage }}</p><br />
            </div>
          </div>
        </b-col>
      </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import {mapState} from "vuex";

export default {
  name: "LoginAction",

  data:() => ({
    hideSpinner: false,
    errorMessage: ''
  }),

  computed: {
    ...mapState(['userDetails']),
    getRoot() {
      return process.env.VUE_APP_API_ROOT
    }
  },

  created() {
    this.getApi()
  },

  methods: {

    async getApi() {
      while (this.$auth.loading) {
        await this.waitfor(100)
      }

      let userURL = `${this.getRoot}users/`
      let taskURL = `${this.getRoot}user_tasks/`

      const token = await this.$auth.getTokenSilently()
      const config = {headers: {Authorization: `Bearer ${token}`}}

      axios.get(userURL, config).then(response => {
            this.$store.commit('setUser', response.data)
            axios.get(`${this.getRoot}companies/${this.userDetails.company_id}/`, config).then(response => {
                this.$store.commit('setCompany', response.data)
                axios.get(taskURL, config).then(response => {
                    this.$store.commit('setTasks', response.data)
                    this.$store.commit('setWeek')
                    this.$emit('loggedIn')
                      if (this.$route.path !== '/home') {
                        this.$router.push('home')
                      }
                }).catch(err => {
                  this.errorMessage = 'Get user task list - ' + err.message
                  this.hideSpinner = true
                })
            }).catch(err => {
              this.errorMessage = 'Get company details - ' + err.message
              this.hideSpinner = true
            })
          }).catch(err => {
            if (err.response.status === 404) {
              this.$emit('newUser')
            } else {
        this.errorMessage = 'Get user details - ' + err.response.status }
        this.hideSpinner = true
      })
    },

    waitfor(ms) {
      return new Promise(resolve => {
        setTimeout(()=> { resolve('') }, ms);
      })
    }

  }
}

</script>

<style scoped>

</style>