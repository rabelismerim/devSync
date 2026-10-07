import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '../store'

import MeetingsView from '@/views/MeetingsView.vue'


Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: '/devsync',
  routes: [

    {
      path: '/',
      name: 'Landing Page',
      component: () => Vue.prototype.$userAuthorized && import('@/views/HomeView') || import('@/views/ErrorView'),
      meta: () => ({ isErrorView: !Vue.prototype.$userAuthorized })
    },


    {
      path: '/participante/reunioes',
      name: 'Participant Meetings',
      meta: { isCoachView: false },
      component: MeetingsView
    },
    {
      path: '/mentor/:id/reunioes',
      name: 'Mentor Meetings',
      meta: { isCoachView: true },
      component: MeetingsView
    }

  ]
})

// ROUTER GUARD
router.beforeEach((to, from, next) => {

  // console.log('to', to)

  // set loading
  store.commit('setTemplateRendered', false)

  let toOverride, snackAttrs = { type: 'error', showContact: true, delay: 750 }

  // TRYING TO ACCESS AN INEXISTANT ROUTE
  if (to.matched.length === 0) {
    toOverride = { name: 'Landing Page' }
    snackAttrs['text'] = 'Página não encontrada.'

  // TRYING TO ACCESS COACHEE VIEW WITHOUT HAVING A COACH
  } else if (!Vue.prototype.$userAuthorized && to.name !== 'Landing Page') {
    toOverride = { name: 'Landing Page' }
    snackAttrs.text = 'Entre para acessar suas reuniões.'
  } else if (to.name === 'Participant Meetings' && !Vue.prototype.$userProfile.is_coachee) {
    toOverride = { name: 'Landing Page' }
    snackAttrs['text'] = 'Usuário não registrado como participante.'

  // TRYING TO ACCESS COACH VIEW NOT BEING ONE
  } else if (to.name === 'Mentor Meetings') {

    if (!Object.prototype.hasOwnProperty.call(to.params, 'id')) {
      toOverride = { name: 'Landing Page' }
      snackAttrs['text'] = 'Página não encontrada.'
    } else if (!Vue.prototype.$userProfile.getCoachee(to.params.id)) {
      toOverride = { name: 'Landing Page' }
      snackAttrs['text'] = 'Usuário não registrado como mentor.'
    }

  }

  if (toOverride != null) {

    if (from.name === 'Landing Page') {
      toOverride = false
      snackAttrs['delay'] = 0

      // set loaded
      store.commit('setTemplateRendered', true)
    }

    next(toOverride)
    store.dispatch('setSnack', snackAttrs)

  } else {
    next()
  }

})

export default router
