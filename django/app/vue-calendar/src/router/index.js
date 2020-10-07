import { createRouter, createWebHistory } from 'vue-router'
import Calendar from '@/components/Calendar.vue'

const routes = [
  {
    path: '/',
    name: 'django-calender',
    components: {
      default: Calendar,
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
