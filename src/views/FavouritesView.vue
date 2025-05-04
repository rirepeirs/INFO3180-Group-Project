<template>
    <div class="p-4">
      <h1 class="text-2xl font-bold mb-4">Favourites</h1>
  
      <!-- Top 20 most favoured users -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-2">Top 20 Most Favoured Users</h2>
        <ul class="space-y-2">
          <li v-for="user in topFavourites" :key="user.id" class="border p-2 rounded hover:bg-gray-100">
            <router-link :to="`/users/${user.id}`" class="flex items-center space-x-4">
              <img :src="user.photo" alt="User photo" class="w-12 h-12 rounded-full object-cover" />
              <div>
                <p class="font-semibold">{{ user.name }}</p>
                <p class="text-sm text-gray-600">{{ user.favourite_count }} favourites</p>
              </div>
            </router-link>
          </li>
        </ul>
      </section>
  
      <!-- Users you favoured -->
      <section>
        <h2 class="text-xl font-semibold mb-2">Users You Favoured</h2>
        <ul class="space-y-2">
          <li v-for="user in userFavourites" :key="user.id" class="border p-2 rounded hover:bg-gray-100">
            <router-link :to="`/users/${user.id}`" class="flex items-center space-x-4">
              <img :src="user.photo" alt="User photo" class="w-12 h-12 rounded-full object-cover" />
              <div>
                <p class="font-semibold">{{ user.name }}</p>
                <p class="text-sm text-gray-600">{{ user.email }}</p>
              </div>
            </router-link>
          </li>
        </ul>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FavouritesView',
    data() {
      return {
        topFavourites: [],
        userFavourites: [],
        currentUserId: null, // Get this from session or backend
      };
    },
    async mounted() {
      try {
        // Optionally fetch current user from backend, or pass in via props/global state
        const userRes = await fetch("/api/auth/user"); // Example route to get logged-in user
        if (userRes.ok) {
          const userData = await userRes.json();
          this.currentUserId = userData.id;
  
          const [topFavRes, userFavRes] = await Promise.all([
            fetch("/api/users/favourites/20"),
            fetch(`/api/users/${userData.id}/favourites`)
          ]);
  
          if (topFavRes.ok) {
            this.topFavourites = await topFavRes.json();
          }
  
          if (userFavRes.ok) {
            const favData = await userFavRes.json();
            this.userFavourites = favData.favourites;
          }
        }
      } catch (error) {
        console.error("Error fetching favourites:", error);
      }
    },
  };
  </script>
  
  <style scoped>
  /* Optional styling tweaks here */
  </style>