import { reactive } from 'vue'

const store = {
  debug: true,
  user: reactive({name: null, token: null}),
  history: reactive([]),

  setUser(name, token) {
    if (this.debug) console.log('[store] setUser triggered with', name, token)
    this.user.name = name
    this.user.token = token
    window.localStorage.setItem("scholarApiUser", name)
    window.localStorage.setItem("scholarApiToken", token)
  },
  clearUser() {
    if (this.debug) console.log('[store] credentials cleared')
    this.user = {email: null, token: null}
    window.localStorage.removeItem("scholarApiToken")
  },
  getUser() {
    if (this.user.name || this.user.token) {
      return this.user
    }
    this.user.name = window.localStorage.getItem("scholarApiUser")
    this.user.token = window.localStorage.getItem("scholarApiToken")
    return this.user
  },
  setHistory(history) {
    if (this.debug) console.log('[store] setHistory triggered with', history)
    this.history = history
  },
  addHistory(page) {
    if (this.debug) console.log('[store] addHistory triggered with', page)
    this.history.push(page)
    if (this.debug) console.log('[store] history is now', this.history)
  },
}
export default store
