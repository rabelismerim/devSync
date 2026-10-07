<template>
  <v-app>
    <!-- NAVBAR -->
    <v-app-bar
      app
      dark
      elevate-on-scroll
      height="60px"
      color="black"
      class="pl-6 pr-6"
      content-class="mx-0"
      id="header-nav"
    >
      <router-link to="/" class="brand-link" aria-label="DevSync — início">
        <img src="@/assets/img/devsync.svg" width="176" height="42" alt="DevSync" />
      </router-link>

      <v-spacer></v-spacer>

      <template v-if="$userAuthorized">
        <div class="d-inline-block mt-1 grey--text devsync-profile-name">
          <v-avatar size="24" class="mt-n1 mr-2">
            <img v-if="$userProfile.picture"
              :src="`data:image/jpeg;base64,${$userProfile.picture}`"
            />
            <v-icon v-else color="grey">{{ icons.accountCircle }}</v-icon>
          </v-avatar>
          Olá, {{ $userProfile.name }}
        </div>

        <v-divider
          inset
          vertical
          class="mx-6"
        ></v-divider>
      </template>

    </v-app-bar>

    <!-- MAIN -->
    <v-main>

      <v-overlay :value="!uiLoaded" opacity="0.9">
        <v-progress-circular
          indeterminate
          size="64"
          color="primary"
        ></v-progress-circular>
      </v-overlay>

      <v-snackbar
        timeout="5000"
        transition="slide-y-reverse-transition"
        v-model="showSnack"
        id="snack-bar"
      >
        <v-alert
          elevation="6"
          :type="uiSnack.type"
        >
          {{ uiSnack.text }}
          <template v-if="uiSnack.showContact">
            <a
              href="#"
              title="Contate a equipe da aplicação DevSync"
            >Contate-nos</a>.
          </template>
        </v-alert>
      </v-snackbar>

      <router-view/>

    </v-main>

    <!-- FOOTER -->
    <v-footer
      app
      dark
      color="black"
      height="40px"
      class="px-10"
      id="footer-nav"
    >
      <span class="caption">© {{ new Date().getFullYear() }} DevSync</span>
      <v-spacer />
      <span class="caption">Desenvolvimento em sintonia</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import { mdiAccountCircle } from '@mdi/js'
import WebFontLoader from 'webfontloader'

export default {
  name: 'App',

  data: () => ({
    icons: {
      accountCircle: mdiAccountCircle
    }
  }),

  computed: {
    ...mapGetters(['uiLoaded', 'uiSnack']),
    showSnack: {
      get() {
        return this.uiSnack.show
      },
      set() {
        this.unsetSnack()
      }
    }
  },

  async created() {
    WebFontLoader.load({
      google: {
        families: [
          'Open Sans:300,400,500,600,700,800',
          'Roboto:100,300,400,500,700,900'
        ],
      },
      active: () => this.setFontsLoaded(true),
      inactive: () => this.setFontsLoaded(true),
      timeout: 2000
    })
  },

  methods: {
    ...mapMutations(['setFontsLoaded']),
    ...mapActions(['unsetSnack'])
  }
}
</script>
<style lang="scss">

  html { overflow-y: auto !important; }

  .brand-link { display: inline-flex; align-items: center; }
  #header-nav { border-bottom: 2px solid #2563eb !important; }
  .v-main { background: #f3f6fc !important; }
  .v-card { border-radius: 14px !important; }
  @media (max-width: 600px) {
    #header-nav { padding: 0 12px !important; }
    #header-nav .devsync-profile-name { letter-spacing: 0 !important; }
    #footer-nav { padding: 0 12px !important; position: static !important; }
    .v-main { padding-bottom: 0 !important; }
    #header-nav .v-divider { display: none; }
    #header-nav .brand-link img { width: 150px; }
    #header-nav .devsync-profile-name { max-width: 145px; margin-left: 12px; }
  }
  .v-application {
    [class*='text-'] {
      font-family: 'Open Sans', sans-serif !important;
    }
    font-family: 'Open Sans', sans-serif !important;
  }

  #header-nav .devsync-profile-name {
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .0892857143em !important;
    text-indent: 0.0892857143em !important;
  }

  #snack-bar .v-snack__wrapper {
    min-width: 100px !important;
    border-radius: 0 !important;
    background-color: transparent !important;
    box-shadow: none !important;
  }
  #snack-bar .v-snack__wrapper .v-snack__content {
    padding: 0 !important;
  }
  #snack-bar .v-alert {
    margin-bottom: 0 !important;
  }
  #snack-bar a {
    color: inherit !important;
    text-decoration: none;
    opacity: 0.75;
  }

  .real-capitalize-text:first-letter {
    text-transform: capitalize
  }
</style>
