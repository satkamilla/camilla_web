<template>
    <div class="chat">
<!--         <div class="chat__header">
            <div class="chat__header-image profile-photo">
                <img :src="profilePhoto" alt="">
            </div>
            <div class="chat__header-title">{{ participantName }}</div>
        </div> -->
        <div class="chat__content">
            <div v-for="message in messages" :key="message.id"
                :class="['chat__message', message.sender.email === currentUserEmail ? 'sent' : 'received']">
                <div class="chat__message-text">{{ message.text }}</div>
                <div class="chat__message-time">{{ formatTimestamp(message.timestamp) }}</div>
            </div>
        </div>
        <div class="chat__type">
            <form @submit.prevent="sendMessage">
                <input type="text" class="chat__input" v-model="newMessage" placeholder="Напишите сообщение...">
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
    conversationId: {
        type: Number,
        required: true
    }
})

const currentUserEmail = localStorage.getItem('user_email')
const messages = ref([])
const newMessage = ref('')
const participantName = ref('')
const profilePhoto = ref('')

watch(
    () => props.conversationId,
    (newVal) => {
        if (newVal) {
            console.log('Fetching messages for conversationId:', newVal)
            fetchMessages(newVal)
        }
    }
)

const fetchMessages = async (conversationId) => {
    try {
        console.log('Fetching messages...')
        const response = await fetch(`http://127.0.0.1:8000/api/v1/conversations/${conversationId}/messages/`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(`Error fetching messages: ${response.status} - ${errorData.detail || response.statusText}`)
        }

        const data = await response.json()
        console.log('Fetched messages:', data)
        messages.value = data
        const participant = data.length > 0 ? data[0].conversation.participants.find(p => p.email !== currentUserEmail) : { email: 'Unknown' }
        participantName.value = participant.first_name + ' ' + participant.last_name
        profilePhoto.value = participant.profile_picture || '/img/masters/master1.jpg' // Placeholder for actual photo URL
    } catch (err) {
        console.error('Error fetching messages:', err)
    }
}

const sendMessage = async () => {
    if (!newMessage.value.trim()) return

    try {
        console.log('Sending message...')
        const response = await fetch(`http://127.0.0.1:8000/api/v1/conversations/${props.conversationId}/messages/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: newMessage.value })
        })

        if (!response.ok) {
            const errorText = await response.text() // Get the full response text
            console.error(`Error sending message: ${response.status} - ${response.statusText}`)
            console.error(errorText) // Log the full error response
            throw new Error(`Error sending message: ${response.status} - ${response.statusText}`)
        }

        const data = await response.json()
        console.log('Message sent:', data)
        messages.value.push(data)
        newMessage.value = ''
    } catch (err) {
        console.error('Error sending message:', err)
    }
}

onMounted(() => {
    if (props.conversationId) {
        fetchMessages(props.conversationId)
    }
})

const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped></style>