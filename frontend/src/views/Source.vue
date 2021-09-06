<template>
  <div>
    <h1 v-if="source">{{ source.title }}</h1>
    <h1 v-else>{{ $route.params.sourceId }}</h1>
    <h4 v-if="source && source.author">{{ source.author }}</h4>

    <div v-if="error">{{ error }}</div>

    <div v-if="loading">
      loading, pls wait
      <p v-if="language === 'en'">loading, pls wait</p>
      <p v-else>Warteschleifenmusik</p>
    </div>
    <div v-else-if="source">
      <card v-bind:key="card.id" v-for="card in this.source.cards" :card="card" :showTopic="true" :language="language"></card>
      <card :createCard="true" :parentSource="source" @cardCreate="refreshContent" :language="language" v-if="loggedIn"></card>
    </div>
    <div v-else>
      <p v-if="language === 'en'">Source not found.</p>
      <p v-else>Quelle nicht gefunden.</p>
    </div>
  </div>
</template>

<script>
import api from '@/lib/api'
import config from '@/config'
import store from '@/store'
import Card from '@/components/Card'
export default {
  name: 'Source',
  components: { Card },
  data () {
    return {
      source: null,
      error: "",
      loading: true
    }
  },
  props: {
    loggedIn: {
      required: false,
      default: false
    },
  },
  computed: {
    contact () {
      return config.contact
    },
    language () {
      return store.user.language
    },
  },
  created () {
    this.refreshContent()
  },
  mounted () {
  },
  methods: {
    refreshContent () {
      api.fetch(`/api/source/${this.$route.params.sourceId}`, 'GET').then(response => {
        if (response.id) {
          this.source = response
          store.addHistory({route: this.$route, title: this.source.title})
        }
        this.loading = false
      }).catch(() => {
        this.source = null
        this.loading = false
      })

    }
  }
}
</script>

<style>
</style>
