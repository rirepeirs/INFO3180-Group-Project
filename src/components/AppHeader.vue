<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">JAM-DATE</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <!-- Left side navigation items -->
          <ul class="navbar-nav me-auto">
            <li class="nav-item" v-if="!isLoggedIn">
              <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/about" class="nav-link" :class="{ active: $route.path === '/about' }">About</RouterLink>
            </li>

            <!--navigation items for logged-in users -->
            <template v-if="isLoggedIn">
              <li class="nav-item">
                <RouterLink to="/search" class="nav-link" :class="{ active: $route.path === '/search' }">Search</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink :to="`/users/${userId}`" class="nav-link" :class="{ active: $route.path.startsWith('/users')}">My Profile</RouterLink>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="reportsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Reports
                </a>
                <ul class="dropdown-menu" aria-labelledby="reportsDropdown">
                  <li><RouterLink to="/profiles/yourfavourites" class="dropdown-item">My Favourites</RouterLink></li>
                  <li><RouterLink to="/top-favoured" class="dropdown-item">Most Favoured Users</RouterLink></li>
                </ul>
              </li>
            </template>
          </ul>

          <!-- Right side navigation items -->
          <ul class="navbar-nav">
            <li class="nav-item" v-if="!isLoggedIn">
              <RouterLink to="/login" class="nav-link">Login</RouterLink>
            </li>
            <li class="nav-item" v-else>
              <a href="#" class="nav-link" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup >
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { isLoggedIn, logout as doLogout } from '@/auth'
import { ref, onMounted } from 'vue'

const router = useRouter()
const userId = ref(localStorage.getItem('userId'));

onMounted(() => {
  const storedId = localStorage.getItem('userId')
  if (storedId) {
    userId.value = storedId
  }
})

const logout = () => {
  doLogout()
  router.push('/login')
}
</script>

<style scoped>
/* Your CSS styling */
</style>
