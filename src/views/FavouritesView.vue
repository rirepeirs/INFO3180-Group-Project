<template>
  <div class="favourites-page container">
    <h2>Your Favourites</h2>
    <div v-if="favourites.length" class="profile-grid">
      <ProfileCard
        v-for="fav in favourites"
        :key="fav.id"
        :profile="fav"
      />
    </div>
    <p v-else class="text-gray-500">No favourites found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/axios'
import ProfileCard from '@/components/ProfileCard.vue'

const favourites = ref([])

onMounted(async () => {
  try {
    const userRes = await apiClient.get('/api/auth/me') 
    const user_id = userRes.data.id
    const res = await apiClient.get(`/api/favourites`)
    favourites.value = res.data.favourites

    favourites.value = res.data.favourites.sort((a, b) =>
      a.name.localeCompare(b.name))
  } catch (err) {
    console.error('Error loading favourites:', err)
  }
})
</script>

<style scoped>
.container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}
</style>
