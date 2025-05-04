<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="hero-container">
    <div class="overlay"></div>
    <div class="container hero-content text-dark position-relative">
      <div class="row align-items-center">
       
        <div class="col-md-6">
          <h1 class="display-4 fw-bold">JAM-DATE</h1>
          <p class="lead">
            JAM-DATE is a platform to help people <span class="highlight">connect</span> and discover 
            <span class="highlight">meaningful relationships</span>. Whether you're searching for a 
            <span class="highlight">friend</span> or a <span class="highlight">lifelong partner</span>, 
            we bring like-minded Jamaicans together in one digital space.
          </p>
        </div>

        
        <div class="col-md-6 text-center">
          <h2 class="tagline mb-4">Find your match</h2>
          <RouterLink to="/login" class="btn btn-primary btn-lg rounded-pill px-5">
            Login
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.hero-container {
  position: relative;
  background-color: #f8f4ec;
  background-image: url('@/assets/couple-photo.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff; 
}
h1{
  color: #e8a97d;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4); 
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  padding: 2rem 4rem;
  text-align: left;
}

.display-4 {
  font-weight: 700;
  color: #fff;
}

.lead {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #fefefe;
}

.highlight {
  color: #38b5a0; 
  font-weight: bold;
}

.tagline {
  font-size: 2rem;
  font-weight: 600;
  color: #fff;
}

.btn-primary {
  background-color: #38b5a0;
  border-color: #38b5a0;
}

.btn-primary:hover {
  background-color: #2c9483;
  border-color: #2c9483;
}
</style>