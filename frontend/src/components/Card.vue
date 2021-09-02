<template>
  <div class="card">
    <template v-if="creating">
      <textarea v-model="createText"></textarea>
      <select v-model="createTopic">
        <option v-for="topic in availableTopics" v-bind:key="topic.id" :value="topic.id">{{ topic.title }}</option>
      </select>
      <button @click="doCreate()">create</button>
    </template>
    <template v-else-if="createCard"><div @click="creating = true" class="create-placeholder">+</div></template>
    <template v-else>
    {{ renderedText }}
    </template>
  </div>
</template>
<script>
// import moment from "moment"

import api from '@/lib/api'
export default {
  name: "card",
  data () {
    return {
      creating: false,
      editing: false,
      createText: "",
      createSources: [],
      createTopic: null,
      availableSources: [],
      availableTopics: [],
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
    parentSource: {
      required: false,
      default: false
    },
    parentTopic: {
      required: false,
      default: false
    },
  },
  computed: {
    renderedText () {
      return this.text || this.card?.text
    },
  },
  created () {
    if (this.parentSource) {
      this.createSources.push(this.parentSource)
    }
    if (this.parentTopic) {
      this.createTopic = this.parentTopic
    }
  },
  mounted () {
    if (this.createCard) {
      if (!this.parentTopic) {
        api.fetch('/api/topic/', 'GET').then(response => this.availableTopics = response)
      }
      if (!this.parentSource) {
        api.fetch('/api/source/', 'GET').then(response => this.availableSources = response)
      }
    }
  },
  methods: {
    doCreate () {
      const data = {text: this.createText, topic: this.createTopic, sources: this.createSources.map(e => e.id)}
      api.fetch(`/api/card/`, 'POST', data).then(response => {
        if (response.id) {
          this.source = response
        }
        this.loading = false
        this.$emit('cardCreated')
      }).catch(() => {
        this.source = null
        this.loading = false
      })
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
  display: flex;
  flex-direction: column;
}
.card:hover {
  box-shadow: 0px 0px 20px 7px rgba(0,0,0,0.12);
}
.card .create-placeholder {
  cursor: pointer;
}
.card .create-placeholder {
  font-size: 32px;
  text-align: center;
  font-weight: bold;
}
.card textarea {
  margin-bottom: 24px;
  padding: 8px 16px;
  line-height: 1.8;
}
</style>
