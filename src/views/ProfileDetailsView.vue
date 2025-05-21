<template>
  <div class="profile-details" v-if="profile && currentUser">
    <div class="flex items-center gap-4 mb-6">
      <img :src="`http://localhost:8080/uploads/${currentUser.photo}`" alt="Profile Photo" class="w-24 h-24 rounded-full object-cover" />
      <div>
        <h2 class="text-xl font-semibold">{{ currentUser.name }}</h2>
        <p class="text-gray-500">@{{ currentUser.username }}</p>
      </div>
    </div>

    <hr class="my-4" />
  
      <p><strong>Description:</strong> {{ profile.description }}</p>
      <p><strong>Biography:</strong> {{ profile.biography }}</p>
      <p><strong>Parish:</strong> {{ profile.parish }}</p>
      <p><strong>Sex:</strong> {{ profile.sex }}</p>
      <p><strong>Race:</strong> {{ profile.race }}</p>
      <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
      <p><strong>Height:</strong> {{ profile.height }} m</p>
      <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
      <p><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
      <p><strong>Favourite Subject:</strong> {{ profile.fav_school_subject }}</p>
      <p><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
      <p><strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
      <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
    
      <div>
        <button v-if="viewerId !== profile.user_id_fk" @click="toggleFavourite" class="btn">
          {{ isFavourited ? 'Favourited' : 'Favourite' }}
        </button>
        <button v-if="viewerId !== profile.user_id_fk" class="btn btn--email">
          Email
        </button>
          <router-link v-if="viewerId == profile.user_id_fk" :to="{ name: 'MatchesView', query: { profile_id: profile.id } }" class="btn">
            See Matches
          </router-link>
      </div>
    
    </div>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/axios'

const profile = ref(null)
const currentUser = ref(null)
const isFavourited = ref(false)
const route = useRoute()
const viewerId =ref(null)

onMounted(async () => {
  try {
    console.log(`/api/profile/${route.params.profile_id}`)
    const res = await apiClient.get(`/api/profile/${route.params.profile_id}`)
    console.log('Profile data:', res.data)    
    profile.value = res.data
    viewerId.value = parseInt(res.data.viewer_id)
    const currentUserRes = await apiClient.get(`/api/users/${profile.value.user_id_fk}`)
    currentUser.value = currentUserRes.data.user

    const favRes = await apiClient.get(`/api/favourites`);
    if (favRes.status === 200 && favRes.data.favourites) {
      isFavourited.value = favRes.data.favourites.some(fav => fav.id === profile.value.user_id_fk);
    }
  } catch (err) {
    console.error('Error fetching profile:', err)
  }
})

const toggleFavourite = async () => {
  try {
    const url = `/api/profiles/${profile.value.user_id_fk}/favourite`
    if (isFavourited.value) {
      // Unfavourite
      const res = await apiClient.delete(`/api/profiles/${profile.value.user_id_fk}/favourite`)
      if (res.status === 200) {
        isFavourited.value = false
      }
    } else {
      // Favourite
      const res = await apiClient.post(`/api/profiles/${profile.value.user_id_fk}/favourite`)
      if (res.status === 200 || res.status === 201) {
        isFavourited.value = true
      }
    }
  } catch (err) {
    console.error('Error toggling favourite status:', err)
  }
}

</script>

<style scoped>
.profile-details {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-header-info .full-name {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.profile-header-info .username {
  color: #555;
}

.btn {
  background-color: #a0512f;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #c7baa2;
}
.btn--email{
  background-color: #70815b;
  color: #f9f9f9;
  margin-left: 10px;
}

</style>