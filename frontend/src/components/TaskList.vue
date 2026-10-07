<template>
  <div class="task-list">
    <p v-if="!tasks.length" class="task-empty">Nenhuma tarefa cadastrada.</p>
    <div v-else-if="$vuetify.breakpoint.smAndDown" class="task-cards">
      <article v-for="(task, index) in tasks" :key="task.task_id || index" class="task-card">
        <div class="task-card-heading">
          <div>
            <span class="task-label">{{ skillName(task, true) }}</span>
            <h3>{{ skillName(task) }}</h3>
          </div>
          <v-chip small outlined color="primary">{{ statusName(task) }}</v-chip>
        </div>
        <div class="task-description"><span class="task-label">Observações</span><p>{{ task.description || 'Sem observações.' }}</p></div>
        <dl class="task-dates">
          <div><dt>Início</dt><dd>{{ date(task.date_started) }}</dd></div>
          <div><dt>Prazo</dt><dd>{{ date(task.date_concluded) }}</dd></div>
        </dl>
        <div v-if="editable" class="task-actions">
          <v-btn small text color="primary" :disabled="task.status === 'C'" @click="$emit('edit', index)">
            <v-icon small left>{{ icons.pencil }}</v-icon>Editar tarefa
          </v-btn>
          <v-btn small text color="primary" :disabled="task.task_id != null" @click="$emit('delete', index)">
            <v-icon small left>{{ icons.delete }}</v-icon>Excluir
          </v-btn>
        </div>
      </article>
    </div>
    <v-simple-table v-else class="task-table">
      <thead><tr><th>Tipo</th><th>Competência</th><th>Início</th><th>Prazo</th><th>Observações</th><th>Status</th><th v-if="editable">Ações</th></tr></thead>
      <tbody>
        <tr v-for="(task, index) in tasks" :key="task.task_id || index">
          <td>{{ skillName(task, true) }}</td><td>{{ skillName(task) }}</td>
          <td>{{ date(task.date_started) }}</td><td>{{ date(task.date_concluded) }}</td>
          <td>{{ task.description }}</td><td>{{ statusName(task) }}</td>
          <td v-if="editable" class="task-table-actions">
            <v-btn icon small color="primary" aria-label="Editar tarefa" :disabled="task.status === 'C'" @click="$emit('edit', index)"><v-icon small>{{ icons.pencil }}</v-icon></v-btn>
            <v-btn icon small color="primary" aria-label="Excluir tarefa" :disabled="task.task_id != null" @click="$emit('delete', index)"><v-icon small>{{ icons.delete }}</v-icon></v-btn>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </div>
</template>
<script>
import { mdiPencil, mdiDelete } from '@mdi/js'
export default {
  name: 'TaskList',
  props: {
    tasks: { type: Array, default: () => [] },
    metadata: { type: Object, default: () => ({}) },
    editable: { type: Boolean, default: false }
  },
  data: () => ({ icons: { pencil: mdiPencil, delete: mdiDelete } }),
  methods: {
    skillName(task, parent = false) {
      return this.$utils.getDisplayName(this.metadata.task_skills_metadata, task.skill_id, true, parent) || 'Não definida'
    },
    statusName(task) {
      return this.$utils.getDisplayName(this.metadata.task_status_metadata, task.status) || 'Não definido'
    },
    date(value) { return this.$utils.getLocalizedDate(value) || 'Não definida' }
  }
}
</script>
<style scoped>
.task-cards { display: grid; gap: 16px; }
.task-card { padding: 18px; border: 1px solid #dbe5f3; border-radius: 12px; background: #fff; }
.task-card-heading { display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: space-between; gap: 12px; }
.task-card-heading h3 { font-size: 16px; line-height: 1.5; margin: 2px 0 0; color: #0b1220; overflow-wrap: anywhere; }
.task-label, .task-dates dt { color: #526176; font-size: 12px; }
.task-description { margin: 16px 0 !important; font-size: 14px; line-height: 1.6; color: #334155; overflow-wrap: anywhere; }
.task-description p { margin: 4px 0 0; }
.task-dates { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; padding-top: 12px; border-top: 1px solid #e2e8f0; }
.task-dates dd { margin: 4px 0 0; color: #0b1220; font-size: 14px; font-weight: 600; }
.task-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
.task-empty { padding: 20px; text-align: center; color: #526176; border: 1px dashed #cbd5e1; border-radius: 12px; }
.task-table-actions { white-space: nowrap; }
.task-table { border: 1px solid #dbe5f3; border-radius: 12px; }
.task-table ::v-deep table { table-layout: auto; }
.task-table ::v-deep td { padding-top: 12px !important; padding-bottom: 12px !important; color: #334155; }
</style>
