<template>
  <v-container class="py-8" id="meeting-coachee">
    <v-row class="mx-14">
      <v-btn
        plain color="#2563eb"
        class="ml-n3 pa-0 text-capitalize font-weight-bold plain-invert"
        to="/"
      >
        <v-icon>{{ icons.chevronLeft }}</v-icon>voltar
      </v-btn>
    </v-row>

    <v-row id="coachee-profile" class="mt-8 mx-14" v-show="!editMeetingDialog.show || !$vuetify.breakpoint.smAndDown">
      <v-col cols="9">
        <v-row no-gutters>
          <span
            class="fill-width text-caption mb-n1"
            style="color:#BBBCBC"
          >
            Participante
          </span>
          <span class="text-h4 text-left font-weight-bold">{{ coacheeProfile.name }}</span>
        </v-row>

        <v-row no-gutters class="pt-3 pb-0 text-subtitle-2 profile-fields">
          <v-col>
            <span
              class="d-inline-block fill-width text-caption mb-n1"
              style="color:#BBBCBC"
            >
              E-mail
            </span>
            <span class="text-body-2">
              {{ coacheeProfile.hasOwnProperty("email") && coacheeProfile.email }}
            </span>
          </v-col>

          <v-col>
            <span
              class="d-inline-block fill-width text-caption mb-n1"
              style="color:#BBBCBC"
            >
              Cargo
            </span>
            <span
              class="text-body-2 real-capitalize-text"
            >
              {{ coacheeProfile.hasOwnProperty('role') ? coacheeProfile.role : '' }}
            </span>
          </v-col>
        </v-row>

        <v-row no-gutters class="py-3 text-subtitle-2 profile-fields">
          <v-col>
            <span
              class="d-inline-block fill-width text-caption mb-n1"
              style="color:#BBBCBC"
            >
              Área
            </span>
            <span class="text-body-2 real-capitalize-text">
              {{ coacheeProfile.hasOwnProperty("area") && coacheeProfile.area }}
            </span>
          </v-col>

          <v-col>
            <span
              class="d-inline-block fill-width text-caption mb-n1"
              style="color:#BBBCBC"
            >
              Serviço
            </span>
            <span class="text-body-2 real-capitalize-text">
              {{
                coacheeProfile.hasOwnProperty("service") && coacheeProfile.service
              }}
            </span>
          </v-col>
        </v-row>
      </v-col>

      <v-col cols="3"
        class="d-flex align-end flex-column profile-actions"
      >
        <!-- Mentor -->
        <v-btn
          v-if="isCoachView"
          dark tile width="80%"
          color="#2563eb" elevation="0"
          class="mb-5 text-capitalize"
          @click="setEditingMeeting()"
        >
          <span style="font-size: 2vh">
            <v-icon small class="mr-2">{{ icons.plus }}</v-icon>Nova Reunião
          </span>
        </v-btn>
      </v-col>
    </v-row>

    <!-- CAROUSEL -->
    <v-row no-gutters justify="center" class="pt-3">
      <v-col>
        <v-carousel
          hide-delimiters height="auto" :continuous="false"
          v-model="carouselIndex"
          :show-arrows="editMeetingDialog.ui.showArrows"
        >
          <v-carousel-item
            v-for="(meeting, i) in data"
            :key="i"
            class="px-14 meeting-slide"
          >
            <v-row no-gutters justify="center">
              <v-col class="fill-height">
                <v-card
                  tile color="#F9F9F9"
                  class="ma-2 pa-6" height="100%"
                >
                  <v-row no-gutters>
                    <v-col cols="10" class="meeting-heading">
                      <v-card-subtitle align="left"
                        class="d-inline-block pa-1"
                        style="background-color:#2563eb"
                      >
                        <span class="text-caption white--text">
                          {{ $utils.getLocalizedDate(meeting.date_update) }}
                        </span>
                      </v-card-subtitle>
                      <v-card-title align="left"
                        class="px-0 pt-4"
                      >
                        <span class="text-h5 font-weight-medium">
                          Reunião {{ meetingsCounter }}
                        </span>
                      </v-card-title>
                      <v-card-subtitle align="left"
                        class="pa-0"
                      >
                        <span class="text-caption" style="color:#BBBCBC">
                          <b>Mentor:</b> {{ meeting.coachcoachee.coach.name }}
                        </span>
                      </v-card-subtitle>
                    </v-col>
                    <v-col cols="2"
                      class="d-flex align-end flex-column meeting-heading-actions"
                    >
                      <v-btn
                        v-if="isCoachView"
                        dark tile color="#2563eb" elevation="0"
                        class="text-capitalize pa-3"
                        @click="setEditingMeeting(i)"
                      >
                        <span style="font-size: 2vh">
                          <v-icon small class="mr-2">{{ icons.pencil }}</v-icon>Editar
                        </span>
                      </v-btn>
                    </v-col>
                  </v-row>

                  <v-row no-gutters>
                    <v-col>
                      <v-card-text class="pt-0 px-0">
                        <v-row class="mt-5">
                          <v-col>
                            <v-card-subtitle align="left"
                              class="text-subtitle-1 font-weight-bold pa-0 pb-1"
                            >
                              Comentários da reunião
                            </v-card-subtitle>
                            <span
                              class="d-block text-body-2"
                              style="color:#767779"
                            >
                              {{ meeting.note }}
                            </span>
                          </v-col>
                        </v-row>
                        <v-row class="mt-5">
                          <v-col class="pb-0">
                            <v-card-subtitle align="left"
                              class="text-subtitle-1 font-weight-bold pa-0 pb-1"
                            >
                              Tarefas
                            </v-card-subtitle>
                            <task-list :tasks="meeting.tasks" :metadata="metadata" />
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
            </v-row>
          </v-carousel-item>

          <!-- DIALOG NEW/EDIT MEETING -->
          <v-carousel-item
            v-if="editMeetingDialog.show"
            ref="editMeetingDialog" class="px-14 meeting-slide"
          >
            <v-overlay :value="editMeetingDialog.ui.showOverlay && !$vuetify.breakpoint.smAndDown"></v-overlay>
            <v-row no-gutters justify="center" style="position:relative; z-index:6;">
              <v-col class="fill-height">
                <v-card
                  tile color="#F9F9F9"
                  class="ma-2 pa-6 meeting-editor" height="100%"
                >


                  <v-row no-gutters>
                    <v-col cols="10" class="meeting-heading">
                      <v-card-subtitle align="left"
                        class="d-inline-block pa-1"
                        style="background-color:#2563eb"
                      >
                        <span class="text-caption white--text">
                          {{ $utils.getLocalizedDate(editMeetingDialog.data.date_update) }}
                        </span>
                      </v-card-subtitle>
                      <v-card-title align="left"
                        class="px-0 pt-4"
                      >
                        <span class="text-h5 font-weight-medium">
                          {{ editMeetingDialog.isNew && "Nova reunião" || "Modificar reunião" }}
                        </span>
                      </v-card-title>
                      <v-card-subtitle align="left"
                        class="pa-0"
                      >
                        <span class="text-caption" style="color:#BBBCBC">
                          <b>Mentor:</b> {{ editMeetingDialog.data.coachcoachee.coach.name }}
                        </span>
                      </v-card-subtitle>
                    </v-col>
                  </v-row>

                  <v-row no-gutters>
                    <v-col>
                      <v-card-text class="pt-0 px-0">

                        <v-form
                          ref="editMeetingForm" lazy-validation
                          v-model="editMeetingDialog.isValid"
                        >

                          <v-row class="mt-5">
                            <v-col>
                              <v-card-subtitle align="left"
                                class="text-subtitle-1 font-weight-bold pa-0 pb-1"
                              >
                                Comentários da reunião
                              </v-card-subtitle>
                              <v-textarea
                                dense outlined no-resize
                                background-color="white"
                                rows="4" color="#2563eb"
                                placeholder="Digite aqui..."
                                v-model="editMeetingDialog.data.note"
                                :rules="requiredRule"
                              ></v-textarea>
                            </v-col>
                          </v-row>

                        </v-form>

                        <v-row>
                          <v-col class="pb-0">
                            <v-row no-gutters class="pb-3 task-list-heading">
                              <v-col
                                class="d-flex align-end"
                              >
                                <v-card-subtitle align="left"
                                  class="text-subtitle-1 font-weight-bold pa-0"
                                >
                                  Tarefas
                                </v-card-subtitle>
                              </v-col>
                              <v-col
                                class="d-flex align-end flex-column"
                              >
                                <v-btn
                                  dark tile color="#2563eb" elevation="0"
                                  class="text-capitalize pa-2"
                                  @click="setEditingTask()"
                                >
                                  <span style="font-size: 2vh">
                                    <v-icon small class="mr-2">{{ icons.plus }}</v-icon>Nova tarefa
                                  </span>
                                </v-btn>
                              </v-col>
                            </v-row>
                            <task-list
                              :tasks="editMeetingDialog.data.tasks"
                              :metadata="metadata"
                              editable
                              @edit="setEditingTask"
                              @delete="Object.assign(deleteTaskDialog, { index: $event, show: true })"
                            />
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-col>
                  </v-row>

                  <v-row class="pt-5 meeting-form-actions">
                    <v-col class="d-flex justify-end">
                      <v-btn
                        dark tile color="#2563eb" elevation="0" width="calc(2vh*10)"
                        class="text-capitalize pa-2 mr-2"
                        @click="unsetEditingMeeting()"
                      >
                        <span style="font-size: 2vh">
                          Cancelar
                        </span>
                      </v-btn>
                      <v-btn
                        dark tile color="#2563eb" elevation="0" width="calc(2vh*10)"
                        class="text-capitalize pa-2"
                        @click="saveEditingMeeting()"
                      >
                        <span style="font-size: 2vh">
                          Salvar
                        </span>
                      </v-btn>
                    </v-col>
                  </v-row>

                </v-card>
              </v-col>
            </v-row>
          </v-carousel-item>
          <!-- /DIALOG NEW/EDIT MEETING -->

        </v-carousel>
      </v-col>
    </v-row>


    <!-- DIALOG NEW/EDIT TASK -->
    <v-dialog
      persistent max-width="640" content-class="task-editor-dialog"
      v-model="editTaskDialog.show"
    >
      <v-card v-if="editTaskDialog.show">
        <v-card-title>
          {{ editTaskDialog.isNew && "Nova tarefa" || "Modificar tarefa" }}
        </v-card-title>
        <v-card-text>
          <v-form lazy-validation ref="editTaskForm" v-model="editTaskDialog.isValid">
            <v-row class="mt-1">
              <v-col cols="6">
                <v-select
                  label="Status" dense
                  item-text="display_name" item-value="value"
                  v-model="editTaskDialog.data.status"
                  :items="metadata.task_status_metadata"
                  :disabled="editTaskDialog.data.task_id == null"
                ></v-select>
              </v-col>
            </v-row>
            <v-row class="mt-1">
              <v-col>
                <v-select
                  label="Tipo" dense return-object
                  item-text="display_name" item-value="value"
                  v-model="editTaskDialog.data.skill_type"
                  :items="metadata.task_skills_metadata"
                  :rules="[v => v.hasOwnProperty('value') && !!v.value || 'Campo obrigatório']"
                  :disabled="editTaskDialog.data.task_id != null"
                ></v-select>
              </v-col>
              <v-col>
                <v-select
                  label="Competência" dense persistent-hint
                  item-text="display_name" item-value="value"
                  v-model="editTaskDialog.data.skill_id"
                  :items="editTaskDialog.data.skill_type.children"
                  :rules="requiredRule"
                  :disabled="editTaskDialog.data.task_id != null || editTaskDialog.data.skill_type.children.length === 0"
                  :hint="(editTaskDialog.data.task_id == null && editTaskDialog.data.skill_type.children.length === 0) && 'Selecione o tipo' || ''"
                ></v-select>
              </v-col>
            </v-row>
            <v-row class="mt-1">
              <v-col>
                <v-menu
                  offset-y max-width="290px" min-width="auto"
                  v-model="editTaskDialog.ui.dateStartedShow"
                  :close-on-content-click="false"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      label="Data" dense readonly
                      v-bind="attrs" v-on="on"
                      v-model="editTaskDialogUiDateStartedFormatted"
                      :append-icon="icons.calendar"
                      :rules="requiredRule"
                      :disabled="editTaskDialog.data.task_id != null"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    no-title locale="pt-BR"
                    v-model="editTaskDialog.data.date_started"
                    @input="editTaskDialog.ui.dateStartedShow = false"
                    :min="new Date().toISOString()"
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-col>
                <v-menu
                  offset-y max-width="290px" min-width="auto"
                  v-model="editTaskDialog.ui.dateConcludedShow"
                  :close-on-content-click="false"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      label="Prazo" dense readonly
                      v-bind="attrs" v-on="on"
                      v-model="editTaskDialogUiDateConcludedFormatted"
                      :append-icon="icons.calendar"
                      :rules="requiredRule"
                      :disabled="editTaskDialog.data.task_id != null"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    no-title locale="pt-BR"
                    v-model="editTaskDialog.data.date_concluded"
                    @input="editTaskDialog.ui.dateConcludedShow = false"
                    :min="new Date().toISOString()"
                  ></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
            <v-row class="mt-1">
              <v-col>
                <v-textarea
                  label="Observações" rows="3"
                  dense filled no-resize
                  v-model="editTaskDialog.data.description"
                  :rules="requiredRule"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="primary"
            text
            @click="unsetEditingTask()"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="saveEditingTask()"
          >
          {{ editTaskDialog.isNew && "Adicionar" || "Modificar" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- /DIALOG NEW/EDIT TASK -->

    <!-- DIALOG TASK DELETE CONFIRMATION -->
    <v-dialog
      ref="deleteTaskDialog"
      max-width="400" persistent
      v-model="deleteTaskDialog.show"
    >
      <v-card>
        <v-card-title>
          Confirmação
        </v-card-title>
        <v-card-text>
          <v-row class="mt-1">
            <v-col>
              Tem certeza que deseja deletar a tarefa?
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="primary"
            text
            @click="handleDeleteEditingTask(true)"
          >
            Não
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="handleDeleteEditingTask(false)"
          >
            Sim
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- /DIALOG TASK DELETE CONFIRMATION -->

  </v-container>
</template>

<script>
import TaskList from "@/components/TaskList.vue"
import { mapMutations, mapActions } from "vuex"
import { mdiChevronLeft, mdiPlus, mdiPencil, mdiDelete, mdiCalendar } from '@mdi/js'

export default {
  name: "MeetingsView",
  components: { TaskList },

  data() {
    return {

      icons: {
        chevronLeft: mdiChevronLeft,
        plus: mdiPlus,
        pencil: mdiPencil,
        delete: mdiDelete,
        calendar: mdiCalendar
      },
      promissedata: null,
      metadata: {},
      data: [],

      carouselIndex: 0,

      editMeetingDialog: {
        show: false,
        index: -1,
        isNew: true,
        isValid: true,
        data: null,
        emptyData: {
          coachcoachee: {
            coach: { name: null }
          },
          date_create: null,
          date_update: null,
          note: null,
          tasks: []
        },
        ui: {
          showArrows: true,
          showOverlay: false
        }
      },
      editTaskDialog: {
        show: false,
        index: -1,
        isNew: true,
        isValid: true,
        data: null,
        emptyData: {
          date_concluded: null,
          date_started: null,
          description: null,
          skill_id: null,
          skill_type: {
            children: []
          },
          status: "N"
        },
        ui: {
          dateStartedShow: false,
          dateConcludedShow: false
        }
      },
      deleteTaskDialog: {
        show: false,
        index: -1
      },

      requiredRule: [v => !!v || 'Campo obrigatório'],

      editDialogShow: false, editDialogOLShow: false
    }
  },

  computed: {

    isCoachView() {
      return this.$route.meta.isCoachView
    },

    coachcoacheeId() {
      return this.$route.params.id
    },

    coacheeProfile() {
      return (
        this.isCoachView && this.$userProfile.getCoachee(this.coachcoacheeId) || this.$userProfile
      )
    },
    coachProfile() {
      return (
        this.isCoachView && this.$userProfile || this.$userProfile.getCoach()
      )
    },

    meetingsCounter() {
      return (
        this.data.length > 0 && `${this.data.length - this.carouselIndex} de ${this.data.length}` || '- de -'
      )
    },

    // COMPUTED VALUES FOR "editTaskDialog"
    editTaskDialogUiDateStartedFormatted: {
      set() {},
      get() {
        return (
          this.editTaskDialog.data != null
          && this.$utils.getLocalizedDate(this.editTaskDialog.data.date_started)
          || null
        )
      }
    },
    editTaskDialogUiDateConcludedFormatted: {
      set() {},
      get() {
        return (
          this.editTaskDialog.data != null
          && this.$utils.getLocalizedDate(this.editTaskDialog.data.date_concluded)
          || null
        )
      }
    }
  },

  created() {
    this.promissedata = this.getAllMeetings()
  },

  mounted() {
    this.$nextTick(async () => {
      this.setBusy(true)
      this.setTemplateRendered(true)

      try {
        await this.promissedata
      } catch (error) {
        this.setSnack({ type: 'error', text: 'Não foi possível carregar as reuniões. Tente novamente.', showContact: false })
      } finally {
        this.setBusy(false)
      }
    })
  },

  methods: {
    ...mapMutations(["setTemplateRendered", "setBusy"]),
    ...mapActions([
      "setSnack",
      "getMeetings",
      "createMeeting",
      "updateMeeting",
    ]),

    async getAllMeetings() {
      const {metadata, data} = await this.getMeetings(this.coachcoacheeId)

      this.metadata = Object.assign({}, metadata)
      this.data = data
    },

    // METHODS FOR NEW/EDIT MEETING
    setEditingMeeting(meetingIndex=null) {

      if (meetingIndex == null) {
        // is new
        this.editMeetingDialog.isNew = true
        this.editMeetingDialog.index = this.carouselIndex
        this.editMeetingDialog.data = Object.assign(
          {},
          JSON.parse(JSON.stringify(this.editMeetingDialog.emptyData)),
          {
            date_update: new Date(),
            coachcoachee: {
              coach: { name: this.$userProfile.name },
              rel_id: this.coachcoacheeId
            }
          }
        )
      } else {
        // is editing
        this.editMeetingDialog.isNew = false
        this.editMeetingDialog.index = meetingIndex
        this.editMeetingDialog.data = Object.assign(
          {},
          JSON.parse(JSON.stringify(this.editMeetingDialog.emptyData)),
          this.data[meetingIndex]
        )
      }

      this.editMeetingDialog.show = true

      this.$nextTick(() => {

        const unwatch = this.$watch(
          () => this.$refs.editMeetingDialog.inTransition,
          (inTransitionNow, inTransitionBefore) => {
            if (inTransitionBefore && !inTransitionNow) {
              this.editMeetingDialog.ui.showArrows = false
              this.editMeetingDialog.ui.showOverlay = true
              this.$vuetify.goTo(this.$vuetify.breakpoint.smAndDown ? 0 : this.$refs.editMeetingDialog)
              unwatch()
            }
          }
        )

        this.carouselIndex = this.data.length
      })
    },
    unsetEditingMeeting(callback=null) {
      this.editMeetingDialog.ui.showOverlay = false
      this.editMeetingDialog.ui.showArrows = true

      this.carouselIndex = this.editMeetingDialog.index

      this.$vuetify.goTo('#coachee-profile').then(() => {
        this.editMeetingDialog.show = false

        this.$refs.editMeetingForm.reset()
        this.editMeetingDialog.index = -1
        this.editMeetingDialog.data = null
      })

      const self = this
      this.$nextTick(() => {
        if (callback != null) {
          callback(self)
        }
      })
    },
    saveEditingMeeting() {

      this.$refs.editMeetingForm.validate()

      const self = this
      this.$nextTick(async () => {
        if (self.editMeetingDialog.isValid) {

          self.setBusy(true)

          let fnc, fncArgs, snackAttrs

          if (self.editMeetingDialog.isNew) {
            fnc = self.createMeeting
            fncArgs = self.editMeetingDialog.data
          } else {
            fnc = self.updateMeeting
            fncArgs = [ self.editMeetingDialog.data.id, self.editMeetingDialog.data ]
          }

          const result = await fnc(fncArgs)
          if (result != null) {

            snackAttrs = {
              delay: 500,
              type: "success",
              text: "Informações salvas com êxito.",
              showContact: false
            }

            if (!this.editMeetingDialog.isNew) { // if (this.editMeetingDialog.index >= 0) {
              self.$set(self.data, this.editMeetingDialog.index, Object.assign({}, result))
            } else {
              self.data.splice(0, 0, Object.assign({}, result))
              // self.data.push(Object.assign({}, result))
              self.editMeetingDialog.index = 0
            }

          } else {

            snackAttrs = {
              delay: 500,
              type: "error",
              text: "Ocorreu um erro durante a operação.",
              showContact: true
            }

          }

          self.unsetEditingMeeting((vm) => {
            vm.setSnack(snackAttrs)
            vm.setBusy(false)
          })

        }
      })
    },
    // METHODS FOR NEW/EDIT MEETING

    // METHODS FOR NEW/EDIT/DELETE TASK
    setEditingTask(taskIndex=null) {
      if (taskIndex == null) {
        // is new
        this.editTaskDialog.isNew = true
        this.editTaskDialog.data = Object.assign(
          {},
          JSON.parse(JSON.stringify(this.editTaskDialog.emptyData))
        )
      } else {
        // is editing
        const editingTask = this.editMeetingDialog.data.tasks[taskIndex]

        this.editTaskDialog.isNew = false
        this.editTaskDialog.index = taskIndex
        this.editTaskDialog.data = Object.assign(
          {},
          JSON.parse(JSON.stringify(this.editTaskDialog.emptyData)),
          editingTask,
          {
            'skill_type': this.$utils.getChoiceByValue(
              this.metadata.task_skills_metadata,
              editingTask.skill_id,
              true, true
            )
          }
        )
      }

      this.$nextTick(() => {
        this.editTaskDialog.show = true
      })
    },
    unsetEditingTask() {
      this.editTaskDialog.show = false

      this.$refs.editTaskForm.reset()
      this.editTaskDialog.index = -1
      this.editTaskDialog.data = null
    },
    saveEditingTask() {

      this.$refs.editTaskForm.validate()

      const self = this
      this.$nextTick(() => {
        if (self.editTaskDialog.isValid) {

          if (this.editTaskDialog.index >= 0) {
            self.$set(
              self.editMeetingDialog.data.tasks,
              this.editTaskDialog.index,
              Object.assign({}, self.editTaskDialog.data)
            )
          } else {
            self.editMeetingDialog.data.tasks.push(Object.assign({}, self.editTaskDialog.data))
          }

          self.unsetEditingTask()
        }
      })
    },
    handleDeleteEditingTask(cancel) {
      if (!cancel && this.deleteTaskDialog.index >= 0) {
        this.editMeetingDialog.data.tasks.splice(this.deleteTaskDialog.index, 1)
      }

      const self = this
      this.$nextTick(() => {
        self.deleteTaskDialog.index = -1
        self.deleteTaskDialog.show = false
      })
    }
    // /METHODS FOR NEW/EDIT/DELETE TASK
  }
}
</script>

<style lang="scss">
.v-data-table table {
  table-layout: fixed;
}
.v-data-table thead th {
  font-size: 0.875rem !important;
  font-weight: 500;
  line-height: 1.25rem;
  letter-spacing: 0.0178571429em !important;
  color:#2563eb !important;
  box-shadow: inset 0 -2px 0 #2563eb !important;
}
.v-data-table thead tr th:nth-child(2),
.v-data-table tbody tr td:nth-child(2) {
  width: 20%;
}
.v-data-table thead tr th:nth-child(5),
.v-data-table tbody tr td:nth-child(5) {
  width: 25%;
}
.v-data-table thead tr th:nth-child(7),
.v-data-table tbody tr td:nth-child(7) {
  width: 10%;
}

.v-input__slot {
  border-radius: unset !important;
}
.v-input__slot input, .v-input__slot textarea {
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    line-height: 1.25rem !important;
    letter-spacing: 0.0178571429em !important;
    color: #767779 !important;
}
.v-input__slot:hover fieldset {
  color: #2563eb !important;
}

.fill-width {
  width: 100%;
}

.plain-invert:hover .v-btn__content {
  opacity: 0.62 !important;
}

.plain-invert .v-btn__content {
  opacity: 1 !important;
}
</style>

<style lang="scss">
@media (max-width: 600px) {
  #meeting-coachee { padding-top: 24px !important; }
  #meeting-coachee .meeting-editor .meeting-heading { flex-basis: 100%; max-width: 100%; }
  #meeting-coachee .meeting-form-actions { margin: 0; }
  #meeting-coachee .meeting-form-actions > .col { display: grid !important; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0; }
  #meeting-coachee .meeting-form-actions .v-btn { width: 100% !important; min-width: 0; margin: 0 !important; }
  #meeting-coachee .v-btn span { font-size: 14px !important; }
  #meeting-coachee .v-btn { min-height: 40px; }
  #meeting-coachee .task-list-heading { align-items: center; gap: 12px; }
  #meeting-coachee .task-list-heading > .col:first-child { flex: 1; }
  #meeting-coachee .task-list-heading > .col:last-child { flex: 0 0 auto; }
  .task-editor-dialog .v-form .col { flex: 0 0 100%; max-width: 100%; }
  .task-editor-dialog .v-card__actions { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; padding: 16px; }
  .task-editor-dialog .v-card__actions .v-btn { margin: 0 !important; min-height: 44px; }
  #coachee-profile .profile-fields { display: grid; grid-template-columns: minmax(0, 1fr); gap: 16px; }
  #coachee-profile .profile-fields > .col { padding: 0; overflow-wrap: anywhere; }
  #coachee-profile .profile-actions .v-btn { width: 100% !important; }
  #meeting-coachee .meeting-heading { flex: 0 0 65%; max-width: 65%; }
  #meeting-coachee .meeting-heading-actions { flex: 0 0 35%; max-width: 35%; }
  #meeting-coachee .meeting-slide > .row > .col > .v-card { padding: 20px 16px !important; }
  #meeting-coachee .meeting-slide { padding-left: 0 !important; padding-right: 0 !important; }
  #meeting-coachee .mx-14 { margin-left: 0 !important; margin-right: 0 !important; }
  #coachee-profile > .col-9, #coachee-profile > .col-3 { flex: 0 0 100%; max-width: 100%; }
}
</style>
