<script setup lang="js">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth'

const slides = [
  {
    image: '/img/banners/slide1.jpg',
    title: 'Сервис для маникюра',
    subtitle: 'Искали где сделать маникюр? Вы попали в нужное для вас место!'
  },
  {
    image: '/img/banners/slide2.jpg',
    title: 'Сервис для маникюра',
    subtitle: 'Искали где сделать маникюр? Вы попали в нужное для вас место!'
  },
  {
    image: '/img/banners/slide3.jpg',
    title: 'Сервис для маникюра',
    subtitle: 'Искали где сделать маникюр? Вы попали в нужное для вас место!'
  }
];

const currentSlide = ref(0);
const router = useRouter();

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length;
};

// Интервал для автоматического переключения слайдов
let intervalId;

const { isAuth, logout, userProfile, fetchUserProfile } = useAuth()

const profileLink = computed(() => {
  if (userProfile.value) {
    return userProfile.value.is_master ? '/profile_master' : '/profile_client'
  }
  return '/profile'
})

onMounted(() => {
  fetchUserProfile()
  intervalId = setInterval(nextSlide, 7000);
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<template>
  <section class="banner__slider">
    <div class="banner__slide" v-for="(slide, index) in slides" :key="index" :class="{ active: index === currentSlide }">
      <img :src="slide.image" :alt="'Slide ' + (index + 1)">
      <div class="banner__container">
        <div class="banner__slide-content">
          <h1>{{ slide.title }}</h1>
          <h3>{{ slide.subtitle }}</h3>
        </div>
      </div>
    </div>
  </section>
  <section class="whosec">
    <div class="container">
      <div class="who__wrapper">
        <div class="who who__client">
          <h3>Для клиентов</h3>
          <h2>Время <br>ноготочек</h2>
          <router-link :to="profileLink">Перейти в кабинет</router-link>
        </div>
        <div class="who who__master">
          <h3>Для мастеров маникюра</h3>
          <h2>Больше <br>возможностей</h2>
          <router-link :to="profileLink">Перейти в кабинет</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.banner__slider{
    margin-bottom: 80px;
}
.banner__slide{
    position: relative;
    height: 590px;
    max-width: 100%;
    width: 100vw;
    overflow-y: hidden;
}
.banner__slide img{
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    width: 100%;
}
.banner__container{
    color: #fff;
    position: absolute;
    z-index: 2;
    top: 200px;
    left: 0; 
    right: 0; 
    margin-left: auto; 
    margin-right: auto; 
    text-align: center;
    max-width: 710px;
}

.banner__slide-content h1{
    font-size: 58px;
    margin-bottom: 24px;
}

.banner__slide-content h3{
    font-weight: 400;
    font-size: 20px;
    margin-bottom: 30px;
}

.banner__search{
    margin: 0 auto;
    position: relative;
    width: 510px;
    height: 50px;
    border: 1px solid #E6E6E6;
    border-radius: 15px;
}
.banner__search input{
    position: absolute;
    left: 0;
    top: 0;
    font-size: 14px;
    height: 48px;
    border: none;
    width: 450px;
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;
    padding-left: 15px;
    outline: none;
    padding-right: 20px;
}

.banner__search button{
    position: absolute;
    right: 0;
    top: 0;
    background-color: #23A6F0;
    border: none;
    text-align: center;

    height: 50px;
    width: 60px;
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
}
.banner__search button img{
    width: 18px;
    margin-top: 30%;
    transform: translateY(-50%);
    margin-left: 50%;
    transform: translateX(-50%);
}
.banner__slide {
  display: none;
}

.banner__slide.active {
  display: block;
}
.who__wrapper{
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.get__wrapper{
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.whosec{
    margin-bottom: 80px;
}

.who{
    width: 510px;
    max-height: 300px;
    padding-left: 50px;
    padding-top: 65px;
    padding-bottom: 70px;
    background-size: cover;
    background-repeat: no-repeat;
}

.get{
    width: 50%;
    height: 434px;
    padding-top: 56px;
    padding-left: 66px;
    background-size: cover;
    background-repeat: no-repeat;
    padding-top: 90px;
}
.get h2{
    margin-bottom: 50px;
    font-size: 58px;
    line-height: 75px;
}
.get h3{
    margin-bottom: 150px;
    font-size: 20px;
}

.get a{
    padding: 25px 60px;
    text-decoration: none;

}
.who h3{
    margin-bottom: 20px;
    font-size: 25px;
}

.get__orders{
    color: #fff;
}

.get__orders a{
    color: #fff;
    border: 1px solid #Fff;
}

.get__masters{
    color: #252b42;
}

.get__masters a{
    color: #252b42;
    border: 1px solid #252b42;
}


.who__client h3{
    color: #fff;
}
.who__master h3{
    color: #E77C40;
}
.who h2{
    margin-bottom: 30px;
    font-size: 32px;
}

.who a{
    text-decoration: underline;
    color: #252b42;
    font-size: 14px;
}

.who__client{
    background-image: url(../img/who/1.jpg);
}

.get__orders{
    background-image: url(../img/get/1.jpg);

}

.who__master{
    background-image: url(../img/who/2.jpg);

}


@media (max-width: 375px) {
  .banner__container {
    top: 100px;
    max-width: 90%;
  }
  .banner__slider{
    margin-bottom: 20px;
  }

  .banner__slide-content{
    margin-top: -50px;
  }

  .banner__slide{
    height: 150px;
  }

  .banner__slide img{
    object-fit: contain;
  }

  .banner__slide-content h1 {
    font-size: 24px;
    margin-bottom: 12px;
  }

  .banner__slide-content h3 {
    font-size: 14px;
    margin-bottom: 15px;
  }

  .banner__search {
    width: 90%;
    height: 40px;
  }

  .banner__search input {
    font-size: 12px;
    height: 38px;
    width: calc(100% - 40px);
  }

  .banner__search button {
    height: 40px;
    width: 40px;
  }

  .who__wrapper {
    flex-direction: column;
    align-items: center;
  }

  .who {
    width: 90%;
    padding: 20px;
    text-align: center;
    margin-bottom: 30px;
  }

  .who h2 {
    font-size: 24px;
  }

  .who h3 {
    font-size: 18px;
  }

  .who a {
    font-size: 12px;
  }
}
</style>