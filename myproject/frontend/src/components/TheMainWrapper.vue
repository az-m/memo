<template>
<div class="default-cursor">
  <b-navbar fixed="true" sticky type="dark" variant="info">
    <b-navbar-brand v-if="$auth.isAuthenticated">Week {{ $store.state.thisWeek }}</b-navbar-brand>
    <b-navbar-nav v-if="$auth.isAuthenticated">
      <b-nav-item v-if="$route.path !== '/home'" to="home">Home</b-nav-item>
    </b-navbar-nav>
    <b-navbar-nav class="ml-auto">
    <b-nav-dropdown right>
      <template #button-content>
        <em>{{ navBarUser }}</em>
      </template>
      <b-dropdown-item to="profile">Profile</b-dropdown-item>
      <b-dropdown-item v-if="!$auth.isAuthenticated" @click="doLogin">Sign In</b-dropdown-item>
      <b-dropdown-item v-if="$auth.isAuthenticated" @click="doLogout">Sign Out</b-dropdown-item>
    </b-nav-dropdown>
    </b-navbar-nav>
  </b-navbar>
  <b-container class="mt-3" v-if="!$auth.isAuthenticated" align="center">
    <h2>Please log in</h2>
  </b-container>
  <b-container v-if="$auth.isAuthenticated">
    <div>
    <keep-alive>
      <router-view v-if="$route.meta.KeepAlive"></router-view>
    </keep-alive>
    <router-view v-if="!$route.meta.KeepAlive"></router-view>
    </div>
    <div v-if="$store.userDetails === undefined">
      <component :is="currentView" @loggedIn="showFrontView" @newUser="showUserAdd" @userAdded="showLoginAction"></component>
    </div>
  </b-container>
</div>
</template>

<script>
import LoginAction from "@/components/LoginAction";
import NewUserAdd from "@/components/NewUserAdd";
import {mapState} from "vuex";

export default {
  name: "TheMainWrapper",
  components: {
    LoginAction,
    NewUserAdd
  },

  data: () => ({
    currentView: 'LoginAction',
    navBarUser: 'User',
    url: process.env.VUE_APP_API_ROOT
  }),

  computed: {
    ...mapState(['userDetails']),
  },

  created() {
    if (this.$route.path !== '/') {
      this.$router.push('/')
    }
  },

  methods: {

    showFrontView() {
      this.navBarUser = this.userDetails.user_name
      this.currentView = ''
    },

    showUserAdd() {
      this.currentView = 'NewUserAdd'
    },

    showLoginAction() {
      this.currentView = 'LoginAction'
    },

    doLogin() {
      this.$auth.loginWithRedirect()
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

.default-cursor {
  cursor: default;
  }

</style>