<template>
  <header>
    <img src="./assets/search.svg">
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
      loginUser: "",
      loginPassword: "",
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
    }
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
header img {
  margin-bottom: 16px;
  cursor: pointer;
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
#login-overlay input {
  width: 50%;
  font-size: 18px;
  margin: 15px auto;
  padding: 8px;
}
</style>
