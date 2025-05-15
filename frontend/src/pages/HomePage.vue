<template>
  <div class="home-page">
    <!-- 使用者資訊 -->
    <div class="info-bar">
      <div>
        <strong>登入帳號：</strong>{{ username }}
        <span class="status-on">已登入</span>
      </div>
      <button class="logout-btn" @click="logout">登出</button>
    </div>

    <!-- 主內容 -->
    <div class="main-content">
      <div v-if="loading" class="status-text">讀取資料中...</div>
      <div v-else>
        <div v-if="error" class="status-text error-text">{{ error }}</div>

        <!-- 卡片顯示 -->
        <div class="stations-wrapper">
          <div v-for="station in stations" :key="station.id" class="station-info-card">
            <img :src="station.image" alt="station" class="station-img" />
            <div class="station-details">
              <h2>{{ station.name }} 狀態</h2>
              <p><strong>是否有車：</strong>{{ station.hasCar ? '有車' : '無車' }}</p>
              <p><strong>電池電壓：</strong>{{ station.batteryVoltage.toFixed(1) }} V</p>
              <p><strong>充電電壓：</strong>{{ station.chargeVoltage.toFixed(1) }} V</p>
              <p><strong>充電電流：</strong>{{ station.current.toFixed(1) }} A</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const error = ref('')
const loading = ref(true)

const stations = ref([
  {
    id: 'A',
    name: '充電站 A',
    hasCar: false,
    batteryVoltage: 0,
    chargeVoltage: 0,
    current: 0,
    image: '/station_a.png',
  },
  {
    id: 'B',
    name: '充電站 B',
    hasCar: false,
    batteryVoltage: 0,
    chargeVoltage: 0,
    current: 0,
    image: '/station_b.png',
  },
  {
    id: 'C',
    name: '充電站 C',
    hasCar: false,
    batteryVoltage: 0,
    chargeVoltage: 0,
    current: 0,
    image: '/station_c.png',
  },
])

// 取得充電站資料
const fetchStations = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/stations`)
    const data = response.data

    for (const station of stations.value) {
      const found = data.find((s: any) => s.station_id === station.id)
      if (found) {
        station.hasCar = found.occupied
        station.batteryVoltage = found.battery_voltage
        station.chargeVoltage = found.charge_voltage
        station.current = found.charge_current
      }
    }
  } catch (err) {
    console.error('❌ 取得資料失敗:', err)
    error.value = '⚠️ 取得充電站資訊失敗，顯示初始資料'
  }
}

// 登出
const logout = () => {
  userStore.logout()
  router.push('/login')
}

let intervalId: number

onMounted(async () => {
  userStore.init()
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/me`, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    username.value = res.data.username
    await fetchStations()

    // ✅ 每秒更新一次資料
    intervalId = setInterval(() => {
      fetchStations()
    }, 1000)

  } catch (err: any) {
    error.value = err.response?.data?.detail || '驗證失敗'
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  clearInterval(intervalId)
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
  flex-direction: column;
  align-items: center;
}

.status-text {
  font-size: 1.1rem;
  color: #606266;
  margin-top: 1rem;
}

.error-text {
  color: red;
  font-weight: bold;
}

.stations-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
  width: 100%;
  max-width: 1000px;
}

.station-info-card {
  width: 300px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.station-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.station-details {
  width: 100%;
  padding: 1rem 1.2rem;
  font-size: 1rem;
  line-height: 1.6rem;
  text-align: left;
}
</style>
