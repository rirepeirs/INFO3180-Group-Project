<template>
  <div class="user-details" v-if="user">
    <!-- Display user info -->
    <img :src="user.photo" alt="User photo" class="user-photo" />
    <h2 class="full-name">{{ user.name }}</h2>
    <p class="username">@{{ user.username }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <p><strong>Date Joined:</strong> {{ user.date_joined }}</p>

    <hr class="my-4" />

    <!-- Display associated profiles as cards -->
    <div v-if="user.profiles && user.profiles.length > 0" class="profiles-cards-container">
      <h3>Profiles:</h3>
      <div class="profiles-grid">
        <ProfileCard
          v-for="profile in user.profiles"
          :key="profile.profile_id"
          :profile="profile"
        />
      </div>
    </div>
    <p v-else>No profiles available.</p>
  </div>

  <div v-else>
    <p>Loading user details...</p>
  </div>
</template>

<script>
import axios from 'axios';
import ProfileCard from '../components/ProfileCard.vue';  // Import ProfileCard component

export default {
  name: 'UserDetailsView',
  components: {
    ProfileCard
  },
  props: {
    userId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      user: null
    };
  },
  mounted() {
    this.fetchUser();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await axios.get(`/api/users/${this.userId}`);
        this.user = response.data;
      } catch (error) {
        console.error('Failed to load user details:', error);
      }
    }
  }
};
</script>

<style scoped>
.user-details {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-photo {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
}

.full-name {
  font-size: 1.75rem;
  font-weight: 600;
}

.username {
  color: #555;
  margin-bottom: 1rem;
}

.profiles-cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.profiles-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}
</style>