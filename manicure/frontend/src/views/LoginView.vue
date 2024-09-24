<template>
  <div class="container">
    <div class="login__wrapper">
      <h1 class="login__title">Войти в аккаунт</h1>
      <form @submit.prevent="submitForm" class="login__form">
        <div class="login__left">
          <label for="email">Почта</label>
          <input type="email" v-model="form.email" id="email">

          <label for="password1">Пароль</label>
          <input type="password" v-model="form.password" id="password">

          <div class="agreement-wrapper">
            <input type="checkbox" v-model="form.agreement" id="agreement" class="agreement__checkbox">
            <label for="agreement" class="agreement">Согласен с нашими Условиями использования и Политикой
              конфиденциальности</label>
          </div>

          <div v-if="errors.length" class="errors">
            <ul>
              <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
          </div>

          <button class="submit__form" type="submit">Далее</button>
          <router-link :to="'/register/'" class="go_to_another">Еще нет аккаунта?
            <span>Зарегистрироваться</span></router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'

const form = ref({
  email: '',
  password: '',
  agreement: false,
})

const errors = ref([])
const router = useRouter()
const { login } = useAuth()

const validateForm = () => {
  errors.value = []

  if (!form.value.email) {
    errors.value.push('Обязательное поле "Почта"')
  }
  if (!form.value.password || form.value.password.length < 8) {
    errors.value.push('Пароль должен быть минимум 8 символов')
  }
  if (!form.value.agreement) {
    errors.value.push('Вы должны согласиться с нашими Условиями использования и Политикой конфиденциальности')
  }
  return errors.value.length === 0
}

const submitForm = async () => {
  if (!validateForm()) {
    return
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: form.value.email,
        password: form.value.password
      })
    })

    if (response.ok) {
      const data = await response.json()
      login(data)
      // Handle successful login, e.g., redirect to the home page
      router.push('/')
    } else {
      const errorData = await response.json()
      errors.value.push(errorData.detail || 'Login failed')
    }
  } catch (error) {
    errors.value.push(error.message)
  }
}
</script>
<style scoped>
.login__wrapper {
  padding-top: 60px;
  padding-bottom: 60px;
}

.login__title {
  font-size: 32px;
  margin-bottom: 40px;
}

.login__form {
  display: flex;
  justify-content: space-between;
}

.login__left {
  width: 500px;
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
  margin-bottom: 25px;
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

.radio__buttons label {
  margin: 0;
}

.radio__button {
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

.agreement-wrapper {
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

@media (max-width: 375px) {
  .login__wrapper {
    padding-top: 30px;
    padding-bottom: 30px;
  }

  .login__title {
    font-size: 24px;
    margin-bottom: 20px;
    text-align: center;
  }

  .login__form {
    flex-direction: column;
    align-items: center;
  }

  .login__left {
    width: 100%;
    padding: 0 10px;
  }

  label {
    font-size: 14px;
    margin-bottom: 10px;
  }

  input[type="email"],
  input[type="password"],
  input[type="text"] {
    font-size: 14px;
    padding: 6px;
    margin-bottom: 15px;
  }

  .submit__form {
    width: 100%;
    padding: 10px;
    font-size: 14px;
  }

  .go_to_another {
    font-size: 12px;
    text-align: center;
  }

  .agreement-wrapper {
    flex-direction: column;
    align-items: flex-start;
  }

  .agreement {
    margin-left: 0;
    margin-top: 10px;
    font-size: 12px;
  }

  .errors {
    font-size: 12px;
  }
}
</style>
