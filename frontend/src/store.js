import { reactive } from 'vue'

const store = {
  debug: true,
  user: reactive({email: null, token: null}),
  history: reactive([]),

  setUser(user) {
    if (this.debug) console.log('[store] setUser triggered with', user)
    this.store.user = user
  },
  clearUser() {
    if (this.debug) console.log('[store] credentials cleared')
    this.store.user = {email: null, token: null}
  },
  setHistory(history) {
    if (this.debug) console.log('[store] setHistory triggered with', history)
    this.store.history = history
  },
  addHistory(page) {
    if (this.debug) console.log('[store] addHistory triggered with', page)
    this.store.history.push(page)
  },
}
export default store
