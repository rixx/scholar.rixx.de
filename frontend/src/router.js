import { createWebHistory, createRouter } from "vue-router";
import Start from "@/views/Start.vue";
import Topic from "@/views/Topic.vue";

const routes = [
  {
    path: "/",
    name: "Start",
    component: Start,
  },
  {
    path: "/t/:topicName",
    name: "Topic",
    component: Topic,
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
})
router.beforeEach((to, from, next) => {
  if (!to.matched.length) {
    next({ name: 'home' })
  } else {
    next()
  }
})
export default router
