<template>
  <header>
    <div class="container">
      <nav>
        <div class="nav__logo">
          NailConnect
        </div>
        <div class="burger" @click="toggleMenu">
          &#9776;
        </div>
        <ul class="nav__navigation" :class="{ open: menuOpen }">
          <li><router-link :to="'/'">Главная</router-link></li>
          <li><router-link :to="'/masters'">Мастера Маникюра</router-link></li>
          <li><router-link :to="'/messenger'">Сообщения</router-link></li>
          <li><router-link :to="'/blogs'">Публикации</router-link></li>
          <li><router-link :to="'/services'">Услуги</router-link></li>
        </ul>
        <div v-if="isAuth" :class="{ open: menuOpen }">
          <router-link :to="profileLink" class="nav__login">Личный кабинет/</router-link>
          <a @click.prevent="logout" class="nav__logout">Выйти</a>
        </div>
        <router-link v-else :to="'/login/'" class="nav__login" :class="{ open: menuOpen }">Логин/Авторизация</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth'

const { isAuth, logout, userProfile, fetchUserProfile } = useAuth()

const profileLink = computed(() => {
  if (userProfile.value) {
    return userProfile.value.is_master ? '/profile_master' : '/profile_client'
  }
  return '/profile'
})

onMounted(() => {
  fetchUserProfile()
})

const menuOpen = ref(false)
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  padding-top: 30px;
  padding-bottom: 30px;
  position: relative;
}

.burger {
  position: absolute;
  right: 20px;
  display: none;
  font-size: 30px;
  cursor: pointer;
}

.nav__navigation {
  display: flex;
}

.nav__navigation li {
  margin-right: 30px;
}

.nav__navigation li a {
  font-size: 14px;
  color: #737373;
  text-decoration: none;
  font-weight: 700;
}

.nav__logo {
  font-weight: 700;
  font-size: 24px;
}

.nav__login {
  color: #23A6F0;
  font-weight: 700;
  font-size: 14px;
  text-decoration: none;
}

.nav__logout {
  color: #23A6F0;
  font-weight: 700;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
}

@media (max-width: 375px) {
  .burger {
    display: block;
  }

  .nav__navigation {
    display: none;
    flex-direction: column;
    align-items: center;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: #fff;
    z-index: 1000;
    padding: 20px 0;
  }

  .nav__navigation.open {
    display: flex;
  }

  .nav__navigation li {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .nav__navigation li a {
    font-size: 18px;
  }

  .nav__login,
  .nav__logout {
    display: none;
    font-size: 18px;
    margin-bottom: 10px;
  }

  .nav__login.open,
  .nav__logout.open {
    display: block;
  }
}
</style>
