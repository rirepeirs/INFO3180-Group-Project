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
      <div class="profile-grid">
        <ProfileCard 
          v-for="profile in profiles" 
          :key="profile.id" 
          :profile="profile" 
          :defaultImage="defaultImage" 
        />
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/axios'
import ProfileCard from '../components/ProfileCard.vue'

const profiles = ref([])

const filters = ref({
  name: '',
  sex: '',
  race: '',
  birth_year: ''
})

const showAdvanced = ref(false)
const defaultImage = '/static/default-profile.png'

const fetchNewestProfiles = async () => {
  try {
    const res = await axios.get('/api/profiles')
    profiles.value = res.data.profiles
      .sort((a, b) => b.id - a.id)
      .slice(0, 4)
  } catch (err) {
    console.error('Error loading newest profiles:', err)
  }
}

const fetchProfiles = async () => {
  try {
    const response = await axios.get('/api/search', {
      params: {
        ...filters.value,
      }
    })
    profiles.value = response.data.profiles
  } catch (err) {
    console.error('Error loading profiles:', err)
  }
}

onMounted(fetchNewestProfiles)
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
  
  /* .profile-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
  }
  
  .profile-card {
    width: 150px;
    text-align: center;
    background: white;
    border-radius: 10px;
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
    padding: 1em;
  } */
  
  /* .profile-card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 8px;
  } */

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
  width: 80px; /* Reduced from 120px */
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
  </style>