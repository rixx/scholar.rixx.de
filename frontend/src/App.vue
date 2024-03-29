<template>
  <select id="language" v-model="language" @change="updateLanguage()">
    <option value="en">English</option>
    <option value="de">Deutsch</option>
  </select>
  <header>
    <div id="search-container" class="header-container" :class="{active: searching}">
      <img src="./assets/search.svg" @click="toggleSearch()">
      <input v-if="searching" v-model="searchTerm" @keydown.esc="toggleSearch()" @input="updateSearch()">
      <div v-if="searching && searchResults.length" id="search-results">
        <template v-for="result in searchResults" v-bind:key="result.id">
          <router-link v-if="result.type === 'topic'" :to="{ name: 'Topic', params: { topicName: language === 'en' ? result.title_en : result.title_de } }" @click="searching = false">
            <strong>Topic: </strong>
            <span v-if="language == 'en'">{{ result.title_en }}</span>
            <span v-else>{{ result.title_de }}</span>
          </router-link>
          <router-link v-else-if="result.type === 'source'" :to="{ name: 'Source', params: { sourceId: result.id } }" @click="searching = false">
            <strong>Source: </strong> {{ result.title }}
          </router-link>
          <router-link v-else-if="result.type === 'tag'" :to="{ name: 'Tag', params: { tagName: result.name } }" @click="searching = false">
            <strong>Tag: </strong> {{ result.name }}
          </router-link>
        </template>
      </div>
    </div>
    <div id="add-container" class="header-container" :class="{active: addMenu}" v-if="user.token">
      <img src="./assets/add.svg" @click="toggleAddMenu()">
      <div id="add-menu" v-if="addMenu">
        <div @click="adding = 'topic'">
          <span class="letter">T</span>
          <span class="word">New topic</span>
        </div>
        <div @click="adding = 'source'">
          <span class="letter">S</span>
          <span class="word">New source</span>
        </div>
      </div>
    </div>
    <router-link :to="{ name: 'TopicList' }">
      <img src="./assets/cards.svg">
    </router-link>
    <img v-if="!user.token" @click="startLogin()" src="./assets/login.svg">
  </header>

  <main>
    <router-view @startLogin="startLogin" :loggedIn="loggedIn" v-slot="{ Component, route }">
      <component :is="Component" :key="route.path" :language="language" />
    </router-view>

    <div v-if="loggingIn || adding " id="overlay" @click="stopOverlay()" @keydown.esc="stopOverlay()">
      <div class="card" @click.stop="" @keydown.esc="stopOverlay()" v-if="loggingIn">
        <h2>Log in</h2>
        <input type="text" @keydown.enter="doLogin()" v-model="loginUser">
        <input type="password" @keydown.enter="doLogin()" v-model="loginPassword">
      </div>
      <div class="card" @click.stop="" @keydown.esc="stopOverlay()" v-else-if="adding == 'topic'">
        <h2>New topic</h2>
        <input type="text" @keydown.enter="doCreateTopic()" v-model="newTopicTitleEn" placeholder="Title (en)">
        <input type="text" @keydown.enter="doCreateTopic()" v-model="newTopicTitleDe" placeholder="Title (de)">
        <button @click="doCreateTopic()">Create</button>
      </div>
      <div class="card" @click.stop="" @keydown.esc="stopOverlay()" v-else-if="adding == 'source'">
        <h2>New source</h2>
        <input type="text" @keydown.enter="doCreateSource()" v-model="newSourceTitle" placeholder="Title">
        <input type="text" @keydown.enter="doCreateSource()" v-model="newSourceAuthor" placeholder="Author">
        <input type="text" @keydown.enter="doCreateSource()" v-model="newSourceNotesEn" placeholder="Notes (en)">
        <input type="text" @keydown.enter="doCreateSource()" v-model="newSourceNotesDe" placeholder="Notes (de)">
        <input type="text" @keydown.enter="doCreateSource()" v-model="newSourceUrl" placeholder="URL">
        <select v-model="newSourceTrust" @keydown.enter="doCreateSource()">
          <option value="5">excellent source</option>
          <option value="4">good source</option>
          <option value="3">better than 50/50 (good pop sci)</option>
          <option value="2">50/50 (pop sci)</option>
          <option value="1">probably incorrect</option>
          <option value="0">incorrect</option>
        </select>
        <button @click="doCreateSource()">Create</button>
      </div>
    </div>
  </main>
  <footer></footer>
</template>

