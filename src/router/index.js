import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import UserDetailsView from '@/views/UserDetailsView.vue';
import ProfileDetailsView from '@/views/ProfileDetailsView.vue';
import AddProfileView from '@/views/AddProfileView.vue';
import FavouritesView from '@/views/FavouritesView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path:'/users/:user_id',
      name: 'UserDetails',
      Component: UserDetailsView
    },
    {
      path:'/profiles/:profile_id',
      name: 'PorfileDetails',
      Component: ProfileDetailsView
    },
    {
      path:'/profiles/new',
      name: 'AddProfile',
      Component: AddProfileView
    },
    {
      path:'/profiles/favourites',
      name: 'Favourites',
      Component: FavouritesView
    }   
  ]
})

export default router
