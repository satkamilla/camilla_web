<template>
  <div class="container">
      <div class="blog__content" v-if="blog">
          <div class="blog__timestamp">{{ formatTimestamp(blog.created_at) }}</div>
          <div class="blog__title">{{ blog.title }}</div>
          <div class="blog__image"><img :src="blog.image" alt=""></div>
          <div class="blog__text">{{ blog.content }}</div>
          <div class="blog__author">
              <div class="blog__author-photo">
                  <img :src="blog.master.user.picture" alt="Author Photo">
              </div>
              <div class="blog__author-name">{{ blog.master.user.name }}</div>
          </div>
      </div>
      <div class="blog__comment-form">
          <form @submit.prevent="submitComment">
              <div class="blog__comment-form-title">Оставьте комментарий</div>
              <div class="blog__comment-form-input">
                  <input type="text" v-model="newComment" placeholder="Введите комментарий">
              </div>
              <button type="submit">Отправить</button>
          </form>
      </div>
      <div class="blog__comments" v-if="comments.length">
          <Comment v-for="comment in comments" :key="comment.id" :comment="comment" />
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Comment from '@/components/Comment.vue'

const blog = ref(null)
const comments = ref([])
const newComment = ref('')
const route = useRoute()
const blogId = route.params.id

const fetchBlog = async () => {
  try {
      console.log('Fetching blog...')
      const response = await fetch(`http://127.0.0.1:8000/api/v1/blogs/${blogId}/`, {
          headers: {
              'Content-Type': 'application/json'
          }
      })

      if (!response.ok) {
          throw new Error('Failed to fetch blog')
      }

      const data = await response.json()
      console.log('Fetched blog data:', data)
      blog.value = data
      comments.value = data.comments
  } catch (error) {
      console.error('Error fetching blog:', error)
  }
}

const submitComment = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
      alert('Авторизуйтесь сначала')
      return
  }

  console.log('Submitting comment:', newComment.value, 'for blog:', blogId)

  try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/blogs/${blogId}/comments/`, {
          method: 'POST',
          headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ content: newComment.value, blog: blogId })
      })

      if (!response.ok) {
          const errorData = await response.json()
          console.log('Error response data:', errorData)
          throw new Error(`Failed to add comment: ${errorData.detail || response.statusText}`)
      }

      const data = await response.json()
      console.log('Comment added:', data)
      comments.value.push(data)
      newComment.value = ''
      alert('Комментарий успешно добавлен')
  } catch (error) {
      console.error('Error adding comment:', error)
  }
}

onMounted(() => {
  fetchBlog()
})

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleDateString([], { year: 'numeric', month: 'numeric', day: 'numeric' })
}
</script>
<style>

    .blog__timestamp{
        color: #2A7CC7;
        font-size: 16px;
        font-weight: 400;
        margin-bottom: 20px;
    }
    .blog__title{
        font-size: 36px;
        color: #333;
        font-weight: 700;
        margin-bottom: 40px;
    }
    .blog__image{
        text-align: center;
    }
    .blog__image img{
        height: 500px;
        margin-bottom: 50px;
    }

    .blog__text{
        font-size: 18px;
        font-weight: 400;
        line-height: 1.5;
        margin-bottom: 50px;
    }

    .blog__author{
        display: flex;
        align-items: center;
        margin-bottom: 50px;
    }

    .blog__author-photo{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 20px;
    }
    .blog__author-photo img{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 20px;
    }
    .blog__author-name{
        font-size: 18px;
        font-weight: 700;
    }
    .blog__comment-form{
      margin-bottom: 30px;
    }
    .blog__comment-form-title{
      font-size: 32px;
      font-weight: 700;
      margin-bottom: 20px;

    }
    .blog__comment-form-input input{
        width: 500px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #AFB8CF;
    }
    .blog__comment-form button{
      margin-top: 10px;
      background-color: transparent;
      border: 1px solid #2A7CC7;
      color: #333;
      font-size: 16px;
      padding: 5px 10px;
    }
</style>