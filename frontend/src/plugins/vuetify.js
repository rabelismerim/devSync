import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'

Vue.use(Vuetify)

export default new Vuetify({
    font: false,
    icons: {
        iconfont: 'mdiSvg'
    },
    theme: {
        themes: {
            light: {
                primary: '#2563eb',
                secondary: '#0b1220',
                success: '#2563eb'
            },
            dark: {
                primary: '#2563eb',
                secondary: '#0b1220',
                success: '#2563eb'
            },
        },
    }
})
