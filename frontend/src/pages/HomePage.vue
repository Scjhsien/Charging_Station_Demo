<template>
  <div class="home-page">
    <div class="info-bar">
      <div>
        <strong>登入帳號：</strong>{{ username }}
        <span class="status-on">已登入</span>
      </div>
      <button class="logout-btn" @click="logout">登出</button>
    </div>

    <div class="main-content">
      <div v-if="loading" class="status-text">讀取使用者資料中...</div>
      <div v-else-if="error" class="status-text error-text">{{ error }}</div>
      <div v-else class="welcome-card">
        <h2 class="welcome-message">Welcome，{{ username }}！</h2>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const error = ref('')
const loading = ref(true)

const logout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(async () => {
  userStore.init()
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/me`, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    username.value = res.data.username
  } catch (err: any) {
    error.value = err.response?.data?.detail || '驗證失敗'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-page {
  padding: 2rem;
  background-color: #f9fafc;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
}

.info-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 1rem 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.status-on {
  color: #409eff;
  margin-left: 10px;
  font-weight: bold;
}

.logout-btn {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.status-text {
  font-size: 1.1rem;
  color: #606266;
  margin-top: 2rem;
}

.error-text {
  color: red;
  font-weight: bold;
}

.welcome-card {
  background-color: #fff;
  padding: 2rem 3rem;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  text-align: center;
  max-width: 500px;
}

.welcome-message {
  font-size: 1.5rem;
  font-weight: bold;
  color: #303133;
  margin-bottom: 1rem;
}

</style>
