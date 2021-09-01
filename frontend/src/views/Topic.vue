<template>
  <div>
    <h1 v-if="topic">{{ topic.title }}</h1>
    <h1 v-else>{{ $route.params.topicName }}</h1>

    <div v-if="error">{{ error }}</div>

    <div v-if="loading">
      loading, pls wait
    </div>
    <div v-else-if="topic">
      TODO: render cards
    </div>

    <div v-else-if="loggedIn">
      <p>
        Wouldn't it be nice if <strong>{{ $route.params.topicName }}</strong> existed? Create it now!
      </p>

      <p>
      <select v-model="createLanguage">
        <option value="de">German</option>
        <option value="en">English</option>
      </select>
      <button @click="doCreate()">Create</button>
      </p>
    </div>

    <div v-else>
      <p>
        Wouldn't it be nice if <strong>{{ $route.params.topicName }}</strong> existed?
        Tell me all about it via <a :href="contact.twitter">Twitter</a> or <a :href="contact.email">email</a>.
      </p>
      <p>
        Or, if you're me, <strong @click="$emit('startLogin')">log in</strong> to create this page.
      </p>
    </div>
  </div>
</template>

<script>
// import store from '@/store'
import api from '@/lib/api'
import config from '@/config'
import store from '@/store'
export default {
  name: 'Topic',
  components: { },
  data () {
    return {
      topic: null,
      createLanguage: "",
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
    store.addHistory(this.$route.params.topicName)
    api.fetch(`/api/topic/${this.$route.params.topicName}`, 'GET').then(response => {
      if (response.id) {
        this.topic = response
      }
      this.loading = false
    }).catch(() => {
      this.topic = null
      this.loading = false
    })
  },
  mounted () {
  },
  methods: {
    doCreate () {
      api.fetch('/api/topic/', 'POST', {title: this.$route.params.topicName, language: this.createLanguage}).then(response => {
        if (response.id) {
          this.topic = response
        } else {
          this.error = response
        }
      })
    },
  }
}
</script>

<style>
</style>
