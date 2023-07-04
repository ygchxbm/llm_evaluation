import { createApp } from 'vue';
import pinia from '@/stores/index';
import App from './App.vue';
import router from './router';
import { i18n } from '@/i18n/index';
import other from '@/utils/other';

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '@/theme/index.scss';
import mitt from 'mitt';
//改默认英文为中文
import locale from 'element-plus/lib/locale/lang/en'

const app = createApp(App);
app.use(ElementPlus, { locale });

other.elSvg(app);

app.use(pinia).use(router).use(ElementPlus, { i18n: i18n.global.t }).use(i18n).mount('#app');

app.config.globalProperties.mittBus = mitt();
