<template>
  <div class="container mt-5 pt-5">
    <ProfileForm :user-photo="userPhoto" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/axios';
import ProfileForm from '@/components/ProfileForm.vue';

const user = ref(null);
const userPhoto = ref('');

onMounted(async () => {
  try {
    const token = localStorage.getItem('token');
    const userId = Number(localStorage.getItem('userId'));

    if (!userId || isNaN(userId)) {
      console.error("Invalid user ID");
      return;
    }

    const res = await axios.get(`/api/users/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    user.value = res.data.user;
    userPhoto.value = user.value.photo;
  } catch (err) {
    console.error("Failed to fetch user:", err);
  }
});
</script>
