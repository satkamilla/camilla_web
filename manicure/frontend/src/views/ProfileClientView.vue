<template>
  <div class="container">
    <div class="profile">
      <div class="profile__header">
        <img :src="profile.picture" alt="Profile Picture" class="profile__picture">
        <div class="profile__info">
          <h1 class="profile__name">{{ profile.name }}</h1>
          <p class="profile__location">{{ profile.location }}</p>
          <p class="profile__bio">{{ profile.bio || 'Нет описания' }}</p>
          <router-link to="/profile_edit/" class="profile__edit">Редактировать профиль</router-link>
        </div>
      </div>
      <button class="profile__message">Перейти к сообщениям</button>
    </div>
    <div class="profile__cart">
      <div class="profile__cart-title">Корзина</div>
      <div class="services-list">
        <ServiceCard v-for="item in cart.items" :key="item.service.id" :service="item.service" />
      </div>
      <div class="profile__cart-buy">
        <div class="profile__cart-price">{{ calculateTotalPrice() }} р</div>
        <button class="profile__cart-button" @click="placeOrder">Оформить заказ</button>
      </div>
    </div>
    <div class="profile__history">
      <div class="profile__history-title">История покупок</div>
      <div class="history-list">
       <HistoryCard v-for="order in orders" :key="order.id" :order="order" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ServiceCard from '@/components/ServiceCard.vue'
import HistoryCard from '@/components/HistoryCard.vue'

const profile = ref({
  picture: '',
  name: '',
  location: '',
  bio: ''
})

const cart = ref({
  items: []
})

const orders = ref([])

const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch('http://127.0.0.1:8000/api/v1/profile/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized - Invalid token');
      }
      throw new Error('Failed to fetch profile');
    }

    const data = await response.json();
    profile.value = data;
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

const fetchCart = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch('http://127.0.0.1:8000/api/v1/cart/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized - Invalid token');
      }
      throw new Error('Failed to fetch cart');
    }

    const data = await response.json();
    cart.value = data;
  } catch (error) {
    console.error('Error fetching cart:', error);
  }
};

const fetchOrderHistory = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch('http://127.0.0.1:8000/api/v1/orders/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized - Invalid token');
      }
      throw new Error('Failed to fetch order history');
    }

    const data = await response.json();
    orders.value = data;
  } catch (error) {
    console.error('Error fetching order history:', error);
  }
};

const placeOrder = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch('http://127.0.0.1:8000/api/v1/checkout/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized - Invalid token');
      }
      throw new Error('Failed to place order');
    }

    const data = await response.json();
    alert('Заказ оформлен успешно');
    await fetchCart(); // Refresh the cart
    await fetchOrderHistory(); // Refresh the order history
  } catch (error) {
    console.error('Error placing order:', error);
  }
};

const calculateTotalPrice = () => {
  return cart.value.items.reduce((total, item) => total + item.service.price * item.quantity, 0);
};

onMounted(async () => {
  await fetchProfile();
  await fetchCart();
  await fetchOrderHistory();
});
</script>

<style scoped>
.container {
  width: 1220px;
  margin: 0 auto;
  padding: 20px;
}

.profile {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: left;
}

.profile__header {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
}

.profile__picture {
  width: 200px;
  object-fit: cover;
  margin-right: 40px;
}

.profile__info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.profile__name {
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 10px;
}

.profile__location {
  margin-bottom: 20px;
}

.profile__bio {
  margin: 0 0 5px;
  font-weight: 400;
}

.profile__edit {
  display: inline-block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
}

.profile__message {
  padding: 10px 20px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  width: 200px;
}

.cart__title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}

.cart {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.cart__item {
  width: 30%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cart__image {
  width: 100%;
  border-radius: 8px;
  object-fit: cover;
  margin-bottom: 15px;
}

.cart__details {
  text-align: center;
}

.cart__name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.cart__description {
  margin-bottom: 10px;
  font-size: 14px;
  color: #555;
}

.cart__usage,
.cart__price {
  margin-bottom: 10px;
  font-size: 14px;
  color: #333;
}

.cart__button {
  background: #007bff;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cart__controls {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
}

.cart__controls button {
  background: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.cart__controls span {
  margin: 0 10px;
  font-size: 16px;
}

.cart__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.cart__total {
  font-size: 18px;
  font-weight: bold;
}

.cart__checkout,
.cart__add {
  background: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cart__add {
  background: transparent;
  color: #007bff;
  border: 2px solid #007bff;
}

.profile__cart-title {
  font-size: 32px;
  font-weight: bold;
  margin-top: 55px;
  margin-bottom: 55px;

}

.profile__history-title {
  font-size: 32px;
  font-weight: bold;
  margin-top: 55px;
  margin-bottom: 55px;
}

.profile__cart-buy {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 30px;
}

.profile__cart-price {
  font-size: 24px;
  color: #333;
  margin-right: 30px;
}

.profile__cart-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 45px;
  background: #2A7CC7;
  font-size: 16px;
  color: #fff;
  border: none;
  border-radius: 40px;
}

.services-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
</style>
