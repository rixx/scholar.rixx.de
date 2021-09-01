<template>
  <h1>Introduction</h1>

    <p class="card">
      Welcome to my knowledge collection. It's a crossover of encyclopedia,
      library, nerd Twitter and learning system. It's tailored to my brain, so
      there's probably not much for you here. You can browse around for odd
      facts, or try the flashcards as the weirdest trivia quiz.
    </p>

    <p class="card">
      But since you're still reading, you're apparently one of us.  You know.
      People who could go forever with just long-form writing to sustain them.
      Read on to find out why I made this thing and how it works. At a guess,
      at least some of its moving parts would work for you, too.
    </p>
    <card text="foo"></card>

</template>
<script>
import Card from '@/components/Card'
export default {
  name: 'start',
  components: { Card },
  data () {
    return { }
  },
  computed: {
    something () {
      return []
    },
  },
  created () { },
  mounted () { },
  methods: {
  }
}
</script>

<style>
</style>
