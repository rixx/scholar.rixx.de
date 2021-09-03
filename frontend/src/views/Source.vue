<template>
  <div>
    <h1 v-if="source">{{ source.title }}</h1>
    <h1 v-else>{{ $route.params.sourceId }}</h1>

    <div v-if="error">{{ error }}</div>

    <div v-if="loading">
      loading, pls wait
    </div>
    <div v-else-if="source">
      <card v-bind:key="card.id" v-for="card in this.source.cards" :card="card" :showTopic="true"></card>
      <card :createCard="true" :parentSource="source" @cardCreate="refreshContent"></card>
    </div>
    <div v-else>
      <p>Source not found.</p>
    </div>
  </div>
</template>

<script>
// import store from '@/store'
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
