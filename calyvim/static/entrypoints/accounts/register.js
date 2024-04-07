import { createApp } from "vue";
import Toast from "vue-toastification";

import AccountsRegister from "@/components/accounts/register.vue";

import '@/scss/styles.scss'
import "vue-toastification/dist/index.css";

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

const vue_props = JSON.parse(document.getElementById("vue-props").textContent);

const app = createApp(AccountsRegister, { ...vue_props });

app.use(Toast, {}).mount("#app");
