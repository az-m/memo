<template>
<div>
  <b-container class="mt-4">
  <h3>Delete user profile</h3>
  <p>Deletes user profile and task progress. Removes contributed XP from company record.</p>
  <b-button variant="danger" @click="confirmDelete">Delete user</b-button>
  </b-container>
</div>
</template>

<script>
import {mapState} from "vuex";
import axios from 'axios';

export default {
  name: "DeleteUser",

  computed: {
    ...mapState(['userDetails', 'companyDetails']),
    getRoot() {
      return process.env.VUE_APP_API_ROOT
    }
  },

  methods: {

    confirmDelete() {
        this.$bvModal.msgBoxConfirm('Please confirm that you want to delete everything.', {
          title: 'Please Confirm',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: 'YES',
          cancelTitle: 'NO',
          footerClass: 'p-2',
          hideHeaderClose: false,
          centered: true
        })
          .then(value => {
            if (value) {
              this.deleteUser()
            }
          })
          .catch(err => {
            console.log(err)
          })
    },

    async deleteUser() {
      const earnedXP = (this.userDetails.user_level - 1)*50 + this.userDetails.user_xp

      const token = await this.$auth.getTokenSilently()
      const config = {headers: {Authorization: `Bearer ${token}`}}

      let userURL = `${this.getRoot}users/`
      let compURL = `${this.getRoot}companies/${this.companyDetails.company_id}/`

      axios.delete(userURL, config).catch(err => {console.log(err)})
      axios.patch(compURL, {company_xp: -earnedXP }, config).catch(err => {console.log(err)})

      this.doLogout()

    },

     doLogout() {
      this.$auth.logout({
        returnTo: window.location.origin
      });
    }
  }

}
</script>

<style scoped>

</style>