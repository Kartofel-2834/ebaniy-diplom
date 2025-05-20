// Styles
import './assets/main.css';

// Vue
import { createApp } from 'vue';

// Plugins
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import router from './router';

import App from './App.vue';

const app = createApp(App);

app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
    },
});

app.mount('#app');
