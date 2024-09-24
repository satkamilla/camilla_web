<template>
    <router-link :to="`/masters/${master.user.id}`" class="masters__master">
      <div class="master__image"><img :src="master.user.picture" alt=""></div>
      <div class="master__name">{{ master.user.name }}</div>
      <div class="master__category">{{ master.description }}</div>
    </router-link>
</template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    master: {
      type: Object,
      required: true
    }
  })
  </script>
  
  <style scoped>
  .masters__master{
    color: #333;
    text-decoration: none;
  }
  .master__image{
    width: 240px;
  }
  .master__image img{
    width: 240px;
  }
  </style>
  