import { createRouter, createWebHashHistory } from 'vue-router';
import EventGroupDetail from './EventGroupDetail.vue';

const routes = [
  {
    path: '/',
    component: EventGroupDetail,
  },
  {
    path: '/:db_path(.*)',
    component: EventGroupDetail,
    props: true
  }
];

const router = createRouter({
  history: createWebHashHistory("/dea/event_group_detail/"), // Use createWebHistory for cleaner URLs
  routes: routes
});

export default router;
