import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    token: '',
    isLoggedIn: false
  }),
  actions: {
    login(token: string, username: string) {
      this.token = token
      this.username = username
      this.isLoggedIn = true
      localStorage.setItem('token', token)
      localStorage.setItem('username', username)
    },
    logout() {
      this.token = ''
      this.username = ''
      this.isLoggedIn = false
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    },
    init() {
      const token = localStorage.getItem('token')
      const username = localStorage.getItem('username')
      if (token && username) {
        this.token = token
        this.username = username
        this.isLoggedIn = true
      }
    }
  }
})
