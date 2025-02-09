<template>
<div>
  <b-container fluid="true" class="mt-5">
    <b-card :header="`${userDetails.user_name}`" header-class="user_header" class="mb-3">
      <b-card-body>
        <h3>XP - {{ userDetails.user_xp }}</h3>
        <b-progress :value="getPercent" variant="success" :striped="striped" class="mb-2"></b-progress>
        <h3>Level - {{ userDetails.user_level }}</h3>
        <b-progress :value="userDetails.user_level" :max="max"></b-progress>
      </b-card-body>
    </b-card>
    <b-card no-body class="overflow-hidden mb-3">
      <b-row no-gutters>
        <b-col>
          <b-img fluid :src="require(`@/assets/logos/${companyDetails.company_id}.png`)" class="rounded-0"></b-img>
        </b-col>
        <b-col md="9">
          <b-card-body :title="companyContent.title" title-tag="h1" :sub-title="companyContent.subtitle"
                         sub-title-tag="h2">
            <b-progress :value="companyDetails.company_xp" :max="companymax" variant="success" class="mt-3"></b-progress>
            <h3>XP - {{ companyDetails.company_xp }}</h3>
          </b-card-body>
        </b-col>
      </b-row>
    </b-card>
    <b-card-group deck class="mt-3">
    <b-card class="mb-3" :img-src="require(`@/assets/logos/${companyDetails.charity}.png`)" :title="charityContent.name" style="max-width: 20rem;">
      <b-card-text>
        {{ charityContent.text }}
      </b-card-text>
      <b-button :href="charityContent.url" target="_blank" variant="primary">Find out more</b-button>
    </b-card>
      <b-card class="mb-3">
        <h2>Testing Functions</h2>
        <ResetWeek />
        <DeleteUser />
      </b-card>
    </b-card-group>
  </b-container>
</div>
</template>

<script>
import {mapState} from "vuex";
import companyJSON from "@/content/companyJSON.json";
import charityJSON from "@/content/charityJSON.json";
import ResetWeek from "@/components/ResetWeek";
import DeleteUser from "@/components/DeleteUser";

export default {
  name: "TheProfileView",
  components: {
    ResetWeek,
    DeleteUser
  },
  data: () => ({
    companyContent: null,
    charityContent: null,
    striped: true,
    max: 10,
    companymax: 1000
  }),

  created() {
    this.companyContent = companyJSON.company.find(el => el.id === this.userDetails.company_id)
    this.charityContent = charityJSON.charity.find(el => el.id === this.companyDetails.charity)
  },

  computed: {
    ...mapState(['userDetails', 'companyDetails']),
    getPercent: function () {
      return this.userDetails.user_xp / 50 * 100
    }
  }
}
</script>

<style scoped>

  .user_header {
    font-size: 2em;
    font-weight: 400
  }

</style>