<template>
  <div class="container" v-if="profile">
    <div class="profile">
      <div class="profile__header">
        <img :src="profile.user.picture" alt="Profile Picture" class="profile__picture">
        <div class="profile__info">
          <h1 class="profile__name">{{ profile.user.name }}</h1>
          <p class="profile__location">{{ profile.user.location }}</p>
          <p class="profile__bio">{{ profile.user.bio || 'Нет описания' }}</p>
        </div>
      </div>
      <button class="profile__message" @click="goToMessages">Перейти к сообщениям</button>
    </div>
    <nav class="profile__chapters">
      <div class="nav__controls">
        <button @click="showServices">Услуги</button>
        <button @click="showBlogs">Публикации</button>
        <button @click="showReviews">Отзывы</button>
      </div>
      <div class="profile__blogs" v-if="activeTab === 'blogs'">
        <div class="container">
          <div class="profile__blogs-content">
            <BlogCard v-for="blog in profile.blogs || []" :key="blog.id" :blog="blog" />
          </div>
        </div>
      </div>
      <div class="profile__services" v-if="activeTab === 'services'">
        <div class="container">
          <div class="profile__services-content">
            <ServiceCard v-for="service in profile.services || []" :key="service.id" :service="service" />
          </div>
        </div>
      </div>
      <div class="profile__comment-form">
        <form @submit.prevent="submitComment">
          <div class="profile__comment-form-title">Оставьте комментарий</div>
          <div class="profile__comment-form-input">
            <input type="text" v-model="newComment" placeholder="Введите комментарий">
          </div>
          <button type="submit">Отправить</button>
        </form>
      </div>
      <div class="profile__reviews" v-if="activeTab === 'reviews'">
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <div class="comment__header">
            <div class="comment__photo">
              <img :src="comment.author.picture" alt="Author Photo">
            </div>
            <div class="comment__username">{{ comment.author.name }}</div>
          </div>
          <div class="comment__text">{{ comment.content }}</div>
          <div class="comment__date">{{ formatTimestamp(comment.created_at) }}</div>

        </div>
      </div>
    </nav>

  </div>
  <div v-else>Loading...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BlogCard from '@/components/BlogCard.vue'
import ServiceCard from '@/components/ServiceCard.vue'

const profile = ref(null)
const comments = ref([])
const newComment = ref('')
const activeTab = ref('services')
const route = useRoute()
const router = useRouter()
const userId = route.params.id

const fetchProfile = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/masters/${userId}/`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch profile')
    }

    const data = await response.json()
    profile.value = data
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

const fetchComments = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/profiles/${userId}/comments/all/`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch comments')
    }

    const data = await response.json()
    comments.value = data
  } catch (error) {
    console.error('Error fetching comments:', error)
  }
}

const submitComment = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Авторизуйтесь сначала')
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/profiles/${userId}/comments/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content: newComment.value, profile: userId })
    })

    if (!response.ok) {
      const errorData = await response.json()
      console.log('Error response data:', errorData)
      throw new Error(`Failed to add comment: ${errorData.detail || response.statusText}`)
    }

    const data = await response.json()
    comments.value.push(data)
    newComment.value = ''
    alert('Комментарий успешно добавлен')
  } catch (error) {
    console.error('Error adding comment:', error)
  }
}

const showServices = () => {
  activeTab.value = 'services'
}

const showBlogs = () => {
  activeTab.value = 'blogs'
}

const showReviews = () => {
  activeTab.value = 'reviews'
}



const goToMessages = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://127.0.0.1:8000/api/v1/conversations/create_or_get/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ other_user_id: userId })
    })

    if (!response.ok) {
      throw new Error('Failed to create or get conversation')
    }

    const data = await response.json()
    router.push(`/messenger`)
  } catch (error) {
    console.error('Error creating or getting conversation:', error)
  }
}

onMounted(() => {
  fetchProfile()
  fetchComments()
  showServices() // Default to showing services
})

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleDateString([], { year: 'numeric', month: 'numeric', day: 'numeric' })
}
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


.profile__chapters {
  text-align: center;
  margin-top: 40px;
}

.nav__controls {
  margin: 0 auto;
  width: 600px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 40px;
}

.nav__controls button {
  background-color: transparent;
  border: none;
  font-size: 20px;
  font-weight: 400;
  cursor: pointer;
}

.profile__comment-form {
  margin-bottom: 30px;
  text-align-last: left;
}

.profile__comment-form-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 20px;

}

.profile__comment-form-input input {
  width: 500px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #AFB8CF;
}

.profile__comment-form button {
  margin-top: 10px;
  background-color: transparent;
  border: 1px solid #2A7CC7;
  color: #333;
  font-size: 16px;
  padding: 5px 10px;
}

.comment {
  padding: 10px;
  border: 1px solid #D8DADC;
  margin-bottom: 15px;
  text-align: left;
}

.comment__wrapper {
  width: 100%;
  border: 1px solid #D8DADC;
  border-radius: 10px;
  padding: 20px;
}

.comment__header {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}

.comment__photo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.comment__photo img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.comment__username {
  margin-left: 20px;
  font-weight: bold;
  font-size: 18px;
}

.comment__text {
  font-weight: 400;
  font-size: 16px;
  margin-bottom: 10px;
}
</style>