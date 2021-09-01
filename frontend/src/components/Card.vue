<template>
  <div class="card">
    {{ renderedText }}
  </div>
</template>
<script>
// import moment from "moment"

export default {
  name: "card",
  data () {
    return {
    }
  },
  props: {
    card: {
      required: false,
      default: null
    },
    text: {
      required: false,
      default: null
    },
  },
  computed: {
    renderedText () {
      return this.text || this.card?.text
    },
  },
  methods: {
    foo () {
    },
  },
}
</script>
<style lang="stylus" scoped>
</style>
