<template>
  <div class="register-container">
    <h1 class="title">註冊新帳號</h1>
    <form class="register-form" @submit.prevent="register">
      <div class="form-group">
        <label>帳號</label>
        <input v-model="username" type="text" placeholder="請輸入帳號" />
      </div>
      <div class="form-group">
        <label>密碼</label>
        <input v-model="password" type="password" placeholder="請輸入密碼" />
      </div>
      <button type="submit" class="register-button">註冊</button>
      <p v-if="message" class="error-message">{{ message }}</p>
      <button type="button" class="secondary-button" @click="goToLogin">
        返回登入頁
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const message = ref('')
const router = useRouter()

const register = async () => {
  try {
    const res = await axios.post(`${import.meta.env.VITE_API_URL}/register`, {
      username: username.value,
      password: password.value
    })
    message.value = res.data.message || '註冊成功！'
  } catch (err: any) {
    message.value = err.response?.data?.detail || '註冊失敗'
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
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

.register-form {
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

.register-button {
  padding: 0.75rem;
  background-color: #67c23a;
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
  margin-top: 0.5rem;
}

.error-message {
  margin-top: 1rem;
  color: red;
  font-size: 0.9rem;
}
</style>
