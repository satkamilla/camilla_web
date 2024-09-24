<template>
    <div class="container">
        <div class="messenger">
            <div class="messenger__aside">
                <div class="messenger__aside-header">
                    <div class="messenger__aside-title">Сообщения</div>
                    <div class="messenger__aside-search">
                        <form action="">
                            <input type="text" placeholder="Найти чат">
                        </form>
                    </div>
                </div>
                <div class="messenger__aside-list">
                    <div v-for="conversation in conversations" :key="conversation.id" class="messenger__aside-chat" @click="openChat(conversation)">
<!--                         <div class="chatcard__profile-photo profile-photo">
                            <img :src="getProfilePhoto(conversation.participants)" alt="Profile Photo">
                        </div> -->
                        <div class="chatcard__text">
                            <div class="chatcard__username">
                                {{ getParticipantName(conversation.participants) }}
                            </div>
                            <div class="chatcard__last-message">
                                {{ conversation.messages.length > 0 ? conversation.messages[conversation.messages.length - 1].text : 'No messages yet' }}
                            </div>
                            <div class="chatcard__timestamp">
                                {{ conversation.messages.length > 0 ? formatTimestamp(conversation.messages[conversation.messages.length - 1].timestamp) : '' }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="messenger__content">
                <ChatWindow v-if="selectedConversationId" :conversation-id="selectedConversationId" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChatWindow from '@/components/ChatWindow.vue'

const conversations = ref([])
const selectedConversationId = ref(null)
const currentUserEmail = localStorage.getItem('user_email') // Assuming user email is stored in localStorage
const error = ref('')

const fetchConversations = async () => {
    try {
        console.log('Fetching conversations...')
        const response = await fetch('http://127.0.0.1:8000/api/v1/conversations/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(`Error fetching conversations: ${response.status} - ${errorData.detail || response.statusText}`)
        }

        const data = await response.json()
        console.log('Fetched conversations:', data)
        conversations.value = data
    } catch (err) {
        console.error('Error fetching conversations:', err)
        error.value = err.message
    }
}

const openChat = (conversation) => {
    const participant = conversation.participants.find(p => p.email !== currentUserEmail)
    console.log('Opening chat with conversationId:', conversation.id, 'and participant:', participant)
    selectedConversationId.value = conversation.id
}

const getParticipantName = (participants) => {
    const participant = participants.find(p => p.email !== currentUserEmail)
    return participant ? `${participant.first_name} ${participant.last_name}` : 'Unknown'
}

const getProfilePhoto = (participants) => {
    const participant = participants.find(p => p.email !== currentUserEmail)
    return participant && participant.picture ? participant.picture : ''
}

const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
    fetchConversations()
})
</script>


<style>
.messenger {
    display: flex;
    justify-content: space-between;
}


.messenger__aside-header {

    border-bottom: 1px solid #AFB8CF;

}

.messenger__aside-search {
    padding: 20px 0;
    width: 100%;
}

.messenger__aside-search form {
    width: 100%;
    box-sizing: border-box;
}

.messenger__aside-search input {
    box-sizing: border-box;
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #AFB8CF;
}

.messenger__aside-title {
    font-size: 18px;
    padding-bottom: 20px;
    border-bottom: 1px solid #AFB8CF;
}

.profile-photo img {
    width: 50px;
    border-radius: 20%;
}

.messenger__aside {
    width: 30%;
}

.messenger__content {
    width: 65%;
}

.messenger__aside-chat {
    display: flex;
    border-bottom: 1px solid #AFB8CF;
    padding-top: 20px;
    padding-bottom: 20px;
    align-items: center;
}

.chatcard__profile-photo {
    margin-right: 10px;
}

.chatcard__username {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
}

.chatcard__last-message {
    font-size: 14px;
    margin-bottom: 8px;
    font-weight: 400;
}

.chatcard__timestamp {
    font-size: 12px;
    font-weight: 300;
}

.chat__header {
    display: flex;
    align-items: center;
    padding: 20px 0;
    margin-bottom: 20px;
}

.chat__header-image {
    margin-right: 20px;
}

.chat__message {
    width: 270px;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 15px;
    background-color: #DCE6FF;
    font-weight: 400;
    font-size: 14px;
    margin-bottom: 40px;
    display: flex;
    flex-direction: column;
}

/* .received{
    left: 10px;
    background-color: #DCE6FF;
    color: #fff;
} */

.chat__message.sent {
    background-color: #3D64FD;
    color: #fff;
    align-self: flex-end;
}


.messenger__content {
    position: relative;
    height: 530px;

}

.chat__content {
    position: relative;
    height: 300px;
    overflow-y: scroll;
    padding-right: 20px;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
}



.chat__input {
    box-sizing: border-box;
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #AFB8CF;
    position: absolute;
    bottom: 20px;
}
</style>