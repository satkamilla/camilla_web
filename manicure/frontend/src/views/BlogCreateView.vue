<template>
    <div class="container">
      <div class="blog__create-title">
        Опубликовать пост
      </div>
      <form @submit.prevent="submitForm" class="blog__create">
        <label for="title">Заголовок</label>
        <input type="text" id="title" v-model="form.title">
        <label for="description">Описание</label>
        <textarea id="description" v-model="form.content"></textarea>
        <label for="image">Изображение</label>
        <div class="image__wrapper">
          <div v-if="!imagePreview" class="image__text">Выберите изображение</div>
          <img v-if="imagePreview" :src="imagePreview" alt="Uploaded Image" class="uploaded-image">
          <input type="file" id="image" name="image" @change="handleFileUpload" class="image__input">
          <a v-if="imagePreview" href="#" @click.prevent="editImage" class="edit-link">Редактировать</a>
        </div>
        <div class="profile__controls">
            <button type="button" @click="cancelEdit" class="profile__cancel profile-btn">Отменить</button>
            <button type="submit" class="profile__submit profile-btn">Сохранить</button>
          </div>
              </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  const form = ref({
    title: '',
    content: '',
    image: null
  })
  
  const imagePreview = ref('')
  
  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    form.value.image = file
    const reader = new FileReader()
    reader.onload = () => {
      imagePreview.value = reader.result
    }
    reader.readAsDataURL(file)
  }
  
  const editImage = () => {
    document.getElementById('image').click()
  }
  
  
  const router = useRouter()
  const cancelEdit = () => {
    router.push('/profile_master')
  }
  const submitForm = async () => {
    const token = localStorage.getItem('access_token')
    const formData = new FormData()
    formData.append('title', form.value.title)
    formData.append('content', form.value.content)
    if (form.value.image) {
      formData.append('image', form.value.image)
    }
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/blogs/create/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })
  
      if (!response.ok) {
        throw new Error('Failed to create blog post')
      }
  
      const data = await response.json()
      console.log('Blog post created:', data)
      router.push('/profile_master/')
    } catch (error) {
      console.error('Error creating blog post:', error)
    }
  }
  </script>
<style scoped>
.blog__create-title {
    margin-top: 20px;
    font-size: 45px;
    color: #1c1c1c;
    margin-bottom: 50px;
}

label {
    display: block;
    margin-bottom: 7px;
    font-size: 25px;
    color: #1c1c1c;
}

input {
    width: 100%;
    height: 50px;
    font-size: 24px;

    padding-left: 20px;
    border: 2px solid #858585;
    border-radius: 5px;
    margin-bottom: 35px;
}

textarea {
    margin-bottom: 35px;
    width: 50%;
    padding-left: 20px;
    border: 2px solid #858585;
    border-radius: 5px;
    height: 80px;
    font-size: 24px;
}



.image__wrapper {
  position: relative;
  border: 1px dashed #ccc;
  padding: 20px;
  text-align: center;
}

.image__text {
  font-size: 18px;
  color: #888;
}

.uploaded-image {
  width: 100%;
  height: 600px;
  object-fit: cover;
}

.image__input {
  display: none;
}

.edit-link {
  display: block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
}

.edit-link:hover {
  text-decoration: underline;
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

