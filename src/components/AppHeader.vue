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
            <li class="nav-item">
              <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/about" class="nav-link" :class="{ active: $route.path === '/about' }">About</RouterLink>
            </li>

            <!-- Additional navigation items for logged-in users -->
            <template v-if="isLoggedIn">
              <li class="nav-item">
                <RouterLink to="/profiles" class="nav-link" :class="{ active: $route.path === '/profiles' }">Search</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink to="/myprofile" class="nav-link" :class="{ active: $route.path === '/myprofile' }">My Profile</RouterLink>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="reportsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Reports
                </a>
                <ul class="dropdown-menu" aria-labelledby="reportsDropdown">
                  <li><RouterLink to="/profiles/favourites" class="dropdown-item">My Favourites</RouterLink></li>
                  <li><RouterLink to="/profiles/favoured" class="dropdown-item">Most Favoured Users</RouterLink></li>
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

<script setup>
import { RouterLink } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'; // Optional: to programmatically navigate after logout

// This should be replaced with your actual authentication state management
const isLoggedIn = ref(false);

// Check authentication status on component mount
onMounted(() => {
  // Check if the user is logged in (e.g., checking for a token in localStorage or using a Vuex store)
  const token = localStorage.getItem('authToken'); // Assuming you store token in localStorage
  isLoggedIn.value = !!token; // If token exists, user is logged in
});

// Logout function
const logout = () => {
  // Perform logout actions (e.g., remove token, reset state, etc.)
  localStorage.removeItem('authToken'); // Remove token from localStorage
  isLoggedIn.value = false; // Update login state

  // Optionally, redirect the user to the home or login page
  const router = useRouter();
  router.push('/login');
};
</script>

<style scoped>
/* Your CSS styling */
</style>
