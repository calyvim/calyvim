<script setup>
import _ from 'lodash'
import { reactive, computed, ref } from 'vue'
import { http } from '@/utils/api/index'
import { useToast } from 'vue-toastification'

const props = defineProps(['next_url'])

const toast = useToast()

const loginForm = reactive({
  username: '',
  password: '',
})
const loading = ref(false)
const validUsername = ref(true)

const onFinish = async () => {
  loading.value = true

  try {
    await http.post('/accounts/login/', loginForm)
    window.location.replace(props.next_url)
  } catch (error) {
    toast.error(error.response.data.detail)
  } finally {
    loading.value = false
  }
}

const disabled = computed(() => {
  return !(
    loginForm.username &&
    loginForm.password
  )
})

</script>
<template>
  <div
    class="d-flex align-items-center justify-content-center"
    id="login-form"
  >
    <div class="card shadow-sm border-0" id="login-card">
      <div class="card-body">
        <h4>Login</h4>
        <form @submit.prevent="onFinish" class="">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              :class="{ 'is-invalid': !validUsername }"
              v-model="loginForm.username"
            />
            <div class="invalid-feedback">This username is not available.</div>
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              v-model="loginForm.password"
            />
          </div>

          <div class="d-grid">
            <button
              class="btn btn-sm btn-primary"
              type="submit"
              :disabled="disabled"
            >
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
#login-form {
  height: 100vh;
}

#login-card {
  width: 350px;
}
</style>
