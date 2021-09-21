<template>
  <div>
    <div v-if="loading">
      loading, pls wait
      <p v-if="language === 'en'">loading, pls wait</p>
      <p v-else>Warteschleifenmusik</p>
    </div>
    <div v-else>
      <ul>
        <li v-for="topic in sortedTopics" v-bind:key="topic.id">
          <router-link :to="{ name: 'Topic', params: { topicName: language === 'en' ? topic.title_en : topic.title_de } }">
            <span v-if="language == 'en'">{{ topic.title_en }}</span>
            <span v-else>{{ topic.title_de }}</span>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api from '@/lib/api'
import store from '@/store'
export default {
  name: 'TopicList',
  components: { },
  data () {
    return {
      loading: true,
      topics: []
    }
  },
  props: {
    loggedIn: {
      required: false,
      default: false
    },
  },
  computed: {
    language () {
      return store.user.language
    },
    sortedTopics () {
      if (!this.topics.length) return []
      if (this.language === "en") {
        return [...this.topics].sort((a, b) => {
            var x = a.title_en.toLowerCase();
            var y = b.title_en.toLowerCase();
            return x < y ? -1 : x > y ? 1 : 0;
        })
      }
        return [...this.topics].sort((a, b) => {
            var x = a.title_de.toLowerCase();
            var y = b.title_de.toLowerCase();
            return x < y ? -1 : x > y ? 1 : 0;
        })
    }
  },
  mounted () {
    api.fetch('/api/topic/', 'GET').then(response => {
      this.topics = response
      this.loading = false
    })
  },
  created () { },
  methods: {
    somethingMethod (foo) {
      return foo
    },
  }
}
</script>

<style>
</style>

