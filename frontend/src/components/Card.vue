<template>
  <div :class="{card: true, create: createCard}">
    <div v-if="createCard">+</div>
    <div v-else>
    {{ renderedText }}
    </div>
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
    createCard: {
      required: false,
      default: false
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
<style>
.card {
  margin: 40px 0;
  padding: 16px 28px;
  border-top-right-radius: 44px;
  border-bottom-left-radius: 44px;
  box-shadow: 0px 0px 20px 4px rgba(0,0,0,0.10);
  background: white;
}
.card:hover {
  box-shadow: 0px 0px 20px 7px rgba(0,0,0,0.12);
}
.card.create {
  cursor: pointer;
}
.card.create > div {
  font-size: 32px;
  text-align: center;
  font-weight: bold;
}
</style>
