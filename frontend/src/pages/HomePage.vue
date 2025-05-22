<template>
  <div class="home-page">
    <div class="info-bar">
      <div>
        <strong>登入帳號：</strong>{{ username }}
        <span class="status-on">已登入</span>
      </div>
      <button class="logout-btn" @click="logout">登出</button>
    </div>

    <div class="station-selector">
      <label for="station-select">選擇充電站：</label>
      <select id="station-select" v-model="selectedStationId">
        <option v-for="station in stations" :key="station.id" :value="station.id">
          {{ station.name }}
        </option>
      </select>
    </div>

    <div v-if="selectedStation" class="station-info-card">
      <h2 class="station-title">{{ selectedStation.name }} 狀態</h2>
      <img :src="selectedStation.image" alt="station" class="station-img" />

      <div class="station-grid">
        <div class="station-column">
          <div class="row">
            <label>是否有車：</label>
            <span>{{ selectedStation.hasCar ? '有車' : '無車' }}</span>
          </div>
          <div class="row">
            <label>電池電壓：</label>
            <span>{{ selectedStation.batteryVoltage.toFixed(1) }} V</span>
          </div>
          <div class="row">
            <label>錯誤資訊：</label>
            <span>{{ selectedStation.errorMessage || '無' }}</span>
          </div>
        </div>

        <div class="divider"></div>

        <div class="station-column">
          <div class="row">
            <label>狀態：</label>
            <select v-model="editing.status" class="input">
              <option value="none">----</option>
              <option value="reserved">預約</option>
            </select>
          </div>
          <div class="row">
            <label>充電電壓：</label>
            <input type="number" step="0.1" v-model.number="editing.chargeVoltage" class="input" />
          </div>
          <div class="row">
            <label>充電電流：</label>
            <input type="number" step="0.1" v-model.number="editing.chargeCurrent" class="input" />
          </div>
          <div class="row button-row">
            <button class="update-btn" @click="submitStationSettings">更新設定</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const error = ref('')
const selectedStationId = ref('A')
const loading = ref(true)

const stations = ref([
  { id: 'A', name: '充電站 A', hasCar: false, batteryVoltage: 0, chargeVoltage: 58, current: 10, status: 'none', errorMessage: '', image: '/station_a.png' },
  { id: 'B', name: '充電站 B', hasCar: false, batteryVoltage: 0, chargeVoltage: 58, current: 10, status: 'none', errorMessage: '', image: '/station_b.png' },
  { id: 'C', name: '充電站 C', hasCar: false, batteryVoltage: 0, chargeVoltage: 58, current: 10, status: 'none', errorMessage: '', image: '/station_c.png' }
])

const selectedStation = computed(() => stations.value.find((s) => s.id === selectedStationId.value))

const editing = ref({ chargeVoltage: 58, chargeCurrent: 10, status: 'none' })

watch(selectedStationId, () => {
  const s = selectedStation.value
  if (s) {
    editing.value.chargeVoltage = s.chargeVoltage
    editing.value.chargeCurrent = s.current
    editing.value.status = s.status
  }
}, { immediate: true })

let socket: WebSocket

const submitStationSettings = () => {
  if (!selectedStation.value || socket.readyState !== WebSocket.OPEN) return
  selectedStation.value.chargeVoltage = editing.value.chargeVoltage
  selectedStation.value.current = editing.value.chargeCurrent
  selectedStation.value.status = editing.value.status

  socket.send(JSON.stringify({
    station_id: selectedStation.value.id,
    charge_voltage: editing.value.chargeVoltage,
    charge_current: editing.value.chargeCurrent
  }))
  alert('設定已傳送至模擬器')
}

const logout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(async () => {
  userStore.init()
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/me`, {
      headers: { Authorization: `Bearer ${userStore.token}` }
    })
    username.value = res.data.username
  } catch (err: any) {
    error.value = err.response?.data?.detail || '驗證失敗'
    return
  } finally {
    loading.value = false
  }

  socket = new WebSocket('ws://localhost:8000/ws/homepage')

  socket.onopen = () => console.log('WebSocket 已連線')
  socket.onclose = () => console.log('WebSocket 已關閉')
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    const found = stations.value.find((s) => s.id === data.station_id)
    if (found) {
      found.hasCar = data.occupied
      found.batteryVoltage = data.battery_voltage
      found.errorMessage = data.error_message || ''
    }
  }
})

onUnmounted(() => {
  socket?.close()
})
</script>

<style scoped>
.home-page {
  padding: 2rem;
  background-color: #f9fafc;
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
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.station-selector {
  margin-bottom: 1.5rem;
  font-size: 1rem;
}

.station-info-card {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  max-width: 800px;
  margin: auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
}

.station-title {
  text-align: center;
  font-size: 1.6rem;
  margin-bottom: 1rem;
  color: #333;
}

.station-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  margin: 0 auto 2rem;
  border-radius: 8px;
}

.station-grid {
  display: grid;
  grid-template-columns: 1fr 1px 1fr;
  gap: 2rem;
}

.station-column {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  justify-content: start;
}

.row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.button-row {
  justify-content: flex-end;
}

label {
  width: 110px;
  font-weight: bold;
}

.input {
  flex: 1;
  padding: 0.4rem;
  font-size: 1rem;
}

.update-btn {
  background-color: #409eff;
  color: white;
  font-size: 1rem;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
}

.divider {
  background-color: #ddd;
  width: 1px;
  height: auto;
}
</style>
