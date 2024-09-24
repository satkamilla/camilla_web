<template>
    <div class="comment">
        <div class="container">
            <div class="comment__wrapper">
                <div class="comment__header">
                    <div class="comment__photo"><img :src="comment.author.picture" alt="Author Photo"></div>
                    <div class="comment__username">{{ comment.author.name }}</div>
                </div>
                <div class="comment__text">{{ comment.content }}</div>
                <div class="comment__timestamp">{{ formatTimestamp(comment.created_at) }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    comment: {
        type: Object,
        required: true
    }
})

const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleString([], { year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.comment {
    margin-bottom: 15px;
}

.comment__wrapper {
    width: 100%;
    border: 1px solid #D8DADC;
    border-radius: 10px;
    padding: 20px;
}

.comment__header {
    display: flex;
    margin-bottom: 20px;
    align-items: center;
}

.comment__photo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.comment__photo img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.comment__username {
    margin-left: 20px;
    font-weight: bold;
    font-size: 18px;
}

.comment__text {
    font-weight: 400;
    font-size: 16px;
    margin-bottom: 10px;
}
</style>