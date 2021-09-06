<template>
  <div class="card">
    <template v-if="creating">
      <textarea v-model="createTextEn" placeholder="Text (en)" @input="resizeTextarea" rows=4></textarea>
      <textarea v-model="createTextDe" placeholder="Text (de)" @input="resizeTextarea" rows=4></textarea>
      <select v-model="createTopic" v-if="!parentTopic">
        <option v-for="topic in availableTopics" v-bind:key="topic.id" :value="topic.id">{{ topic.title }}</option>
      </select>
      <select v-model="createSources" v-if="!parentSource" multiple>
        <option v-for="source in availableSources" v-bind:key="source.id" :value="source.id">{{ source.title }}</option>
      </select>
      <button @click="doCreate()">create</button>
    </template>
    <template v-else-if="createCard"><div @click="creating = true" class="create-placeholder">+</div></template>
    <template v-else>
      <div v-html="renderedText" @click="handleLink"></div>
      <div v-if="showTopic && card.topic">{{ card.topic }}</div>
    </template>
  </div>
</template>
<script>
// import moment from "moment"
import renderMarkdown from '@/lib/markdown'
import api from '@/lib/api'
export default {
  name: "card",
  data () {
    return {
      creating: false,
      editing: false,
      createTextDe: "",
      createTextEn: "",
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
    language: {
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
    showTopic: {
      required: false,
      default: false
    },
  },
  computed: {
    baseText () {
      return this.text || (this.language == "en" ? this.card.text_en : this.card.text_de)

    },
    renderedText () {
      return renderMarkdown(this.baseText)
    },
  },
  created () {
    if (this.parentSource) {
      this.createSources.push(this.parentSource.id)
    }
    if (this.parentTopic) {
      this.createTopic = this.parentTopic.id
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
      const data = {text_en: this.createTextEn, text_de: this.createTextDe, topic: this.createTopic, sources: this.createSources}
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
    handleLink (event) {
      // via https://dennisreimann.de/articles/delegating-html-links-to-vue-router.html
      let { target } = event
      while (target && target.tagName !== 'A') target = target.parentNode
      // handle only links that occur inside the component and do not reference external resources
      if (target && target.matches(".dynamic-content a:not([href*='://'])") && target.href) {
        // some sanity checks taken from vue-router:
        // https://github.com/vuejs/vue-router/blob/dev/src/components/link.js#L106
        const { altKey, ctrlKey, metaKey, shiftKey, button, defaultPrevented } = event
        // don't handle with control keys
        if (metaKey || altKey || ctrlKey || shiftKey) return
        // don't handle when preventDefault called
        if (defaultPrevented) return
        // don't handle right clicks
        if (button !== undefined && button !== 0) return
        // don't handle if `target="_blank"`
        if (target && target.getAttribute) {
          const linkTarget = target.getAttribute('target')
          if (/\b_blank\b/i.test(linkTarget)) return
        }
        // don't handle same page links/anchors
        const url = new URL(target.href)
        const to = url.pathname
        if (window.location.pathname !== to && event.preventDefault) {
          event.preventDefault()
          this.$router.push(to)
        }
      }
    },
    resizeTextarea (event) {
      let { target } = event
      while (target && target.tagName !== 'TEXTAREA') target = target.parentNode
      target.style.overflow = 'hidden';
      console.log(target)
      target.style.height = target.scrollHeight - 16 + 'px'
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
