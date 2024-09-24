import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isAuthenticated = ref(!!localStorage.getItem('access_token'))
const userProfile = ref(null)

export function useAuth() {
  const router = useRouter()

  const login = (tokens) => {
    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    isAuthenticated.value = true
    fetchUserProfile()
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    isAuthenticated.value = false
    userProfile.value = null
    router.push('/')
  }

  const isAuth = computed(() => isAuthenticated.value)

  const fetchUserProfile = async () => {
    if (!isAuthenticated.value) return

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
      userProfile.value = data
    } catch (error) {
      console.error('Error fetching profile:', error)
    }
  }

  onMounted(() => {
    if (isAuthenticated.value) {
      fetchUserProfile()
    }
  })

  return {
    login,
    logout,
    isAuth,
    userProfile,
    fetchUserProfile
  }
}
