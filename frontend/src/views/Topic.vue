<template>
  <div>
    <h1 v-if="topic">{{ topic.title }}</h1>
    <h1 v-else>{{ $route.params.topicName }}</h1>
    <div v-if="topic">
      TODO: render cards
    </div>
    <div v-else-if="loggedIn">
      TODO create topic
    </div>
    <div v-else>
    <p>
      Wouldn't it be nice if <strong>{{ $route.params.topicName }}</strong> existed?
      Tell me all about it via <a :href="contact.twitter">Twitter</a> or <a :href="contact.email">email</a>.
    </p>
    <p>
      Or, if you're me, <a @click="$emit('startLogin')">log in</a> to create this page.
    </p>
    </div>
  </div>
</template>

<script>
// import store from '@/store'
import config from '@/config'
export default {
  name: 'Topic',
  components: { },
  data () {
    return {
      topic: null
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
    console.log("adding to history")
    // store.addHistory(this.$route.params.topicName)
  },

  mounted () {

  },
  methods: {
    somethingMethod (foo) {
      return foo
    },
  }
}
</script>

<style>
</style>
