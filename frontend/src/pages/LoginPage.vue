<template>
  <div class="login-container">
    <h1 class="title">登入</h1>
    <form class="login-form" @submit.prevent="login">
      <div class="form-group">
        <label for="username">帳號</label>
        <input id="username" v-model="username" type="text" placeholder="請輸入帳號" />
      </div>
      <div class="form-group">
        <label for="password">密碼</label>
        <input id="password" v-model="password" type="password" placeholder="請輸入密碼" />
      </div>
      <button type="submit" class="login-button">登入</button>
      <p v-if="message" class="error-message">{{ message }}</p>
    </form>
    <button class="secondary-button" @click="goToRegister">註冊新帳號</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const message = ref('')
const userStore = useUserStore()
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post(`${import.meta.env.VITE_API_URL}/login`, {
      username: username.value,
      password: password.value
    })
    userStore.login(res.data.access_token, username.value)
    message.value = '登入成功'
    setTimeout(() => {
      router.push('/home')
    }, 1000)
  } catch (err: any) {
    message.value = err.response?.data?.detail || '登入失敗'
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  width: 340px;
  margin: 100px auto;
  padding: 2rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  background-color: #fff;
  text-align: center;
}

.title {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: bold;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input {
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.login-button {
  padding: 0.75rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
}

.secondary-button {
  background: none;
  border: none;
  color: #409eff;
  font-size: 0.9rem;
  cursor: pointer;
  margin-top: 1rem;
}

.error-message {
  margin-top: 1rem;
  color: red;
  font-size: 0.9rem;
}
</style>
