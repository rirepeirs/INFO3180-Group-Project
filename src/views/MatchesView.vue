<template>
  <div class="matches-page container">
    <h2>Match Results</h2>

    <div v-if="matches.length" class="profile-grid">
      <ProfileCard
        v-for="match in matches"
        :key="match.id"
        :profile="match"
      />
    </div>
    <p v-else class="text-gray-500">No matches found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/axios'
import ProfileCard from '@/components/ProfileCard.vue'

const route = useRoute()
const matches = ref([])

onMounted(async () => {
  const profileId = route.query.profile_id
  if (!profileId) return

  try {
    const res = await apiClient.get(`/api/profiles/matches/${profileId}`)
    matches.value = res.data
  } catch (err) {
    console.error('Failed to load matches:', err)
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