<template>
  <v-container class="pa-6 devsync-home">

    <v-row align="stretch" justify="center" class="home-dashboard">
      <v-col cols="12" md="5" align="center">
        <v-card color="#0b1220" min-height="360" height="100%" class="d-flex flex-column">
          <v-row no-gutters align="center" justify="center">
            <v-col align="center">
              <v-img
                max-height="150" class="mt-8"
                contain
                src="@/assets/img/sync-mark.svg"
              ></v-img>
              <span align="center" justify="center" class="d-block pt-3 hero-text" style="font-size: 6.5vh">
                Olá,
                <br>
                {{ $userProfile.name }}!
                <small class="welcome-subtitle">Conecte metas, pessoas e evolução.</small>
              </span>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
      <v-col cols="12" md="7">
        <v-card align="center" height="100%" class="d-flex flex-column">
          <v-card-title class="text-h5 justify-center">
            <span style="font-size: 4vh;">Acessar</span>
          </v-card-title>
          <v-divider horizontal></v-divider>
          <v-card-text class="my-auto">
            <v-row no-gutters justify="center" align="center">
              <v-col
                justify="center"
                align="center"
              >
                <v-btn
                  dark
                  plain
                  height="auto"
                  width="140px"
                  class="btn-coach-coachee"
                  :disabled="!$userProfile.is_coach"
                  @click="handleShowCoacheesSlider"
                >
                  <v-row
                    justify="center"
                    align="center"
                  >
                    <v-icon color="white" size="80px">{{ icons.whistleOutline }}</v-icon>
                  </v-row>
                  <v-row
                    justify="center"
                    align="center"
                    style="font-size: 2vh"
                  >
                    Mentor
                  </v-row>
                </v-btn>
              </v-col>
              <v-col
                justify="center"
                align="center"
              >
                <v-btn
                  dark
                  plain
                  height="auto"
                  width="140px"
                  class="btn-coach-coachee"
                  :disabled="!$userProfile.is_coachee"
                  :to="{ name: 'Participant Meetings' }"
                >
                  <v-row
                    justify="center"
                    align="center"
                  >
                    <v-icon color="white" size="80px">{{ icons.sealVariant }}</v-icon>
                  </v-row>
                  <v-row
                    justify="center"
                    align="center"
                    style="font-size: 2vh"
                  >
                    Participante
                  </v-row>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Slider Coachees -->
    <v-row
      v-if="showCoacheesSlider"
      id="coachees-slider"
      align="center"
      justify="center"
      class="mt-5"
    >
      <v-col cols="12">

        <v-card
          elevation="0"
          tile
          color="#f6f6f6"
        >
          <v-card-title class="text-h5 justify-space-between ">
            <span style="font-size: 4vh">Participantes ({{ $userProfile.coachees.length }})</span>
          </v-card-title>
          <v-divider horizontal></v-divider>
          <v-card-text class="px-0">
            <v-slide-group
              show-arrows="always"

            >
              <v-slide-item
                v-for="item in $userProfile.coachees"
                :key="item.coachcoachee_id"
              >
                <v-card
                  elevation="8"
                  class="ma-4"
                  height="234"
                  width="310"
                  color= "white"
                  :to="{ name: 'Mentor Meetings', params: {id: item.coachcoachee_id}}"
                >
                  <v-card-title class="font-weight-bold">
                    {{ item.name}} <!-- Nome do coachee -->
                  </v-card-title>
                  <v-card-subtitle style="color:#2563eb">
                    <b>Última Reunião:</b> {{ getPTBRDateFormat(item.date_update) }}
                  </v-card-subtitle>
                  <v-card-text class="mr-1">
                    <b>Cargo:</b> <span class="real-capitalize-text">{{item.role}}</span>
                    <br>
                    <b>E-mail:</b> {{ item.email }}
                    <br>
                    <b>Observações:</b>
                    <br>
                    <v-row
                      class="my-auto ml-2 mr-auto truncated-text"
                      style="height: calc(22px * 3); -webkit-line-clamp: 3;"
                    >
                      {{ item.note }}
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-slide-item>
            </v-slide-group>
          </v-card-text>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapMutations } from "vuex"
import { mdiWhistleOutline, mdiSealVariant } from "@mdi/js"

export default {
  name: "HomeView",

  data: () => ({
    icons: {
      whistleOutline: mdiWhistleOutline,
      sealVariant: mdiSealVariant,
    },
    showCoachees: false,
  }),
  computed: {
    showCoacheesSlider() {
      return this.$userProfile.is_coach && this.showCoachees
    }
  },

  mounted() {
    this.$nextTick(() => {
      this.setTemplateRendered(true);
    });
  },

  methods: {
    ...mapMutations(["setTemplateRendered"]),

    handleShowCoacheesSlider() {
      this.showCoachees = true;
      this.$nextTick(() => {
        this.$vuetify.goTo("#coachees-slider");
      });
    },

    getPTBRDateFormat(date) {
      return date != null && new Date(date).toLocaleDateString("pt-BR", {timeZone: 'UTC'}) || "-"
    }
  },
};
</script>

<style lang="scss">
.devsync-home {
  max-width: 1200px;
  min-height: calc(100vh - 100px);
  min-height: calc(100dvh - 100px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 24px !important;
}
.devsync-home > .row { flex: 0 0 auto; }
@media (max-width: 600px) {
  .devsync-home .btn-coach-coachee { max-width: 100%; }
}
.welcome-subtitle { display: block; font-size: 16px; color: #93c5fd; margin: 20px 16px 32px; }
// Hero welcome text
.hero-text {
  font-size: 2.5rem !important;
  font-weight: 400;
  line-height: 2.625rem;
  letter-spacing: normal !important;
  color: white;
}
// /Hero welcome text
// Coach and coachee buttons
.btn-coach-coachee:before {
  display: block !important;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: white;
  transition: opacity 0.2s cubic-bezier(0.4, 0, 0.6, 1);
  opacity: 0;
  z-index: 1;
}
.btn-coach-coachee:hover::before {
    opacity: 0.08;
}

.btn-coach-coachee .v-btn__content {
  display: block !important;
  opacity: 1 !important;
}

// # icon
.btn-coach-coachee .v-btn__content div.row:nth-child(1) {
    background-color: #2563eb;
    height: 120px;
    width: 120px;
    margin: 0 auto;
    border-radius: 60px;
}
.btn-coach-coachee.v-btn--disabled .v-btn__content div.row:nth-child(1) {
    background-color: rgba(0, 0, 0, 0.12) !important;
}
// /# icon
// # text
.btn-coach-coachee .v-btn__content div.row:nth-child(2) {
    margin: 12px 0;
    color: #2563eb;
}
.btn-coach-coachee.v-btn--disabled .v-btn__content div.row:nth-child(2) {
    color: rgba(0, 0, 0, 0.26) !important;
}


.truncated-text {
  display: block;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
