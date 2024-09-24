<template>
  <div class="container">
    <div class="register__wrapper">
      <h1 class="register__title">Регистрация</h1>
      <form @submit.prevent="submitForm" class="registration__form">
        <div class="registration__left">
          <label for="email">Почта</label>
          <input type="email" v-model="form.email" id="email">

          <label for="password1">Придумайте пароль</label>
          <input type="password" v-model="form.password1" id="password1">
          <div class="password__hint">Используйте 8 или более символов, состоящих из букв, цифр и символов.</div>
          <label for="password2">Повторите пароль</label>
          <input type="password" v-model="form.password2" id="password2">
          <div class="agreement-wrapper">
            <input type="checkbox" v-model="form.agreement" id="agreement" class="agreement__checkbox">
            <label for="agreement" class="agreement">Согласен с нашими Условиями использования и Политикой конфиденциальности</label>
          </div>
          <div class="radio__title">Выберите тип аккаунта</div>
          <div class="radio__buttons">
            <div class="radio__button">
              <input type="radio" v-model="form.accountType" id="is_master" value="master">
              <label for="is_master">Мастер</label>
            </div>
            <div class="radio__button">
              <input type="radio" v-model="form.accountType" id="is_client" value="client">
              <label for="is_client">Клиент</label>
            </div>
          </div>
          <button class="submit__form" type="submit">Далее</button>
          <router-link :to="'/login/'" class="go_to_another">Уже есть аккаунт? <span>Войти</span></router-link>
        </div>
        <div class="registration__right">
          <label for="first_name">Имя</label>
          <input type="text" v-model="form.first_name" id="first_name">
          <label for="last_name">Фамилия</label>
          <input type="text" v-model="form.last_name" id="last_name">
          <label for="phone_number">Номер телефона</label>
          <input type="text" v-model="form.phone_number" id="phone_number">
          <label for="city">Город</label>
          <input type="text" v-model="form.city" id="city">
        </div>
        <div v-if="errors.length" class="errors">
          <ul>
            <li v-for="error in errors" :key="error">{{ error }}</li>
          </ul>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const form = ref({
  email: '',
  password1: '',
  password2: '',
  agreement: false,
  accountType: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  city: ''
})

const errors = ref([])
const router = useRouter()

const validateForm = () => {
  errors.value = []

  if (!form.value.email) {
    errors.value.push('Email is required')
  }
  if (!form.value.password1 || form.value.password1.length < 8) {
    errors.value.push('Password must be at least 8 characters long')
  }
  if (form.value.password1 !== form.value.password2) {
    errors.value.push('Passwords do not match')
  }
  if (!form.value.agreement) {
    errors.value.push('You must agree to the terms')
  }
  if (!form.value.first_name) {
    errors.value.push('First name is required')
  }
  if (!form.value.last_name) {
    errors.value.push('Last name is required')
  }
  if (!form.value.phone_number) {
    errors.value.push('Phone number is required')
  }
  if (!form.value.city) {
    errors.value.push('City is required')
  }
  return errors.value.length === 0
}

const submitForm = async () => {
  if (!validateForm()) {
    return
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: form.value.email,
        password: form.value.password1,
        first_name: form.value.first_name,
        last_name: form.value.last_name,
        phone_number: form.value.phone_number,
        city: form.value.city,
        accountType: form.value.accountType
      })
    })

    if (response.ok) {
      const data = await response.json()
      // Handle successful registration, e.g., redirect to login page
      router.push('/login/')
    } else {
      const errorData = await response.json()
      errors.value.push(errorData.message || 'Registration failed')
    }
  } catch (error) {
    errors.value.push(error.message)
  }
}
</script>

<style scoped>


.register__wrapper{
  padding-top: 60px;
  padding-bottom: 60px;
}

.register__title {
  font-size: 32px;
  margin-bottom: 40px;
}

.registration__form {
  display: flex;
  justify-content: space-between;
}

.registration__left,
.registration__right {
  width: 46%;
}

label {
  display: block;
  margin-bottom: 15px;
  font-weight: 300;
}

input[type="email"],
input[type="password"],
input[type="text"] {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.password__hint {
  font-size: 12px;
  color: #777;
  margin-bottom: 15px;
}

input[type="checkbox"] {
  margin-right: 10px;
}

.radio__title {
  margin-top: 15px;
  margin-bottom: 5px;
  font-weight: 600;
}

.radio__buttons {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  margin-top: 10px;
}
.radio__buttons label{
  margin: 0;
}

.radio__button{
  display: flex;
  margin-right: 40px;
}
input[type="radio"] {
  margin-right: 5px;
}

.submit__form {
  background-color: rgba(42, 124, 199, 0.8);
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  display: block;
  width: 250px;
  margin-top: 20px;
}

.submit__form:hover {
  background-color: #0056b3;
}

.go_to_another {
  display: block;
  margin-top: 15px;
  font-size: 14px;
  color: #000;
  text-decoration: none;
  font-weight: 400;
}

.go_to_another span {
  text-decoration: underline;
}

.agreement-wrapper{
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.agreement {
  margin-left: 10px;
  margin: 0;
}


.errors {
  color: red;
  margin-top: 20px;
}
</style>
