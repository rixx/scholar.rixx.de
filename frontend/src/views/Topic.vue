<template>
  <div>
    hi {{ $route.params.topicName }}
  </div>
</template>

<script>
// import store from '@/store'
export default {
  name: 'Topic',
  components: { },
  data () {
    return { }
  },
  computed: {
    something () {
      return true
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
