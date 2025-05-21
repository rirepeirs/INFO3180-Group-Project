<template>
  <div class="register-container">
    <h1>Register</h1>
    <form @submit.prevent="registerUser">
      <div>
        <label for="username">Username:</label>
        <input v-model="username" type="text" id="username" required />
      </div>

      <div>
        <label for="email">Email:</label>
        <input v-model="email" type="email" id="email" required />
      </div>

      <div>
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" required />
      </div>

      <div>
        <label for="name">Full Name:</label>
        <input v-model="name" type="text" id="name" required />
      </div>

      <!-- Add file input for photo -->
      <div>
        <label for="photo">Profile Photo:</label>
        <input type="file" id="photo" @change="handlePhotoUpload" />
      </div>

      <button type="submit">Register</button>

      <ul v-if="errors.length" class="error-list">
        <li v-for="(err, index) in errors" :key="index" class="error">{{ err }}</li>
      </ul>
    </form>

    <p class="mt-3">
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<script>
import apiClient from '@/axios'

export default {
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      name: '',
      photo: null, 
      errors: []
    }
  },
  methods: {
    handlePhotoUpload(event) {
      this.photo = event.target.files[0]
    },

    async registerUser() {
      const formData = new FormData()
      formData.append('username', this.username)
      formData.append('email', this.email)
      formData.append('password', this.password)
      formData.append('name', this.name)
      if (this.photo) formData.append('photo', this.photo)

      try {
        const response = await apiClient.post('/api/register', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'  // Important for file uploads
          }
        })

        this.$router.push('/login')
      } catch (err) {
        const data = err.response?.data
        if (Array.isArray(data?.errors)) {
          this.errors = data.errors
        } else if (data?.error) {
          this.errors = [data.error]
        } else {
          this.errors = ['Registration failed. Please try again.']
        }
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
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
  display: block;
  margin-bottom: 0.4em;
  font-weight: 600;
  color: #ffffff;
}

input {
  width: 100%;
  padding: 0.75em;
  border-radius: 8px;
  border: 1px solid #ccc;
  transition: border 0.3s;
}

input:focus {
  border-color: #7e9e69;
  outline: none;
}

button[type='submit'] {
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

button[type='submit']:hover {
  background: #c7baa2;
  transform: translateY(-2px);
}

button[type='submit']:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(126, 158, 105, 0.3);
}

.error-list {
  margin-top: 1em;
  padding-left: 1.2em;
  color: red;
}

.error {
  font-weight: 500;
}

.mt-3 {
  text-align: center;
  margin-top: 1.5em;
  font-size: 0.95em;
  color: #d7d5d5;
}

.mt-3 a {
  color: #99bd81;
  font-weight: bold;
  text-decoration: none;
}

.mt-3 a:hover {
  text-decoration: underline;
}
</style>