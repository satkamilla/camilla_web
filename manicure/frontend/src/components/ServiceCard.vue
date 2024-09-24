<template>
    <div class="service-card">
      <img :src="service.image" alt="Service Image" class="service-card__image">
      <div class="service-card__content">
        <h3 class="service-card__title">{{ service.name }}</h3>
        <p class="service-card__subtitle">{{ service.subtitle }}</p>
        <p class="service-card__description">{{ service.description }}</p>
        <p class="service-card__usage"><i class="icon-usage"></i> {{ service.usage }} раз использовано</p>
        <p class="service-card__price">{{ service.price }} рублей</p>
        <router-link :to="`/services/${service.id}`" class="service-card__button">Узнать подробнее</router-link>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    service: Object
  })
  </script>



<style scoped>

.service-card {
    width: 333px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
}

.service-card__image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.service-card__content {
    padding: 15px;
    display: flex;
    flex-direction: column;
}

.service-card__title {
    font-size: 16px;
    font-weight: bold;
    color: #2A7CC7;
    margin: 10px 0 5px;
}

.service-card__subtitle {
    font-size: 14px;
    font-weight: bold;
    margin: 5px 0;
    color: #333;
}

.service-card__description {
    font-size: 14px;
    color: #555;
    margin: 5px 0;
}

.service-card__usage {
    font-size: 14px;
    color: #333;
    margin: 5px 0;
    display: flex;
    align-items: center;
}

/* .service-card__usage .icon-usage {
} */

.service-card__price {
    font-size: 18px;
    font-weight: bold;
    color: #28a745;
    margin: 10px 0;
}

.service-card__button {
    padding: 10px 20px;
    background: transparent;
    color: #2A7CC7;
    border: 2px solid #2A7CC7;
    border-radius: 4px;
    cursor: pointer;
    text-align: center;
    transition: background-color 0.3s, color 0.3s;
}

.service-card__button:hover {
    background-color: #007bff;
    color: #fff;
}

</style>