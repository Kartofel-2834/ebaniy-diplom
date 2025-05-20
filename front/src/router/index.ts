// Router
import { createRouter, createWebHistory } from 'vue-router';

// Pages
import MainPage from '@/pages/MainPage.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'main',
            component: () => import('@/pages/MainPage.vue'),
        },
    ],
});

export default router;
