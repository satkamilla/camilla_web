<template>
    <section class="masters">
      <div class="container">
        <div class="masters__top">
          <h1>Мастера маникюра</h1>
          <p class="masters__subtitle">
            Эти мастера точно сделают нужный вам маникюр
          </p>
        </div>
        <div class="masters__best">
          <MasterCard v-for="master in bestMasters" :key="master.user.id" :master="master" />
        </div>
      </div>
    </section>
    <section class="search__masters">
      <div class="container">
        <div class="search__masters-top">
          <h2>Поиск мастеров</h2>
          <form action="" class="banner__search">
            <input type="text" placeholder="Искать" v-model="searchQuery" @input="filterMasters" />
          </form>
        </div>
        <div class="masters__best">
          <MasterCard v-for="master in filteredMasters" :key="master.user.id" :master="master" />
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import MasterCard from '@/components/MasterCard.vue'
  
  const bestMasters = ref([])
  const allMasters = ref([])
  const filteredMasters = ref([])
  const searchQuery = ref('')
  
  const fetchMasters = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/masters/', {
        headers: {
          'Content-Type': 'application/json'
        }
      })
  
      if (!response.ok) {
        throw new Error('Failed to fetch masters')
      }
  
      const data = await response.json()
      allMasters.value = data
      bestMasters.value = data.slice(0, 4) // Assuming the best masters are the first 4 for demo purposes
      filteredMasters.value = data
    } catch (error) {
      console.error('Error fetching masters:', error)
    }
  }
  
  const filterMasters = () => {
    filteredMasters.value = allMasters.value.filter(master => 
      master.user.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  onMounted(() => {
    fetchMasters()
  })
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
<style>
.masters{
    margin-top: 30px;
    margin-bottom: 100px;
}

.masters__top{
    text-align: center;
    margin-bottom: 60px;
}

.masters__top h1{
    font-size: 58px;
    margin-bottom: 24px;
}
.masters__subtitle{
    font-size: 20px;
}

.masters__best{
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}

.masters__master{
    width: 260px;
}

.master__image{
    margin-bottom: 10px;
}

.master__name{
    font-size: 20px;
    font-weight: 400;
    margin-bottom: 8px;
}


.master__category{
    font-size: 14px;
    font-weight: 400;
}

.search__masters-top h2{
    font-size: 37px;
    font-weight: 600;
    margin-bottom: 40px;
}
.search__masters-top form{
    width: 400px;
    height: 30px;
    margin-bottom: 50px;
    font-size: 20px;
}
.search__masters-top input{
    width: 100%;
    height: 100%;
    padding: 10px;
    border-radius: 5px;
    font-size: 20px;
    border: 1px solid #AFB8CF;
}
</style>