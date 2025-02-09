<template>
  <div class="mt-2">
    <component :is="currentView" :taskID="taskID" :xp="taskResponse.score" :redo="redoBool" :err="errorMsg"
               @completeClicked="onSubmit" @redoQuiz="redoQuiz" @resubmit="doUpdate" @reset="resetUpdate">
    </component>
  </div>
</template>

<script>
import TextHolder from "@/components/TextHolder";
import QuizHandler from "@/components/QuizHandler";
import FeedbackHandler from "@/components/FeedbackHandler";
import PollHandler from "@/components/PollHandler";
import PickOneHolder from "@/components/PickOneHolder";
import TimerHolder from "@/components/TimerHolder";
import CongratsSplash from "@/components/CongratsSplash";
import NetworkError from "@/components/NetworkError";
import axios from 'axios';
import {mapState} from 'vuex';
import {mapGetters} from 'vuex';

export default {
  name: "TheTaskHandler",
  data: () => ({
    currentView: null,
    taskID: '',
    taskDetails: [],
    taskResponse: {
      score: 0,
      partial: [],
      feedback: []
    },
    levelUp: 0,
    redoBool: false,
    errorMsg: '',
    fbID: -1
  }),

  created() {
    this.taskID = this.getTask
    this.taskDetails = require(`@/content/${this.userDetails.company_id}taskwidgetJSON.json`).task.find(el =>
          el.id === this.taskID)
    this.currentView = this.componentFile
  },

  destroyed() {
    this.$store.dispatch('clearWorkingID')
  },

  components: {
    'text-holder': TextHolder,
    'quiz-handler': QuizHandler,
    'poll-handler': PollHandler,
    'pick-holder': PickOneHolder,
    'timer-holder': TimerHolder,
    'feedback-handler': FeedbackHandler,
    'congrats-splash': CongratsSplash,
    'error': NetworkError
  },

  computed: {

    ...mapState(['userDetails', 'companyDetails', 'taskList']),

    ...mapGetters(['getTaskIndex', 'getTask']),

    getRoot() {
      return process.env.VUE_APP_API_ROOT
    },

    componentFile() {
        let resp = ''
        switch (this.taskDetails.type) {
        case 'quiz':
          resp = 'quiz-handler'
          break
        case 'feedback':
          resp = 'feedback-handler'
          break
        case 'poll':
          resp = 'poll-handler'
          break
        case 'pick':
          resp = 'pick-holder'
          break
        case 'timer':
          resp = 'timer-holder'
          break
        default:
          resp = 'text-holder'
      }
      return resp
    },

    getFbPayload() {
      const dataObj = {
        'task_id': this.taskID,
        'company_id': this.companyDetails.company_id
      }
      this.taskResponse.feedback.forEach(function(value, i) {
        dataObj[`answer${i}`] = value
      })
      return dataObj
    },

  },

  methods: {

    onSubmit(response) {
      this.taskResponse = response
      this.levelUp = 0
      if (!this.taskResponse.partial.includes('n')) {
        this.taskResponse.partial = []
        this.redoBool = false
       } else {
        this.redoBool = true
     }

     const newXP = this.userDetails.user_xp + this.taskResponse.score
     if (newXP >= 50) {
       this.levelUp = 1
       this.$store.commit('toggleFlag')
     }

     this.doUpdate()
    },

    async doUpdate() {

      const token = await this.$auth.getTokenSilently()
      const config = {headers: {Authorization: `Bearer ${token}`}}

      let taskURL = `${this.getRoot}user_tasks/`

      axios.get(taskURL, config).then(response => {
            let ind = response.data.tasks.findIndex(el => el.task_id === this.taskID)

            const taskPayload = {
              user_sub: this.userDetails.user_sub, task_id: this.taskID, completed: !this.redoBool, partial: this.taskResponse.partial.join(',')
            }
            const userPayload = {user_xp: this.taskResponse.score, user_level: this.levelUp}
            const compPayload = {company_xp: this.taskResponse.score}

            let taskURL = ind === -1 ? `${this.getRoot}tasks/` : `${this.getRoot}tasks/${response.data.tasks[ind].id}/`
            let feedbackURL = `${this.getRoot}feedback/`
            let userURL = `${this.getRoot}users/`
            let compURL = `${this.getRoot}companies/${this.companyDetails.company_id}/`

            const taskPromise = ind === -1 ? axios.post(taskURL, taskPayload, config) :  axios.patch(taskURL, taskPayload, config)
            const fbPromise = this.taskResponse.feedback.length !== 0 ?
                axios.post(feedbackURL, this.getFbPayload, config).then((response) => {
                    this.fbID = response.data.id
                    this.taskResponse.feedback = [] }) : ""
            const userPromise = axios.patch(userURL, userPayload, config)
            const compPromise = axios.patch(compURL, compPayload, config)

            Promise.all([taskPromise, fbPromise, userPromise, compPromise]).then(responses => {
              if (this.getTaskIndex === -1) {
                this.$store.commit('appendTask', responses[0].data)
              } else {
                this.$store.commit('updateTask', {index: this.getTaskIndex, data: responses[0].data})
              }
              this.$store.commit('setUser', responses[2].data)
              this.$store.commit('setCompany', responses[3].data)
              this.currentView = 'congrats-splash'
            }).catch(err => {
              this.onUpdateError(err)
              })

          }).catch(err => {
            this.onUpdateError(err)
        })
    },

    onUpdateError(err) {
      this.errorMsg = err
      this.currentView = 'error'
    },

    async resetUpdate() {

      const token = await this.$auth.getTokenSilently()
      const config = {headers: {Authorization: `Bearer ${token}`}}

      let taskURL = `${this.getRoot}user_tasks/`
      let allTasksURL = `${this.getRoot}tasks/`
      let userURL = `${this.getRoot}users/`
      let compURL = `${this.getRoot}companies/${this.companyDetails.company_id}/`
      let feedbackURL = `${this.getRoot}feedback/${this.fbID}/`

      axios.get(taskURL, config).then(response => {
        let t = response.data.tasks.find(el => el.task_id === this.taskID)
        if (typeof t !== 'undefined') {
          if (this.getTaskIndex !== -1) {
            axios.patch(allTasksURL, this.taskList.tasks[this.getTaskIndex], config).catch(err => {
              console.log(err)
            })
          } else {
            axios.delete(allTasksURL, config).catch(err => {console.log(err)})
          }
        }
      }).catch(err => {console.log(err)})

      axios.patch(userURL, {user_xp: -this.taskResponse.score, user_level: -this.levelUp}, config).catch(err => {
        console.log(err)})
      axios.patch(compURL, {company_xp: -this.taskResponse.score}, config).catch(err => {console.log(err)})
      axios.delete(feedbackURL, config).catch(err => {console.log(err)})

      if (this.$store.state.levelUpFlag) {
        this.$store.commit('toggleFlag')
      }

      await this.$router.push('home')
    },

    redoQuiz() {
      this.taskResponse = {}
      this.currentView = 'quiz-handler'
    }

  }

}
</script>

<style scoped>

</style>