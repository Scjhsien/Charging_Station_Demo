<template>
  <div class="container">
    <div v-for="station in stations" :key="station.id" class="station-card">
      <h2>{{ station.name }}</h2>

      <div class="switch">
        <label>
          <input type="checkbox" v-model="station.occupied" />
          站位佔用
        </label>
      </div>

      <div class="battery-voltage">
        電池電壓：{{ station.occupied ? station.batteryVoltage.toFixed(1) + ' V' : '--' }}
      </div>

      <div class="voltage">
        充電電壓：{{ station.occupied ? CHARGE_VOLTAGE + ' V' : '--' }}
      </div>

      <div class="current">
        充電電流：{{ station.occupied ? CHARGE_CURRENT + ' A' : '--' }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

// === 常數設定 ===
const CHARGE_VOLTAGE = 58.0
const CHARGE_CURRENT = 10.0

// === 充電站模擬資料 ===
const stations = reactive([
  { id: 'A', name: '充電站 A', occupied: false, batteryVoltage: 0.0 },
  { id: 'B', name: '充電站 B', occupied: false, batteryVoltage: 0.0 },
  { id: 'C', name: '充電站 C', occupied: false, batteryVoltage: 0.0 }
])

// === 傳送資料到後端 ===
const sendToBackend = async (station: any) => {
  const payload = {
    station_id: station.id,
    occupied: station.occupied,
    battery_voltage: station.batteryVoltage,
    charge_voltage: CHARGE_VOLTAGE,
    charge_current: CHARGE_CURRENT
  }

  try {
    await axios.post('http://127.0.0.1:8000/update_station', payload)
    console.log(`[✅] 已送出 ${station.id}：`, payload)
  } catch (error) {
    console.error(`[❌] 傳送失敗 ${station.id}`, error)
  }
}

// === 啟動定時器，每秒更新電壓並送出資料 ===
let intervalId: number

onMounted(() => {

    axios.post('http://localhost:8000/api/reset_stations') 
    .then(() => console.log('充電站狀態已重置'))
    .catch((err) => console.error('初始化失敗', err))

  intervalId = setInterval(() => {
    stations.forEach(station => {
      if (station.occupied) {
        const fluctuation = (Math.random() - 0.5) * 0.5
        station.batteryVoltage = Math.min(58, Math.max(50, station.batteryVoltage + fluctuation))
      } else {
        station.batteryVoltage = 0.0
      }

      sendToBackend(station)
    })
  }, 1000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<style scoped>
.container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background-color: #222;
  padding: 20px;
}

.station-card {
  background-color: #fff;
  color: #000;
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 20px;
  width: 220px;
  height: 240px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.station-card h2 {
  font-size: 20px;
  margin-bottom: 16px;
}

.switch {
  margin-bottom: 10px;
}

.battery-voltage,
.voltage,
.current {
  margin-top: 8px;
  font-size: 15px;
  font-weight: 500;
}
</style>
