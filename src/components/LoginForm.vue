<template>
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="loginUser">
        <div>
          <label for="username">Username:</label>
          <input v-model="username" type="text" id="username" required />
        </div>
  
        <div>
          <label for="password">Password:</label>
          <input v-model="password" type="password" id="password" required />
        </div>
  
        <button type="submit">Login</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
  
      <p class="mt-3">
        Don't have an account?
        <router-link to="/register">Register</router-link>
      </p>
    </div>
  </template>
  
<script>
  import apiClient from '@/axios'
  import { login } from '@/auth'
  
  export default {
    name: 'LoginView',
    data() {
      return {
        username: '',
        password: '',
        error: ''
      }
    },
    methods: {
      async loginUser() {


        try {
          const response = await apiClient.post('/api/auth/login', {
            username: this.username,
            password: this.password
          })
  
          const token = response.data.token;
          const user = response.data.user;
          if (token && user?.id) {
            localStorage.setItem('userId', user.id);
            login(token)
            this.$router.push('/search')
          } else {
            this.error = 'Invalid login response'
          }
        } catch (err) {
          this.error =
            err.response?.data?.errors?.[0] ||
            err.response?.data?.error ||
            'Login failed. Please try again.'
        }
      }
    }
  }
</script>
  
  <style scoped>
  .login-container {
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
  
  .error {
    color: red;
    margin-top: 1em;
    font-weight: 500;
    text-align: center;
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