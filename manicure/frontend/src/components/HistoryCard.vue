<template>
    <div class="history-card">
      <div class="history__card-title">
        Покупка услуги: {{ order.service_name }}
      </div>
      <div class="history__card-date">
        {{ formatTimestamp(order.created_at) }}
      </div>
      <div class="history__card-price">
        {{ order.total_price }} р
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    order: {
      type: Object,
      required: true
    }
  })
  
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleDateString('ru-RU', { year: 'numeric', month: 'long', day: 'numeric' })
  }
  </script>
  
<style scoped>

.history-card {
    width: 500px;
    padding: 20px;

    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
}

.history__card-title {
    font-size: 20px;
    font-weight: bold;
    color: #2A7CC7;
    margin: 10px 0 5px;
}

.history__card-date {
    font-size: 18px;
    font-weight: bold;
    margin: 5px 0;
    color: #333;
}

.history__card-price {
    font-size: 22px;
    font-weight: bold;
    margin: 5px 0;
    color: #333;
}


</style>