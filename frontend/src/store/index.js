import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    uiFontsLoaded: false,
    uiTemplateRendered: false,
    uiIsBusy: false,

    uiSnackShow: false,
    uiSnackType: null,
    uiSnackText: null,
    uiSnackShowContact: false,
  },
  getters: {
    uiLoaded: (s) => s.uiFontsLoaded && s.uiTemplateRendered && !s.uiIsBusy,
    uiSnack: (s) => {
      return {
        show: s.uiSnackShow,
        type: s.uiSnackType,
        text: s.uiSnackText,
        showContact: s.uiSnackShowContact
      }
    }
  },
  mutations: {

    setFontsLoaded: (state, payload) => {
      state.uiFontsLoaded = payload
    },
    setTemplateRendered: (state, payload) => {
      state.uiTemplateRendered = payload
    },
    setBusy: (state, payload) => {
      state.uiIsBusy = payload
    },

    setSnack: (state, payload) => {
      state.uiSnackType = payload.type
      state.uiSnackText = payload.text
      state.uiSnackShowContact = payload.showContact
      state.uiSnackShow = true
    },
    hideSnack: (state) => {
      state.uiSnackShow = false
    },
    unsetSnack: (state) => {
      state.uiSnackType = null
      state.uiSnackText = null
      state.uiSnackShowContact = false
    }
  },
  actions: {
    setSnack: ({commit}, payload) => {
      setTimeout(() => {
        commit('setSnack', payload)
      }, payload.delay != null && payload.delay || 0)
    },
    unsetSnack: ({commit}) => {
      commit('hideSnack')
      setTimeout(() => {
        commit('unsetSnack')
      }, 750)
    },

    getMeetings: (_, coachcoacheeId) => Vue.prototype.$http.get('/meetings/', {
      params: coachcoacheeId != null ? { coachcoachee_id: coachcoacheeId } : {}
    }).then(r => ({ metadata: r.data.metadata, data: r.data.data })),
    createMeeting: (_, meetingData) => new Promise((resolve) => {
      Vue.prototype.$http.post(
          '/meetings/',
          JSON.stringify(meetingData),
          { headers: { "Content-Type": "application/json" } }
        ).then((r) => {
          resolve(r.data)
        }).catch(() => {
          resolve(null)
        })
    }),
    updateMeeting: (_, [meetingId, meetingData]) => new Promise((resolve) => {
      Vue.prototype.$http.patch(
          `/meetings/${meetingId}/`,
          JSON.stringify(meetingData),
          { headers: { "Content-Type": "application/json" } }
        ).then((r) => {
          resolve(r.data)
        }).catch(() => {
          resolve(null)
        })
    })

  }
})
