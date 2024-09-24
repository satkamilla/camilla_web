<template>
  <div class="service-card">
      <img :src="service.image" alt="Service Image" class="service-card__image">
      <h1 class="service-card__name">{{ service.name }}</h1>
      <p class="service-card__description">{{ service.description }}</p>
      <p class="service-card__price">{{ service.price }} рублей</p>
      <p class="service-card__usage">{{ service.usage }} раз использовано</p>
      <div class="service-card__controls">
          <button class="service-card__button" @click="orderService">Оформить заказ</button>
          <button class="service-card__button" @click="addToCart">Добавить в корзину</button>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'

const service = ref({
  image: '',
  name: '',
  description: '',
  price: 0,
  usage: 0
})

const route = useRoute()
const router = useRouter()

const fetchService = async () => {
  try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/services/${route.params.id}/`, {
          headers: {
              'Content-Type': 'application/json'
          }
      })

      if (!response.ok) {
          throw new Error('Failed to fetch service details')
      }

      const data = await response.json()
      service.value = data
  } catch (error) {
      console.error('Error fetching service details:', error)
  }
}

const addToCart = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
      alert('Авторизуйтесь сначала')
      return
  }

  try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/cart/add/', {
          method: 'POST',
          headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ service_id: service.value.id, quantity: 1 })
      })

      if (!response.ok) {
          const errorData = await response.json()
          throw new Error(`Failed to add to cart: ${errorData.detail || response.statusText}`)
      }

      const data = await response.json()
      alert('Услуга добавлена в корзину')
  } catch (error) {
      console.error('Error adding to cart:', error)
  }
}

const orderService = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
      alert('Авторизуйтесь сначала')
      return
  }

  try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/checkout/', {
          method: 'POST',
          headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ service_id: service.value.id, quantity: 1 }) // ensuring service_id and quantity are sent
      })

      if (!response.ok) {
          const errorData = await response.json()
          throw new Error(`Failed to place order: ${errorData.detail || response.statusText}`)
      }

      const data = await response.json()
      alert('Заказ оформлен успешно')
      router.push('/profile_client') // Redirect to profile or any other appropriate page
  } catch (error) {
      console.error('Error placing order:', error)
  }
}

onMounted(() => {
  fetchService()
})
</script>

<style scoped>
.service-card__controls{
  margin-top: 20px;
  display: flex;
  gap: 20px;
}
.service-card {
    width: 500px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
}

.service-card__image {
    width: 100%;
    height: 300px;
    object-fit: cover;
}

.service-card__content {
    padding: 15px;
    display: flex;
    flex-direction: column;
}

.service-card__name {
    font-size: 24px;
    font-weight: bold;
    color: #2A7CC7;
    margin: 20px 0 5px;
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

.service-card__usage .icon-usage {
    margin-right: 5px;
}

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