<template>
<div>
  <b-container class="mt-3">
    <form method="post" @submit.prevent="checkInput">
      <p>Please enter a screen name and your company ID and click submit</p>
      <b-form-input class="mt-2" placeholder="Name" type="text" v-model="userName"/>
      <p><span class="errormsg">{{ userMessage }}</span></p>
      <b-form-input class="mt-2" placeholder="Company" type="text" v-model="companyID"/>
      <p><span class="errormsg">{{ compMessage }}</span></p>
      <b-button class="mt-3" type="submit" variant="primary">Submit</b-button>
    </form>
  </b-container>
</div>
</template>

<script>
import companyJSON from "@/content/companyJSON.json";
import axios from 'axios';

export default {
  name: "NewUserAdd",
  data: () => ({
    userName: "",
    companyID: null,
    userMessage: "",
    compMessage: ""
  }),

  computed: {
     getRoot() {
      return process.env.VUE_APP_API_ROOT
    }
  },

  watch: {

    userName: function (val) {
        if(val.length>30) {
          this.userMessage = "Screen name 30 characters max"
        } else {
          this.userMessage = ""
        }
    },

    companyID: function (oldval, newval) { // eslint-disable-line no-unused-vars
      this.compMessage = ""
    }

  },

  methods: {

    checkInput() {
      let formErrors = 0
      if(this.userName.length > 30) {
        formErrors = 1
      }
      if(!companyJSON.company.find(el => el.id === parseInt(this.companyID))) {
        formErrors = 1
        this.compMessage = "Company does not exist"
      }
      if(!formErrors) {
      this.createUser() }
    },


    async createUser() {
      const todayDate = new Date().toJSON().slice(0,10)
      const userPayload = { user_sub: this.$auth.user.sub, user_name: this.userName, company_id: this.companyID,
      start_date: todayDate, user_xp: 0, user_level: 1}

      const token = await this.$auth.getTokenSilently()
      const config = {headers: {Authorization: `Bearer ${token}`}}
      let userUrl = `${this.getRoot}create_user/`

      axios.post(userUrl, userPayload, config).then(() => { //
          this.$emit('userAdded')}).catch(err => {
              this.onUpdateError(err)
              })
    }
  }

}
</script>

<style scoped>

.errormsg {
  color: red;
}


</style>