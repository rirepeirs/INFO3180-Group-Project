import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import UserDetailsView from '@/views/UserDetailsView.vue';
import ProfileDetailsView from '@/views/ProfileDetailsView.vue';
import AddProfileView from '@/views/AddProfileView.vue';
import FavouritesView from '@/views/FavouritesView.vue';
import SearchView from '@/views/SearchView.vue';
import TopFavouredView from '@/views/TopFavouredView.vue';
import MatchesView from '@/views/MatchesView.vue';

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
      component: UserDetailsView,
      props: route => ({ userId: Number(route.params.user_id) })
    },
    {
      path:'/profiles/:profile_id',
      name: 'ProfileDetails',
      component: ProfileDetailsView
    },
    {
      path:'/profiles/new',
      name: 'AddProfile',
      component: AddProfileView
    },
    {
      path:'/profiles/yourfavourites',
      name: 'Favourites',
      component: FavouritesView
    },
    {
      path: '/search',
      name: 'Search',
      component: SearchView
    },
    {
      path: '/top-favoured',
      name: 'TopFavoured',
      component: TopFavouredView
    },
    {
      path: '/matches-report',
      name: 'MatchesView',
      component: MatchesView
    }      
  ]
})

export default router
