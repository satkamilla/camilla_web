<template>
    <div class="container">
        <div class="service__create-title">
            Разместить услугу
        </div>
        <form @submit.prevent="submitForm" class="service__create">
            <label for="title">Заголовок</label>
            <input type="text" id="title" v-model="form.name">
            <label for="description">Описание</label>
            <textarea id="description" v-model="form.description"></textarea>
            <label for="price">Цена</label>
            <input type="text" id="price" v-model="form.price">
            <label for="service_type">Тип услуги</label>
            <select id="service_type" v-model="form.service_type">
                <option v-for="type in serviceTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                </option>
            </select>
            <label for="image">Изображение</label>
            <div class="image__wrapper">
                <div v-if="!imagePreview" class="image__text">Загрузить фотографию</div>
                <img v-if="imagePreview" :src="imagePreview" alt="Uploaded Image" class="uploaded-image">
                <input type="file" id="image" name="image" @change="handleFileUpload" class="image__input">
                <a v-if="imagePreview" href="#" @click.prevent="editImage" class="edit-link">Редактировать</a>
            </div>
            <div class="profile__controls">
                <button type="button" @click="cancelEdit" class="profile__cancel profile-btn">Отменить</button>
                <button type="submit" class="profile__submit profile-btn">Опубликовать</button>
            </div>
        </form>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const form = ref({
    name: '',
    description: '',
    price: '',
    service_type: '',
    image: null
})

const imagePreview = ref('')
const serviceTypes = ref([])
const errorMessage = ref('')

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
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)
    formData.append('price', form.value.price)
    formData.append('service_type', form.value.service_type) // Ensure this is sent as an integer
    if (form.value.image) {
        formData.append('image', form.value.image)
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/services/create/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        })

        if (!response.ok) {
            const errorData = await response.json()
            console.log('Backend error:', errorData) // Log the backend error
            errorMessage.value = `Failed to create service: ${errorData.detail || response.statusText}`
            throw new Error(errorMessage.value)
        }

        const data = await response.json()
        console.log('Service created:', data)
        router.push('/profile_master')
    } catch (error) {
        console.error('Error creating service:', error)
    }
}

const fetchServiceTypes = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/service-types/', {
            headers: {
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) {
            throw new Error('Failed to fetch service types')
        }

        const data = await response.json()
        serviceTypes.value = data
    } catch (error) {
        console.error('Error fetching service types:', error)
    }
}

onMounted(() => {
    fetchServiceTypes()
})
</script>

<style scoped>
.container {
    width: 600px;
    margin: 0 auto;
}

.service__create-title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

.service__create {
    display: flex;
    flex-direction: column;
}

label {
    margin-top: 10px;
    margin-bottom: 5px;
    font-weight: bold;
}

input[type='text'],
textarea {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border-radius: 4px;
    border: 1px solid #ccc;
    box-sizing: border-box;
}

.image__wrapper {
    position: relative;
    border: 1px dashed #ccc;
    padding: 20px;
    text-align: center;
    margin-bottom: 10px;
}

.image__text {
    font-size: 18px;
    color: #888;
}

.uploaded-image {
    width: 100%;
    height: auto;
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
    justify-content: space-between;
}

.profile-btn {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.profile-btn:hover {
    background-color: #0056b3;
}

.profile__cancel {
    background-color: #6c757d;
}

.profile__cancel:hover {
    background-color: #5a6268;
}
</style>