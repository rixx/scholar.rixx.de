<template>
  <div>
    <h1 v-if="source">{{ source.title }}</h1>
    <h1 v-else>{{ $route.params.sourceId }}</h1>

    <div v-if="error">{{ error }}</div>

    <div v-if="loading">
      loading, pls wait
    </div>
    <div v-else-if="source">
      TODO: render cards
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
export default {
  name: 'Source',
  components: { },
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
  },
  mounted () {
  },
  methods: {
  }
}
</script>

<style>
</style>
