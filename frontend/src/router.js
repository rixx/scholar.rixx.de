import { createWebHistory, createRouter } from "vue-router";
import Start from "@/views/Start.vue";

// import config from '@/config'

let topicHistory = []

const routes = [
  {
    path: "/",
    name: "Start",
    component: Start,
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
  // base: process.env.BASE_URL,
})
router.beforeEach((to, from, next) => {
  if (!to.matched.length) {
    next({ name: 'home' })
  } else {
    const topics = to.matched.filter(record => record.name === 'topic')
    if (topics.length) {
      const topic = topics[0]
      topicHistory = topicHistory.filter(item => item !== topic)
      topicHistory.push(topic)
    }
    next()
  }
})
export default router
