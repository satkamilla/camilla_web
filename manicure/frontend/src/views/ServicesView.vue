<template>
    <div class="container">
      <h1>Услуги</h1>
      <div class="service__search">
        <input type="text" placeholder="Поиск" v-model="searchQuery">
      </div>
      <div class="service__categories">
        <button v-for="category in categories" :key="category.id" @click="filterByCategory(category.name)">
          {{ category.name }}
        </button>
      </div>
      <div class="service__list">
        <ServiceCard v-for="service in filteredServices" :key="service.id" :service="service" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import ServiceCard from '@/components/ServiceCard.vue'
  
  const services = ref([])
/*   const categories = ref([
    { id: 1, name: 'Маникюр' },
    { id: 2, name: 'Педикюр' },
    { id: 3, name: 'Стокфиш' }
  ]) */
  const searchQuery = ref('')
  
  const fetchServices = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/services/', {
        headers: {
          'Content-Type': 'application/json'
        }
      })
  
      if (!response.ok) {
        throw new Error('Failed to fetch services')
      }
      const data = await response.json()
      services.value = data
    } catch (error) {
      console.error('Error fetching services:', error)
    }
  }
  
  const filterByCategory = (category) => {
    searchQuery.value = category
  }
  
  const filteredServices = computed(() => {
    if (!searchQuery.value) {
      return services.value
    }
    return services.value.filter(service => service.name.includes(searchQuery.value))
  })
  
  onMounted(() => {
    fetchServices()
  })
  </script>
  
  <style scoped>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  h1 {
    font-size: 2rem;
    margin-bottom: 20px;
  }
  
  .service__search input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .service__categories {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .service__categories button {
    padding: 10px 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background: none;
    cursor: pointer;
  }
  
  .service__categories button:hover {
    background-color: #f0f0f0;
  }
  
  .service__list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .service__card {
    width: calc(33.333% - 20px);
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 10px;
    background-color: #fff;
  }
  
  .service__image {
    width: 100%;
    height: auto;
  }
  
  .service__title {
    font-size: 1.5rem;
    margin: 10px 0;
  }
  
  .service__description {
    font-size: 1rem;
    color: #666;
    margin-bottom: 10px;
  }
  
  .service__info {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 10px;
  }
  
  .service__usage,
  .service__price {
    font-size: 1rem;
    font-weight: bold;
  }
  
  .service__link {
    margin-top: auto;
    padding: 10px 20px;
    border: 1px solid #007bff;
    border-radius: 5px;
    background-color: #007bff;
    color: #fff;
    text-decoration: none;
    transition: background-color 0.3s;
  }
  
  .service__link:hover {
    background-color: #0056b3;
  }
  </style>
  