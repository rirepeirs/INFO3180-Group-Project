<template>
    <div class="profile-page">
      <div class="search-section">
        <h2>Search Profiles</h2>
  
        <!-- Name Search -->
        <input type="text" placeholder="Search name" v-model="filters.name" />
  
        <!-- Buttons Section -->
        <div class="button-group">
          <button @click="showAdvanced = !showAdvanced" type="button" class="btn rounded-btn">
            {{ showAdvanced ? 'Hide Filters' : 'More Filters' }}
          </button>
  
          <button @click="fetchProfiles" class="btn rounded-btn">
            Search
          </button>

          <button @click="resetFilters" class="btn rounded-btn">
            Reset
          </button>
        </div>
  
        <!-- Advanced Filters -->
        <div v-if="showAdvanced">
          <!-- Sex Radio Buttons -->
          <div class="tab-group">
            <label>Sex:</label>
            <div class="radio-tabs">
              <label
                v-for="option in ['Male', 'Female']"
                :key="option"
                :class="{ active: filters.sex === option }"
              >
                <input
                  type="radio"
                  name="sex"
                  :value="option"
                  v-model="filters.sex"
                />
                {{ option }}
              </label>
            </div>
          </div>
  
          <!-- Race Multi-Select Tabs -->
          <div class="tab-group">
            <label>Race:</label>
            <div class="radio-tabs">
              <label
                v-for="option in ['Black', 'White', 'Asian']"
                :key="option"
                :class="{ active: filters.race === option }"
              >
                <input
                  type="radio"
                  name="race"
                  :value="option"
                  v-model="filters.race"
                />
                {{ option }}
              </label>
            </div>
          </div>
  
          <!-- Birth Year Input -->
          <div class="tab-group">
            <label>Birth Year:</label>
            <input type="text"
              v-model="filters.birth_year" placeholder="e.g., 1995"
              class="short-input"/>
          </div>
      </div>
  
      <!-- Profiles Grid -->
      <div class="profile-grid" v-if="profiles.length">
        <ProfileCard 
          v-for="profile in profiles" 
          :key="profile.id" 
          :profile="profile" 
        />
      </div>
      <p v-else class="no-results">No results found</p>
    </div>
  </div>
</template>
  
<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from '@/axios'
import ProfileCard from '../components/ProfileCard.vue'

const profiles = ref([])
const currentUserId = ref(null)

const filters = ref({
  name: '',
  sex: '',
  race: '',
  birth_year: ''
})

const resetFilters = () => {
  filters.value = {
    name: '',
    sex: '',
    race: '',
    birth_year: ''
  }
  fetchNewestProfiles()
}

const showAdvanced = ref(false)

const enrichProfilesWithUserData = async (rawProfiles) => {
  return await Promise.all(
    rawProfiles.map(async (profile) => {
      try {
        const userRes = await axios.get(`/api/users/${profile.user_id_fk}`)
        const user = userRes.data.user
        return {
          ...profile,
          user: user ? {
            name: user.name,
            photo: user.photo,
            username: user.username
          } : null
        }
      } catch (err) {
        console.error(`Failed to fetch user for profile ${profile.id}`, err)
        return { ...profile, user: null }
      }
    })
  )
}

const fetchNewestProfiles = async () => {
  try {
    const res = await axios.get('/api/profiles')
    const newest = res.data.profiles
      .filter(p => p.user_id_fk !== currentUserId.value)
      .sort((a, b) => b.id - a.id)
      .slice(0, 4)
    profiles.value = await enrichProfilesWithUserData(newest)
  } catch (err) {
    console.error('Error loading newest profiles:', err)
  }
}

const fetchProfiles = async () => {
  try {
    const queryParams = { ...filters.value };
    Object.keys(queryParams).forEach((key) => {
      if (!queryParams[key]) delete queryParams[key];
    });

    const response = await axios.get('/api/search', { params: queryParams });
    const rawProfiles = (response.data || [])
      .filter(p => p.user_id_fk !== currentUserId.value) 

    if (rawProfiles.length === 0) {
      profiles.value = [];
      return;
    }

    const enrichedProfiles = await enrichProfilesWithUserData(rawProfiles)
    profiles.value = enrichedProfiles
  } catch (err) {
    console.error('Error loading profiles:', err)
  }
}

watch(filters, (newFilters) => {
  const allEmpty = Object.values(newFilters).every((val) => val === '')
  if (allEmpty) fetchNewestProfiles()
}, { deep: true })

onMounted(async () => {
  try {
    const res = await axios.get('/api/auth/me')
    currentUserId.value = res.data.id
    fetchNewestProfiles()
  } catch (err) {
    console.error('Failed to fetch current user:', err)
  }
})
</script>




  <style scoped>
  .profile-page {
    max-width: 960px;
    margin: auto;
    padding: 2em;
  }
  
  .search-section {
    background-color: #f5f5f5;
    padding: 1em;
    margin-bottom: 2em;
    border-radius: 10px;
  }
  
  .search-section h2 {
    margin-bottom: 0.5em;
  }
  
  .search-section input {
    display: block;
    width: 100%;
    margin-bottom: 1em;
    padding: 0.5em;
  }
  
  .tabs,
  .radio-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5em;
    margin-bottom: 1em;
  }
  
  .tabs button,
  .radio-tabs label {
    padding: 0.5em 1em;
    border-radius: 20px;
    background-color: #eee;
    cursor: pointer;
    border: none;
    transition: background 0.2s;
    font-size: 0.9rem;
  }
  
  .tabs button.active,
  .radio-tabs label.active {
    background-color: #e8a97d;
    color: white;
    font-weight: bold;
  }
  
  .radio-tabs input[type="radio"] {
    display: none;
  }
  
  .tab-group label {
    display: block;
    margin-bottom: 0.25em;
    font-weight: 600;
  }

.button-group {
  display: flex;
  gap: 1em;
  margin-bottom: 1.5em;
}

.btn.rounded-btn {
  padding: 0.6em 1.2em;
  border-radius: 25px;
  background-color: #e8a97d;
  color: white;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.btn.rounded-btn:hover {
  background-color: #70815b;
}

.short-input {
  width: 80px;
  padding: 0.3em 0.5em;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 0.9rem;
  text-align: left;
}

.profile-grid{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.75rem;
}

.no-results{
  text-align: center;
  font-style: italic;
  color: #888;
  margin-top: 1em;
}
  </style>