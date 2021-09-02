<template>
  <header>
    <div id="search-container" class="header-container" :class="{active: searching}">
      <img src="./assets/search.svg" @click="toggleSearch()">
      <input v-if="searching" v-model="searchTerm" @keydown.esc="toggleSearch()" @input="updateSearch()">
      <div v-if="searching && searchResults.length" id="search-results">
        <template v-for="result in searchResults" v-bind:key="result.id">
          <a v-if="result.type === 'topic'" :href="'/t/' + result.title">
            <strong>Topic: </strong> {{ result.title }}
          </a>
          <a v-else-if="result.type === 'source'" :href="'/source/' + result.id">
            <strong>Source: </strong> {{ result.title }}
          </a>
          <a v-else-if="result.type === 'tag'" :href="'/tag/' + result.name">
            <strong>Tag: </strong> {{ result.name }}
          </a>
        </template>
      </div>
    </div>
    <div id="add-container" class="header-container" :class="{active: addMenu}">
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
    <img src="./assets/cards.svg">
    <img v-if="!user.token" @click="startLogin()" src="./assets/login.svg">
  </header>

  <main>
    <router-view @startLogin="startLogin" :loggedIn="loggedIn" />
    <div v-if="loggingIn || adding " id="overlay" @click="stopOverlay()" @keydown.esc="stopOverlay()">
      <div class="card" @click.stop="" @keydown.esc="stopOverlay()" v-if="loggingIn">
        <h2>Log in</h2>
        <input type="text" @keydown.enter="doLogin()" v-model="loginUser">
        <input type="password" @keydown.enter="doLogin()" v-model="loginPassword">
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
    }
  },
  components: {
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
        }
      })
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
  position: absolute;
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
  margin-top: 40vh;
  display: flex;
  flex-direction: column;
  padding: 32px 64px;
  text-align: center;
}
input, input:focus {
  font-size: 18px;
  padding: 8px;
  border: 1px solid #ccc;
  outline: none;
}
#overlay input {
  width: 50%;
  margin: 15px auto;
}
</style>
