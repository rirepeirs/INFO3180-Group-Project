<template>
    <div class="add-profile-container">
      <h1>Create New Profile</h1>
      <form @submit.prevent="submitProfile">
        <div>
          <label>Description:</label>
          <textarea v-model="profile.description" required></textarea>
        </div>
  
        <div>
          <label>Parish:</label>
          <select v-model="profile.parish" required>
            <option disabled value="">Select Parish</option>
            <option v-for="parish in parishes" :key="parish" :value="parish">
              {{ parish }}
            </option>
          </select>
        </div>
  
        <div>
          <label>Biography:</label>
          <textarea v-model="profile.biography" required></textarea>
        </div>
  
        <div>
          <label>Sex:</label>
          <select v-model="profile.sex" required>
            <option disabled value="">Select</option>
            <option>Male</option>
            <option>Female</option>
          </select>
        </div>
  
        <div>
          <label>Race:</label>
          <select v-model="profile.race" required>
            <option disabled value="">Select Race</option>
            <option>Black</option>
            <option>White</option>
            <option>Asian</option>
          </select>
        </div>
  
        <div>
          <label>Birth Year:</label>
          <select v-model.number="profile.birth_year" required>
            <option disabled value="">Select Birth Year</option>
            <option v-for="year in birthYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
  
        <div>
          <label for="height">Height (cm)</label>
          <input type="number" id="height" v-model="profile.height" min="100" max="300" step="1" class="form-control" required/>
        </div>
  
        <div>
          <label>Favourite Cuisine:</label>
          <input type="text" v-model="profile.fav_cuisine" />
        </div>
  
        <div>
          <label>Favourite Colour:</label>
          <input type="text" v-model="profile.fav_colour" />
        </div>
  
        <div>
          <label>Favourite School Subject:</label>
          <input type="text" v-model="profile.fav_school_subject" />
        </div>
  
        <div class="checkbox-group">
          <label><input type="checkbox" v-model="profile.political" /> Political</label>
        </div>
        <div class="checkbox-group">
          <label><input type="checkbox" v-model="profile.religious" /> Religious</label>
        </div>
        <div class="checkbox-group">
          <label><input type="checkbox" v-model="profile.family_oriented" /> Family Oriented</label>
        </div>
        <button type="submit">Create Profile</button>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>
      </form>
    </div>
  </template>
  
<script setup>
  import { reactive, ref, computed } from 'vue';
  import axios from '@/axios'; 
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const profile = reactive({
    description: '',
    parish: '',
    biography: '',
    sex: '',
    race: '',
    birth_year: '',
    height: null,
    fav_cuisine: '',
    fav_colour: '',
    fav_school_subject: '',
    political: false,
    religious: false,
    family_oriented: false
  });
  
  const error = ref('');
  const success = ref('');
  
  const parishes = [
    'Kingston', 'St. Andrew', 'St. Thomas', 'Portland', 'St. Mary',
    'St. Ann', 'Trelawny', 'St. James', 'Hanover', 'Westmoreland',
    'St. Elizabeth', 'Manchester', 'Clarendon', 'St. Catherine'
  ];
  
  const currentYear = new Date().getFullYear();
  const birthYears = computed(() => {
    const years = [];
    for (let y = currentYear - 18; y >= currentYear - 100; y--) {
      years.push(y);
    }
    return years;
  });
  

  console.log("Sending profile data:", profile);

  const submitProfile = async () => {
  error.value = '';
  success.value = '';

  try {
    const token = localStorage.getItem('token');
    console.log("Sending profile data:", profile);

    console.log("About to send profile data:", JSON.stringify(profile, null, 2));
    const response = await axios.post('/api/profiles', profile, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    success.value = 'Profile successfully created!';
    Object.keys(profile).forEach(key => {
      profile[key] = typeof profile[key] === 'boolean' ? false : '';
    });
    router.push('/profiles/${profile_id}');
  } catch (err) {
    console.error("Server response:", err.response?.data);
    
    if (err.response) {
      const status = err.response.status;
      const msg = err.response.data.msg;

      if (status === 401 && msg === 'Token has expired') {
        alert('Your session has expired. Please log in again.');
        localStorage.removeItem('token');
        router.push('/login');  
      } else {
        error.value = msg || 'Something went wrong.';
      }
    } else {
      error.value = 'Network error or server is unreachable.';
    }
  }
};
</script>
  
  
  <style scoped>
  .add-profile-container {
    max-width: 600px;
    margin: 60px auto;
    padding: 2em;
    background-color: #5c3a2e;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    text-align: center;
    margin-bottom: 1.5em;
    font-size: 1.8em;
    color: #fffdfd;
  }
  
  form > div {
    margin-bottom: 1.2em;
  }
  
  label {
    font-weight: 600;
    color: #ffffff;
  }
  
  form > div:not(.checkbox-group) > label {
    display: block;
    margin-bottom: 0.4em;
  }
  
  textarea,
  input,
  select {
    width: 100%;
    padding: 0.75em;
    border-radius: 8px;
    border: 1px solid #ccc;
    transition: border 0.3s;
  }
  
  textarea:focus,
  input:focus,
  select:focus {
    border-color: #7e9e69;
    outline: none;
  }
  
  input[type="checkbox"] {
    margin-right: 0.5em;
    transform: scale(1.1);
  }
  
  .checkbox-group {
    display: flex;
    align-items: center;
    margin-bottom: 0.8em;
  }
  
  .checkbox-group label {
    display: flex;
    align-items: center;
    gap: 0.5em;
    color: #ffffff;
    font-weight: 500;
    margin: 0;
    white-space: nowrap;
  }
  
  button[type="submit"] {
    margin-top: 1.2em;
    width: 100%;
    padding: 0.75em;
    background: #70815b;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s ease;
  }
  
  button[type="submit"]:hover {
    background: #c7baa2;
    transform: translateY(-2px);
  }
  
  button[type="submit"]:active {
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(126, 158, 105, 0.3);
  }
  
  .error {
    color: red;
    margin-top: 1em;
    font-weight: 500;
    text-align: center;
  }
  
  .success {
    color: #a7ffb4;
    margin-top: 1em;
    font-weight: 500;
    text-align: center;
  }
  </style>