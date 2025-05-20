import { ref } from 'vue'

export const isLoggedIn = ref(!!localStorage.getItem('token'))

export function login(token) {
  localStorage.setItem('token', token)
  isLoggedIn.value = true
}

export function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('userId')
  isLoggedIn.value = false
}
