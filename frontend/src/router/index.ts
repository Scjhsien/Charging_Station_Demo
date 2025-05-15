// src/router/index.ts

import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import HomePage from '@/pages/HomePage.vue'
import { useUserStore } from '@/store/user'  // 引入 Pinia store

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: HomePage,
      meta: { requiresAuth: true }  // 需要登入保護
    },
    {
      path: '/login',
      component: LoginPage
    },
    {
      path: '/register',
      component: RegisterPage
    },
    {
      path: '/home',
      component: HomePage
    }
  ]
})

// 路由守衛：保護需要登入的頁面
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  userStore.init()  // 重新整理後還原登入狀態

  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')  // 未登入跳轉到 login
  } else {
    next()  // 放行
  }
})

export default router
