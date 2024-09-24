<template>
    <div class="container">
      <div class="profile">
        <h1>Редактировать профиль</h1>
        <form @submit.prevent="submitForm" class="profile__form">
          <div class="form__top">
            <div class="profile-picture-block">
              <img :src="form.profile_picture_preview || defaultProfilePicture" alt="Profile Picture" class="profile-picture">
              <label for="profile-picture" class="profile__label">Фотография профиля</label>
              <input type="file" id="profile-picture" class="profile__input" @change="handleFileUpload">
            </div>
            <div class="form__right">
              <div class="form-group">
                <div class="form-group-element">
                  <label for="first_name">Имя</label>
                  <input type="text" id="first_name" v-model="form.first_name" :placeholder="placeholders.first_name">
                </div>
                <div class="form-group-element">
                  <label for="last_name">Фамилия</label>
                  <input type="text" id="last_name" v-model="form.last_name" :placeholder="placeholders.last_name">
                </div>
              </div>
              <label for="email">Почта</label>
              <input type="text" id="email" class="form__email" v-model="form.email" readonly>
            </div>
          </div>
          <div class="form__body">
            <label for="city">Город</label>
            <input type="text" id="city" v-model="form.city" :placeholder="placeholders.city">
            <label for="phone_number">Контактный номер</label>
            <input type="text" id="phone_number" v-model="form.phone_number" :placeholder="placeholders.phone_number">
            <label for="bio">О себе</label>
            <textarea id="bio" rows="4" v-model="form.bio" :placeholder="placeholders.bio"></textarea>
          </div>
          <div class="profile__controls">
            <button type="button" @click="cancelEdit" class="profile__cancel profile-btn">Отменить</button>
            <button type="submit" class="profile__submit profile-btn">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup lang="js">
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const defaultProfilePicture = ''
  
  const form = ref({
    profile_picture: '',
    profile_picture_preview: '',
    first_name: '',
    last_name: '',
    email: '',
    city: '',
    phone_number: '',
    bio: ''
  })
  
  const placeholders = ref({
    first_name: '',
    last_name: '',
    city: '',
    phone_number: '',
    bio: ''
  })
  
  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch('http://127.0.0.1:8000/api/v1/profile/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
  
      if (!response.ok) {
        throw new Error('Failed to fetch profile')
      }
  
      const data = await response.json()
      console.log(data);
      form.value = {
        profile_picture: '',
        profile_picture_preview: data.picture || defaultProfilePicture,
        first_name: data.name.split(' ')[0],
        last_name: data.name.split(' ')[1] || '',
        email: data.email,
        city: data.location || '',
        phone_number: data.phone_number,
        bio: data.bio || "Расскажите о себе",
        is_master: data.is_master

      }
  
      placeholders.value = {
        first_name: data.name.split(' ')[0],
        last_name: data.name.split(' ')[1] || '',
        city: data.location || '',
        phone_number: '',
        bio: data.bio || "Расскажите о себе"
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
    }
  }
  
  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    const reader = new FileReader()
    reader.onload = () => {
      form.value.profile_picture_preview = reader.result
      form.value.profile_picture = file
    }
    reader.readAsDataURL(file)
  }
  
  const submitForm = async () => {
    const token = localStorage.getItem('access_token')
    const formData = new FormData()
    formData.append('first_name', form.value.first_name)
    formData.append('last_name', form.value.last_name)
    formData.append('city', form.value.city)
    formData.append('description', form.value.bio)
    if (form.value.profile_picture) {
      formData.append('profile_picture', form.value.profile_picture)
    }
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/profile/update/', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })
  
      if (!response.ok) {
        throw new Error('Failed to update profile')
      }
  
      const data = await response.json()
      console.log('Profile updated:', data)
      // Optionally navigate to the profile page
      if (form.value.is_master) {
        router.push('/profile_master')
      } else {
        router.push('/profile_client')

      }
    } catch (error) {
      console.error('Error updating profile:', error)
    }
  }
  
  const cancelEdit = () => {
  // Navigate to the appropriate profile page
  if (form.value.is_master) {
    router.push('/profile_master')
  } else {
    router.push('/profile_client')
  }
}
  
  onMounted(() => {
    fetchProfile()
  })
  </script>

<style scoped>
.container {
    padding-top: 50px;
}

.profile h1 {
    font-size: 35px;
    font-weight: 700;
    margin-bottom: 40px;
}

.form__top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;

}

.profile-picture-block {
    width: 250px;
    height: 305px;
    position: relative;
    margin-right: 21px;
}

.profile-picture-block img {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    width: 100%;
    height: 100%;
    object-fit: cover;

}

.profile__label {
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 100%;
    background-color: #2A7CC7;
    color: #fff;
    font-size: 14px;
    font-weight: 400;
    text-align: center;
    height: 30px;
    line-height: 30px;
    z-index: 2;
}

.profile__input {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    z-index: 1;
    height: 30px;
    background-color: transparent;
}

.form__right {

    width: 100%;

}

.form-group {
    display: flex;
    width: 100%;
    justify-content: space-between;


}

.form-group-element {
    width: 48%;
    margin-bottom: 30px;
}

.form-group-element input {
    width: 100%;
}

label {
    display: block;
    margin-bottom: 8px;
    font-size: 26px;
}

input[type="text"] {
    height: 50px;
    font-size: 20px;
    padding-left: 20px;
    width: 100%;
    border: 2px solid #858585;
    border-radius: 5px;
    margin-bottom: 20px;
}

textarea {
    width: 60%;
    padding: 10px;
    font-size: 20px;
    border: 2px solid #858585;
    border-radius: 5px;
}

textarea::placeholder {
    font-size: 20px;
    padding: 10px;
}

.profile__controls {
    display: flex;
}

.profile-btn {
    margin-top: 70px;
    margin-bottom: 70px;
    margin-right: 20px;
    display: flex;
    width: 245px;
    height: 55px;
    font-size: 24px;
    font-weight: 400;
    border-radius: 10px;
    justify-content: center;
    align-items: center;

}

.profile__cancel {
    background-color: transparent;
    border: 2px solid #858585;
    color: #000;
}

.profile__submit {
    background-color: #2A7CC7;
    border: none;
    color: #fff;
}
</style>