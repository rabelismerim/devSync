import Vue from 'vue'
import vuetify from './plugins/vuetify'
import Axios from './plugins/axios'

import App from './App.vue'
import router from './router'
import store from './store'

const userProfile = window.getProfile ? window.getProfile() : null

Vue.config.productionTip = false

Vue.prototype.$http = Axios
Vue.prototype.$userAuthorized = userProfile != null
Vue.prototype.$userProfile = userProfile && Object.assign(userProfile, {
  'getCoach': () => (
    Vue.prototype.$userProfile.is_coachee
    && Vue.prototype.$userProfile.coach
  ),
  'getCoachee': (coachcoacheeId) => (
    Vue.prototype.$userProfile.is_coach
    && Vue.prototype.$userProfile.coachees?.find(
      c => c.coachcoachee_id === parseInt(coachcoacheeId, 10)
    )
  )
})
Vue.prototype.$utils = {
  'getLocalizedDate': (date) => (
    date != null && new Date(date).toLocaleDateString("pt-BR", {timeZone: 'UTC'}) || null
  ),
  'getChoiceByValue': (source, value, isChild=false, returnParent=false) => {
    let result
    if (Array.isArray(source)) {
      for (const i of source) {
        if (isChild) {
          result = i.children && Vue.prototype.$utils.getChoiceByValue(i.children, value)
          if (result != null) {
            if (returnParent) {
              result = Object.assign({}, i)
            }
            break
          }
        } else if (i.value === value) {
          result = Object.assign({}, i)
          break
        }
      }
    }
    return result
  },
  'getDisplayName': (source, value, isChild=false, returnParent=false) => {
    return Vue.prototype.$utils.getChoiceByValue(source, value, isChild, returnParent)?.display_name
  }
}


new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
