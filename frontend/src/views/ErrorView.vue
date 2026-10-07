<template>
  <v-container class="welcome-page text-center">
    <v-card class="welcome-card pa-8" max-width="520">
      <v-icon size="64" color="primary">{{ syncIcon }}</v-icon>
      <h1 class="welcome-title mt-6 mb-4">Bem-vindo ao DevSync</h1>
      <p>Acompanhe reuniões, metas e o desenvolvimento da sua equipe em um só lugar.</p>
      <v-btn color="primary" large href="/devsync/login/?next=/devsync/">Entrar</v-btn>
      <p class="text-caption mt-6 mb-0">O acesso depende de um usuário cadastrado pelo administrador.</p>
    </v-card>
  </v-container>
</template>
<script>
import { mdiSync } from '@mdi/js'
export default {
  name: 'ErrorView',
  data: () => ({ syncIcon: mdiSync }),
  mounted() { this.$store.commit('setTemplateRendered', true) }
}
</script>
<style scoped>
.welcome-page {
  min-height: calc(100vh - 100px);
  min-height: calc(100dvh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.welcome-card { width: 100%; }
.welcome-title { font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 500; line-height: 1.3; }
</style>
