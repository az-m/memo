import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {

    workingID: { article: '', task: '' },
    selectedChannel: '',

    userDetails: [],
    companyDetails: [],
    taskList: [],
    thisWeek: null,
    levelUpFlag: false
  },

  getters: {
    getWeek: (state) => {
      return state.thisWeek + 100
    },
    getTask: (state) => {
      return state.workingID.task
    },
    getTaskIndex: (state) => {
      return state.taskList.tasks.findIndex(el => el.task_id === state.workingID.task)
    },
    getComplete: (state) => (id) => {
      id = id.slice(0, -1) + 'T'
      let i = state.taskList.tasks.findIndex(el => el.task_id === id)
      let b = false
      if (i !== -1) {
        b = state.taskList.tasks[i].completed
      }
      return b
    },
    getPartial: (state) => (id) => {
      id = id.slice(0, -1) + 'T'
      let i = state.taskList.tasks.findIndex(el => el.task_id === id)
      let b = false
      if (i !== -1) {
        b = state.taskList.tasks[i].partial.includes('n')
      }
      return b
    }
  },

  mutations: {

    logOut(state) {
      state.userDetails = []
      state.companyDetails = []
      state.taskList = []
    },

    setUser (state, p) { state.userDetails = p },
    setCompany (state, p) { state.companyDetails = p },
    setTasks (state, p) { state.taskList = p },

    setWeek (state) {
      const date1 = new Date(state.userDetails.start_date)
      const date2 = Date.now()
      const oneweek = 1000 * 60 * 60 * 24 * 7

      const diff = date2 - date1.getTime()
      state.thisWeek =  Math.ceil(diff/oneweek)
    },

    setWorkingID (state, p) { state.workingID = p },
    setSelectedChannel (state, p) { state.selectedChannel = p },

    updateTask (state, p) { state.taskList.tasks[p.index] = p.data },
    appendTask (state, p) { state.taskList.tasks.push(p)},
    deleteTask (state, p) { state.taskList.tasks.splice(p.index,1)},

    toggleFlag (state) { state.levelUpFlag = !state.levelUpFlag },

  },

  actions: {

    makeWorkingID (context, p) {
      let a = p.slice(0, -1) + 'A'
      let t = p.slice(0, -1) + 'T'
      context.commit('setWorkingID', { article: a, task: t })
    },

    clearWorkingID (context) {
      context.commit('setWorkingID', { article: '', task: '' })
    }

  }

})

export default store;