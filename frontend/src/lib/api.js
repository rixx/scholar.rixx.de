// import Vue from 'vue'

import store from '@/store'

const api = {
  baseUrl: process.env.VUE_APP_API_URL,
  fetch (url, method, body, options = { headers: {} }) {
    const user = store.getUser()
    const headers = {
        'Content-Type': 'application/json',
        Authorization: (user.token) ? 'Token ' + user.token : null,
        ...options.headers
      }
    return fetch(this.baseUrl + url, {
      method,
      body: JSON.stringify(body),
      headers,
    }).then((response) => {
      return response.json()
    }).then((response) => {
      return response
    }).catch((response) => {
      return Promise.reject(response.error || response)
    })
  }
}
export default api
