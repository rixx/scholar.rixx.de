import { createWebHistory, createRouter } from "vue-router";
import Start from "@/views/Start.vue";
import Topic from "@/views/Topic.vue";
import TopicList from "@/views/TopicList.vue";
import Source from "@/views/Source.vue";

const routes = [
  {
    path: "/",
    name: "Start",
    component: Start,
  },
  {
    path: "/t/",
    name: "TopicList",
    component: TopicList,
  },
  {
    path: "/t/:topicName",
    name: "Topic",
    component: Topic,
  },
  {
    path: "/source/:sourceId",
    name: "Source",
    component: Source,
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
