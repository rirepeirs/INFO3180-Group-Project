<template>
    <div class="profile-details" v-if="profile">
      <h1>Profile #{{ profile.id }}</h1>
  
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
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from '@/axios'
  
  const profile = ref(null)
  const route = useRoute()
  
  onMounted(async () => {
    try {
      const response = await axios.get(`/api/profile/${route.params.profile_id}`)
      profile.value = response.data
    } catch (err) {
      console.error('Failed to fetch profile:', err)
    }
  })
  </script>