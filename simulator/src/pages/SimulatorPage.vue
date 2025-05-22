<script setup lang="ts">
import { reactive, onMounted, onUnmounted } from 'vue'

const CHARGE_VOLTAGE = 58.0
const CHARGE_CURRENT = 10.0

const stations = reactive([
  { id: 'A', name: '充電站 A', occupied: false, batteryVoltage: 50.0, chargeVoltage: CHARGE_VOLTAGE, chargeCurrent: CHARGE_CURRENT },
  { id: 'B', name: '充電站 B', occupied: false, batteryVoltage: 50.0, chargeVoltage: CHARGE_VOLTAGE, chargeCurrent: CHARGE_CURRENT },
  { id: 'C', name: '充電站 C', occupied: false, batteryVoltage: 50.0, chargeVoltage: CHARGE_VOLTAGE, chargeCurrent: CHARGE_CURRENT },
])

let socket: WebSocket
let intervalId: number

onMounted(() => {
  socket = new WebSocket('ws://localhost:8000/ws/station')

  socket.onopen = () => console.log('Simulator WebSocket 已連線')
  socket.onclose = () => console.log('Simulator WebSocket 已關閉')

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    const found = stations.find((s) => s.id === data.station_id)
    if (found) {
      if (typeof data.charge_voltage === 'number') found.chargeVoltage = data.charge_voltage
      if (typeof data.charge_current === 'number') found.chargeCurrent = data.charge_current
    }
  }

  intervalId = setInterval(() => {
    stations.forEach(station => {
      if (station.occupied) {
        const fluctuation = (Math.random() - 0.5) * 0.5
        station.batteryVoltage = Math.min(58, Math.max(50, station.batteryVoltage + fluctuation))
      } else {
        station.batteryVoltage = 0.0
      }

      const payload = {
        station_id: station.id,
        occupied: station.occupied,
        battery_voltage: station.batteryVoltage,
        charge_voltage: station.chargeVoltage,
        charge_current: station.chargeCurrent,
        status: station.occupied ? 'reserved' : 'none',
        error_message: ''
      }

      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(payload))
        console.log(`WebSocket 傳送資料 ${station.id}:`, payload)
      }
    })
  }, 1000)
})

onUnmounted(() => {
  clearInterval(intervalId)
  socket?.close()
})
</script>

<template>
  <div class="container">
    <div v-for="station in stations" :key="station.id" class="station-card">
      <h2>{{ station.name }}</h2>
      <div class="switch">
        <label><input type="checkbox" v-model="station.occupied" /> 站位佔用</label>
      </div>
      <div class="battery-voltage">電池電壓：{{ station.batteryVoltage.toFixed(1) }} V</div>
      <div class="voltage">充電電壓：{{ station.chargeVoltage }} V</div>
      <div class="current">充電電流：{{ station.chargeCurrent }} A</div>
    </div>
  </div>
</template>

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