<template>
  <div>
    <h1 v-if="topic">
      {{ currentTitle }}
    </h1>
    <h1 v-else>{{ $route.params.topicName }}</h1>

    <div v-if="error">{{ error }}</div>

    <div v-if="loading">
      loading, pls wait
      <p v-if="language === 'en'">loading, pls wait</p>
      <p v-else>Warteschleifenmusik</p>
    </div>

    <div v-else-if="topic">
      <card v-bind:key="card.id" v-for="card in this.topic.cards" :card="card" :language="language" @cardUpdated="refreshContent"></card>
      <card :createCard="true" :parentTopic="topic" @cardCreated="refreshContent" :language="language" v-if="loggedIn"></card>

      <h2 v-if="this.topic.backrefs.length">Backrefs</h2>

      <card v-bind:key="card.id" v-for="card in this.topic.backrefs" :card="card" :showTopic="true" :language="language" @cardUpdated="refreshContent"></card>
    </div>

    <div v-else-if="loggedIn">
      <p>
        Wouldn't it be nice if <strong>{{ $route.params.topicName }}</strong> existed? Create it now!
      </p>

      <p class="card">
      <input type="text" v-model="createTitleEn" placeholder="English title">
      <input type="text" v-model="createTitleDe" placeholder="Deutscher Titel">
      <button @click="doCreate()">Create</button>
      </p>
    </div>

    <div v-else>
      <p v-if="language == 'en'">
        Wouldn't it be nice if <strong>{{ $route.params.topicName }}</strong> existed?
        Tell me all about it via <a :href="contact.twitter">Twitter</a> or <a :href="contact.email">email</a>.
      </p>
      <p v-else>
        Wäre es nicht cool, wenn es <strong>{{ $route.params.topicName }}</strong> gäbe?
        Erzähl mir auf <a :href="contact.twitter">Twitter</a> oder per <a :href="contact.email">Mail</a> davon!
      </p>
      <p v-if="language == 'en'">
        Or, if you're me, <strong @click="$emit('startLogin')">log in</strong> to create this page.
      </p>
      <p v-else>
        Oder, wenn du ich bist (hi!), <strong @click="$emit('startLogin')">melde dich an</strong>, um die Seite zu erstellen.
      </p>
    </div>
  </div>
</template>

<script>
import api from '@/lib/api'
import config from '@/config'
import store from '@/store'
import Card from '@/components/Card'
export default {
  name: 'Topic',
  components: { Card },
  data () {
    return {
      topic: null,
      createTitleEn: "",
      createTitleDe: "",
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
    currentTitle () {
      let title = this.language === "en" ? this.topic.title_en : this.topic.title_de
      return title.charAt(0).toUpperCase() + title.slice(1);
    }
  },
  created () {
    store.addHistory(this.$route.params.topicName)
    this.refreshContent()
  },
  mounted () {
  },
  methods: {
    doCreate () {
      api.fetch('/api/topic/', 'POST', {slug: this.$route.params.topicName, title_en: this.createTitleEn, title_de: this.createTitleDe}).then(response => {
        if (response.id) {
          this.topic = response
        } else {
          this.error = response
        }
      })
    },
    refreshContent () {
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
  }
}
</script>

<style>
</style>
