import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/masters/',
      name: 'masters',
      component: () => import('@/views/MastersView.vue')
    },
    {
      path: '/register/',
      name: 'register',
      component: () => import('@/views/RegisterView.vue')
    },
    {
      path: '/login/',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/profile_client/',
      name: 'profile_client',
      component: () => import('@/views/ProfileClientView.vue')
    },
    {
      path: '/profile_master/',
      name: 'profile_master',
      component: () => import('@/views/ProfileMasterView.vue')},
      
    {
      path: '/profile_edit/',
      name: 'profile_edit',
      component: () => import('@/views/ProfileEditView.vue')
    },    
    {
      path: '/masters/:id',
      name: 'masterprofile',
      component: () => import('@/views/MasterProfileView.vue')
    },
    {
      path: '/services/',
      name: 'services',
      component: () => import('@/views/ServicesView.vue')
    },
    {
      path: '/services/:id',
      name: 'service',
      component: () => import('@/components/Service.vue')
    },
    {
      path: '/blogs/',
      name: 'blogs',
      component: () => import('@/views/BlogsView.vue')
    },
    {
      path: '/blogs/:id',
      name: 'blog',
      component: () => import('@/views/BlogView.vue')
    },

    {
      path: '/blog_create/',
      name: 'blog_create',
      component: () => import('@/views/BlogCreateView.vue')
    },
    {
      path: '/service_create/',
      name: 'service_create',
      component: () => import('@/views/ServiceCreateView.vue')
    },
    {
      path: '/messenger/',
      name: 'messenger',
      component: () => import('@/views/MessengerView.vue')
    },

  ]
})

export default router
