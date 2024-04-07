import { createApp } from "vue";
import Antd from "ant-design-vue";

import Home from "@/components/home/index.vue";

// Import our custom CSS
import '@/scss/styles.scss'

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

const vue_props = JSON.parse(document.getElementById("vue-props").textContent);

const app = createApp(Home, { ...vue_props });

app.use(Antd).mount("#app");
