<template>
  <div class="profile-card">
    <img 
      :src="getPhotoUrl" 
      alt="Profile photo" 
      class="profile-photo" 
    />
    <div class="profile-info">
      <h4 class="profile-name">{{ displayName }}</h4>
      <p class="profile-birthyear" v-if="profile.birth_year">
        {{ profile.birth_year }}
      </p>
    </div>

    <button v-if="hasProfileId" @click="viewProfile">
      View Details
    </button>
  </div>
</template>

<script>
export default {
  name: 'ProfileCard',
  props: {
    profile: {
      type: Object,
      required: true
    },
    defaultImage: {
      type: String,
      default: '/static/default-profile.png'
    }
  },
  computed: {
    displayName() {
      return this.profile?.user?.name || this.profile.name || 'Unknown Name';
    },
    getPhotoUrl() {
      const photo = this.profile?.user?.photo || this.profile.photo;
      return photo ? `http://localhost:8080/uploads/${photo}` : this.defaultImage;
    },
    hasProfileId() {
      return this.profile?.profile_id || this.profile?.id;
    }
  },
  methods: {
    viewProfile() {
      const pid = this.profile?.profile_id || this.profile?.id;
      if (pid) {
        this.$router.push(`/profiles/${pid}`);
      } else {
        console.error('Missing profile ID:', this.profile);
      }
    }
  }
};
</script>

  
  <style scoped>
  .profile-card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    width: 220px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    margin: 1rem;
    transition: box-shadow 0.3s;
  }
  
  .profile-card:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }
  
  .profile-photo {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 1rem;
  }
  
  .profile-info {
    margin-bottom: 1rem;
  }
  
  .profile-name {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 0.3rem;
  }
  
  .profile-birthyear {
    font-size: 0.9rem;
    color: #555;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 0.5rem;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #45a049;
  }

/*   
.email-btn {
  background-color: #5a86a0;
}

.email-btn:hover {
  background-color: #87b2cb;
} */
  </style>