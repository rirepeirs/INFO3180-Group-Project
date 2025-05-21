<template>
  <div class="user-details" v-if="user">
    <div class="user-header">
      <img
        :src="user.photo ? `http://localhost:8080/uploads/${user.photo}` : '/default-user.png'"
        alt="User photo"
        class="user-photo"
      />
      <div class="user-info">
        <h2 class="full-name">{{ user.name }}</h2>
        <p class="username">@{{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Date Joined:</strong> {{ formatDate(user.date_joined) }}</p>
      </div>
    </div>

    <hr class="my-4" />

    <div v-if="user.profiles?.length" class="profiles-cards-container">
      <h3 class="profile-title">Profiles</h3>
      <div class="profiles-grid">
        <ProfileCard
          v-for="profile in user.profiles"
          :key="profile.profile_id"
          :profile="profile"
        />
      </div>
    </div>
    <p v-else>No profiles available.</p>

    <div class="add-profile-container">
      <button @click="goToAddProfile" class="add-profile-btn">
        Add Profile
      </button>
    </div>

    <hr class="my-4" />

    <div v-if="favouritedProfiles.length" class="favourites-section mt-8">
      <h3 class="profile-title">Favourited Profiles</h3>
      <div class="profiles-grid">
        <ProfileCard
          v-for="profile in favouritedProfiles"
          :key="profile.profile_id"
          :profile="profile"
        />
      </div>
    </div>
    <p v-else class="no-results">No favourites found.</p>
  </div>

  <div v-else>
    <p>Loading user details...</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/axios'
import ProfileCard from '../components/ProfileCard.vue'

const user = ref(null)
const favouritedProfiles = ref([])
const router = useRouter()

onMounted(async () => {
  try {
    const meRes = await apiClient.get('/api/auth/me')
    const userId = meRes.data.id

    const userRes = await apiClient.get(`/api/users/${userId}`)
    user.value = userRes.data.user

    const favRes = await apiClient.get(`/api/favourites`)
    if (favRes.status === 200 && favRes.data.favourites) {
      favouritedProfiles.value = favRes.data.favourites
    }
  } catch (error) {
    console.error('Failed to load user details:', error)
  }
})

function formatDate(isoDate) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(isoDate).toLocaleDateString(undefined, options);
}

function goToAddProfile() {
  router.push({ name: 'AddProfile' })
}
</script>


<style scoped>

.user-details {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-header {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 2rem;
}

.user-info {
  flex: 1;
}

.user-photo {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
}

.full-name {
  font-size: 1.75rem;
  font-weight: 600;
}

.username {
  color: #555;
  margin-bottom: 1rem;
}
.profiles-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}
.add-profile-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.add-profile-btn {
  background-color: #70815b;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-profile-btn:hover {
  background-color: #c7baa2;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
} 
</style>

