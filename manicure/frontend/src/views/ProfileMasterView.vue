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
  </div>
  <div class="container">
    <div class="profile__addcontrols">
      <router-link :to="'/blog_create/'" class="profile__addcontrol">Добавить публикацию</router-link>
      <router-link :to="'/service_create/'" class="profile__addcontrol">Добавить услугу</router-link>
    </div>
  </div>
  <div class="profile__blogs">
    <div class="container">
      <div class="profile__blogs-title">
        Публикации
      </div>
      <div class="profile__blogs-content">
        <BlogCard v-for="blog in blogs" :key="blog.id" :blog="blog" />

      </div>
    </div>
  </div>
  <div class="profile__services">
    <div class="container">
      <div class="profile__services-title">
        Услуги
      </div>
      <div class="profile__services-content">
        <ServiceCard v-for="service in services" :key="service.id" :service="service" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ServiceCard from '@/components/ServiceCard.vue'
import BlogCard from '@/components/BlogCard.vue'

const profile = ref({
  picture: '',
  name: '',
  location: '',
  bio: ''
})

const services = ref([])
const blogs = ref([])

const getServices = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch('http://127.0.0.1:8000/api/v1/user-services/', {
      headers: {
        'Authorization': `Bearer ${token}`,
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

const getBlogs = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch('http://127.0.0.1:8000/api/v1/master-blogs/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized - Invalid token');
      }
      throw new Error('Failed to fetch blogs');
    }

    const data = await response.json();
    blogs.value = data;
  } catch (error) {
    console.error('Error fetching blogs:', error);
  }
};

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

onMounted(async () => {
  await fetchProfile()
  await getServices()
  await getBlogs()
})
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

.profile__blogs-title {
  font-size: 32px;
  margin-bottom: 30px;
}

.profile__blogs-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.profile__services-title {
  font-size: 32px;
  margin-bottom: 30px;
}

.profile__services-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.profile__addcontrols {
  display: flex;

}

.profile__addcontrols {
  display: flex;
  gap: 30px;
  /* Adjust the space between the buttons as needed */
}

.profile__addcontrol {
  position: relative;
  display: flex;
  align-items: center;
  padding-left: 40px;
  /* Space for the icon */
  text-decoration: none;
  color: black;
  /* Adjust text color as needed */
  font-size: 16px;
  /* Adjust font size as needed */
}

.profile__addcontrol::before {
  content: '+';
  position: absolute;
  left: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #d3d3d3;
  /* Adjust circle color as needed */
  display: flex;
  justify-content: center;
  align-items: center;
  color: black;
  /* Adjust plus sign color as needed */
  font-size: 16px;
  /* Adjust plus sign size as needed */
}
</style>