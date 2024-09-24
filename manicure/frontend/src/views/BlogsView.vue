<template>
    <div class="container">
      <h1>Публикации</h1>
      <div class="blog__search">
        <input type="text" placeholder="Поиск" v-model="searchQuery">
      </div>
      <div class="blog__list">
        <BlogCard v-for="blog in filteredBlogs" :key="blog.id" :blog="blog" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import BlogCard from '@/components/BlogCard.vue'
  
  const blogs = ref([])
  const searchQuery = ref('')
  
  const fetchBlogs = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/blogs/', {
        headers: {
          'Content-Type': 'application/json'
        }
      })
  
      if (!response.ok) {
        throw new Error('Failed to fetch blogs')
      }
      const data = await response.json()
      blogs.value = data
    } catch (error) {
      console.error('Error fetching blogs:', error)
    }
  }
  
  const filteredBlogs = computed(() => {
    if (!searchQuery.value) {
      return blogs.value
    }
    return blogs.value.filter(blog => blog.title.includes(searchQuery.value))
  })
  
  onMounted(() => {
    fetchBlogs()
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
  
  .blog__search input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .blog__list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }


</style>