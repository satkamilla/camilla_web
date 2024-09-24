<template>
    <router-link :to="`/blogs/${blog.id}`" class="blog__card">
      <div class="blog__card-image">
        <img :src="blog.image" alt="Blog Image">
      </div>
      <div class="blog__info">
        <div class="blog__cardauthor">{{ blog.master.user.name }}</div>
        <div class="blog__date">{{ new Date(blog.created_at).toLocaleDateString() }}</div>
      </div>
      <div class="blog__title">{{ blog.title }}</div>
      <div class="blog__text">{{ blog.content }}</div>
    </router-link>
  </template>
  
  <script setup>
  defineProps({
    blog: Object
  })
  </script>
  

<style scoped>
    .blog__card{
        max-width: 330px;
        padding: 10px;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        align-items: left;
        text-decoration: none;
        
    }
    .blog__card-image{
        margin-bottom: 32px; 
        max-width: 330px;  
        max-height: 200px;
    }
    .blog__card-image img{
        max-width: 330px;
        max-height: 200px;
        object-fit: contain;
    }
    .blog__info{
        display: flex;
        margin-bottom: 12px;
        color: #007bff;
        font-size: 14px;
    }
    .blog__cardauthor{
        margin-right: 10px;
    }
    
    .blog__title{
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 12px;

        color: #000;
        
    }
    .blog__text{
        color: #667085;
        font-size: 16px;
        font-weight: 400;
    }
    
    </style>