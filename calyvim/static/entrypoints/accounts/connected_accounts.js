import { createApp } from "vue";
import Toast from "vue-toastification";

import connectedAccounts from "@/components/accounts/connected_accounts.vue";

import '@/scss/styles.scss'
import "vue-toastification/dist/index.css";

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

const vue_props = JSON.parse(document.getElementById("vue-props").textContent);

const app = createApp(connectedAccounts, { ...vue_props });

app.use(Toast, {}).mount("#app");
