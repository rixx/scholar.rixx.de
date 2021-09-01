<template>
  <header>
    <div id="search-container" :class="{active: searching}">
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
    <img src="./assets/add.svg">
    <img src="./assets/cards.svg">
    <img v-if="!user.token" @click="startLogin()" src="./assets/login.svg">
  </header>

  <main @keydown.esc="stopLogin()">
  <router-view @startLogin="startLogin" :loggedIn="loggedIn" />
    <div v-if="loggingIn" id="login-overlay" @click="stopLogin()" @keydown.esc="stopLogin()">
      <div class="card" @click.stop="" @keydown.esc="stopLogin()">
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
    stopLogin () {
      this.loggingIn = false
    },
    doLogin () {
      api.fetch('/api/login/', 'POST', {username: this.loginUser, password: this.loginPassword}).then(response => {
        if (response.token) {
          store.setUser(this.loginUser, response.token)
        }
      })
    },
    toggleSearch () {
      if (this.searching) {
        this.searching = false
      } else {
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
  width: 40px;
}
header #search-container.active {
  position: relative;
  box-shadow: 0px 0px 20px 4px rgba(0,0,0,0.10);
  border-radius: 44px;
  padding: 4px;
  display: flex;
  width: 300px;
}
header #search-container.active img {
  width: 28px;
  margin-left: 12px;
  margin-right: 8px;
}
header #search-container.active input {
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
#login-overlay {
  z-index: 1000;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.7);
}
#login-overlay .card {
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
#login-overlay input {
  width: 50%;
  margin: 15px auto;
}
</style>
