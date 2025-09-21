import { createRouter, createWebHashHistory } from 'vue-router';
import EventDetail from './EventDetail.vue'; // Import your component

const routes = [
  {
    path: '/',
    component: EventDetail,
  },
  {
    path: '/:db_path(.*)',
    component: EventDetail,
    props: true
  }
];

const router = createRouter({
  history: createWebHashHistory("/dea/event_detail/"), // Use createWebHistory for cleaner URLs
  routes: routes
});

export default router;
