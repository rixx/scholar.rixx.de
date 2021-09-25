<template>
  <div class="card" @mouseover="hovering = true" @mouseleave="hovering = false">
    <template v-if="creating || editing">
      <textarea class="resize" v-model="createTextEn" placeholder="Text (en)" @input="resizeTextarea" rows=4></textarea>
      <textarea class="resize" v-model="createTextDe" placeholder="Text (de)" @input="resizeTextarea" rows=4></textarea>
      <select v-model="createTopic" v-if="!parentTopic || editing">
        <option v-for="topic in availableTopics" v-bind:key="topic.id" :value="topic.id">
          <span v-if="language == 'en'">{{ topic.title_en }}</span>
          <span v-else>{{ topic.title_de }}</span>
        </option>
      </select>
      <select v-model="createSources" v-if="!parentSource || editing" multiple>
        <option v-for="source in availableSources" v-bind:key="source.id" :value="source.id">{{ source.title }}</option>
      </select>
      <button v-if="creating" @click="doUpdate()">create</button>
      <button v-if="editing" @click="doUpdate()">save</button>
    </template>
    <template v-else-if="createCard"><div @click="creating = true" class="create-placeholder">+</div></template>
    <template v-else>
      <div v-html="renderedText" @click="handleLink"></div>
      <p v-if="card.sources && card.sources.length" class="sources">
        (<span v-for="source in card.sources" v-bind:key="source.id">
          <router-link :to="{ name: 'Source', params: { sourceId: source.id } }">
          {{ source.title }}
          </router-link>
        </span>)
      </p>
      <div v-if="showTopic && card.topic" class="topic">
        <i>
          in
          <router-link :to="{ name: 'Topic', params: { topicName: language === 'en' ? card.topic.title_en : card.topic.title_de } }">
            <span v-if="language == 'en'">{{ card.topic.title_en }}</span>
            <span v-else>{{ card.topic.title_de }}</span>
          </router-link></i><br>
      </div>
    </template>
    <div class="card-tools" v-if="card && card.id && (hovering | editing)">
      <div v-if="!editing" class="card-tool" @click="startEditing">edit</div>
      <div v-if="editing" class="card-tool" @click="stopEditing">stop</div>
      <div class="card-tool">delete</div>
    </div>
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
      hovering: false,
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
    doUpdate () {
      const data = {text_en: this.createTextEn, text_de: this.createTextDe, topic: this.createTopic, sources: this.createSources}
      let url = '/api/card/'
      let method = 'POST'
      let creating = true
      if (this.card && this.card.id) {
        data.id = this.card.id
        url += this.card.id + "/"
        method = 'PUT'
        creating = false
      }
      api.fetch(url, method, data).then(response => {
        if (response.id) {
          this.loading = false
          this.createTextEn = ""
          this.createTextDe = ""
          if (creating) {
            this.$emit('cardCreated', response)
          } else {
            this.stopEditing()
            this.$emit('cardUpdated', response)
          }
        }
      }).catch(() => {
        this.loading = false
      })
    },
    startEditing () {
      if (!this.availableTopics.length) {
        api.fetch('/api/topic/', 'GET').then(response => this.availableTopics = response)
      }
      if (!this.availableSources.length) {
        api.fetch('/api/source/', 'GET').then(response => this.availableSources = response)
      }
      this.createTextDe = this.card.text_de
      this.createTextEn = this.card.text_en
      this.createTopic = this.card.topic.id
      this.createSources = this.card.sources.map(s => s.id)
      this.editing = true
      window.setTimeout(() => document.querySelectorAll("textarea.resize").forEach(ta => this.resizeTextarea(ta)), 5)
    },
    stopEditing () {
      this.createTextDe = ""
      this.createTextEn = ""
      this.createTopic = ""
      this.createSources = ""
      this.editing = false
    },
    handleLink (event) {
      // via https://dennisreimann.de/articles/delegating-html-links-to-vue-router.html
      let { target } = event
      while (target && target.tagName !== 'A' && target.parentNode) target = target.parentNode
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
      let target = null
      if (event.tagName && event.tagName === 'TEXTAREA') {
        target = event
      } else {
        let { target } = event
        while (target && target.tagName !== 'TEXTAREA' && target.parentNode) target = target.parentNode
      }
      target.style.overflow = 'hidden';
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
  position: relative;
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
.card .topic {
  text-align: right
}
.card .sources, .card .sources a {
  text-decoration: none;
  color: #aaa;
  font-size: 14px;
  line-height: 1;
}
.card .card-tools {
  position: absolute;
  left: 100%;
  top: 16px;
  width: 80px;
  padding: 24px;
  display: flex;
}
.card .card-tool {
  margin: 0 8px;
  cursor: pointer;
}
</style>