<script>
import api from '@/lib/api'
import store from '@/store'
export default {
  name: 'App',
  data () {
    return {
      loggingIn: false,
      searching: false,
      adding: false,
      addMenu: false,
      loginUser: "",
      loginPassword: "",
      searchResults: [],
      searchTerm: "",
      newTopicTitleDe: "",
      newTopicTitleEn: "",
      newSourceTitle: "",
      newSourceAuthor: "",
      newSourceNotesEn: "",
      newSourceNotesDe: "",
      newSourceTrust: "",
      newSourceUrl: "",
      language: "",
    }
  },
  components: {
  },
  created () {
    this.language = store.getLanguage()
  },
  methods: {
    startLogin () {
      this.loggingIn = true
    },
    stopOverlay () {
      this.loggingIn = false
      this.adding = false
      this.addMenu = false
    },
    doLogin () {
      api.fetch('/api/login/', 'POST', {username: this.loginUser, password: this.loginPassword}).then(response => {
        if (response.token) {
          store.setUser(this.loginUser, response.token)
          this.stopOverlay()
        }
      })
    },
    doCreateTopic() {
      api.fetch('/api/topic/', 'POST', {title_en: this.newTopicTitleEn, title_de: this.newTopicTitleDe}).then(response => {
        if (response.id) {
          this.stopOverlay()
          this.$router.push({ name: 'Topic', params: { topicName: this.language == "en" ? this.newTopicTitleEn : this.newTopicTitleDe } })
        } else {
          this.error = response
        }
      })
    },
    doCreateSource() {
      api.fetch('/api/source/', 'POST', {title: this.newSourceTitle, author: this.newSourceAuthor, url: this.newSourceUrl, trust: this.newSourceTrust, notes_de: this.newSourceNotesDe, notes_en: this.newSourceNotesEn}).then(response => {
        if (response.id) {
          this.stopOverlay()
          this.$router.push({ name: 'Source', params: { sourceId: response.id } })
        } else {
          this.error = response
        }
      })
    },
    updateLanguage () {
      store.setLanguage(this.language)
    },
    toggleAddMenu () {
      if (this.addMenu) {
        this.addMenu = false
      } else {
        this.stopOverlay()
        this.addMenu = true
      }
    },
    toggleSearch () {
      if (this.searching) {
        this.searching = false
      } else {
        this.stopOverlay()
        this.searching = true
        window.setTimeout(() => document.querySelector("#search-container input").focus(), 5)
      }
    },
    updateSearch () {
      if (this.searchTerm.length == 0) return
      const params = new URLSearchParams({q: this.searchTerm, short: true}).toString()
      api.fetch(`/api/search/?${params}`, 'GET').then(response => {
        if (response.result) {
          this.searchResults = response.result
        }
      })
    },
  },
  computed: {
    user () {
      return store.getUser()
    },
    loggedIn () {
      return this.user && this.user?.token
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #294370;
}
header {
  position: fixed;
  display: flex;
  flex-direction: column;
  width: 40px;
  top: 64px;
  left: 20px;
}
header > * {
  margin-bottom: 16px;
  cursor: pointer;
}
header img {
  height: 42px;
}
header .header-container.active {
  position: relative;
  box-shadow: 0px 0px 20px 4px rgba(0,0,0,0.10);
  border-radius: 44px;
  padding: 4px;
  display: flex;
  width: 300px;
  height: 40px;
}
header .header-container.active img {
  width: 28px;
  margin-left: 12px;
  margin-right: 8px;
}
header .header-container.active input {
  border-radius: 44px;
  margin: 0 4px;
  width: 100%;
  padding-left: 16px;
}
#search-results {
  position: absolute;
  top: 50px;
  right: 24px;
  width: 220px;
  background: white;
  display: flex;
  flex-direction: column;
}
#search-results > a {
  padding: 16px;
  border: 1px solid #ddd;
  border-top: none;
  text-decoration: none;
  color: #294370;
}
#search-results > a:hover {
  background-color: #f4f4f4;
}
#add-menu {
  display: flex;
  width: 100%;
  justify-content: space-around;
}
#add-menu > div {
  display: flex;
  flex-direction: column;
  align-items: center;
}
#add-menu .letter {
  font-size: 24px;
}
#add-menu .word {
  font-size: 11px;
}
main {
  max-width: 800px;
  margin: 0 auto;
}
main h1 {
  text-align: center;
  margin: 160px 0 90px 0;
}
main p {
  line-height: 1.9;
  font-size: 18px;
  text-align: left;
}
#overlay {
  z-index: 1000;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.7);
}
#overlay .card {
  width: 500px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 20vh;
  display: flex;
  flex-direction: column;
  padding: 32px 64px;
  text-align: center;
}
input, input:focus, select, textarea {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: 18px;
  padding: 8px;
  border: 1px solid #ccc;
  outline: none;
}
button {
  margin: 40px 0;
  padding: 12px 24px;
  font-size: 18px;
  border-top-right-radius: 24px;
  border-bottom-left-radius: 24px;
  box-shadow: 0px 0px 20px 4px rgba(0,0,0,0.10);
  background: white;
  border: 2px solid #294370;
  cursor: pointer;
}
#overlay input, #overlay select, #overlay button {
  width: 70%;
  margin: 15px auto;
}
#overlay input {
  width: calc(70% - 20px);
}
</style>
