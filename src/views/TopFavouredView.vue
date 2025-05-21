<template>
  <div class="top-favoured-page container">
    <h2>Top 20 Most Favoured Users</h2>

    <div v-if="users.length" class="profile-grid">
      <ProfileCard
        v-for="user in users"
        :key="user.id"
        :profile="{ user:user }"
      />
    </div>
    <p v-else class="text-gray-500">No favourites found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/axios'
import ProfileCard from '@/components/ProfileCard.vue'

const users = ref([])

onMounted(async () => {
  try {
    const res = await apiClient.get('/api/users/favourites/20')
    users.value = res.data
  } catch (err) {
    console.error('Error loading top favourites:', err)
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
