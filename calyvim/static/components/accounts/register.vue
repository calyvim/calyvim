<script setup>
import _ from 'lodash'
import { reactive, computed, ref } from 'vue'
import { http } from '@/utils/api/index'
import { useToast } from "vue-toastification";

const props = defineProps(['recaptcha_enabled', 'recaptcha_site_key'])
const toast = useToast()

const registerForm = reactive({
	username: '',
	email: '',
	full_name: '',
	password: '',
})
const loading = ref(false)
const validUsername = ref(true)

const onFinish = async () => {
	console.log('Success:', registerForm)
	loading.value = true

	try {
		await http.post('/accounts/register/', registerForm)
		window.location.replace('/')
	} catch (error) {
		toast.error(error.response.data.detail)
	} finally {
		loading.value = false
	}
}
const onFinishFailed = (errorInfo) => {
	console.log('Failed:', errorInfo)
}
const disabled = computed(() => {
	return !(registerForm.username && registerForm.password && registerForm.full_name && registerForm.email)
})

const checkForUsername = async (event) => {
	try {
		if(!event.target.value) {
			validUsername.value = true
		}

		const { data } = await http.get('/accounts/username-check/', {
			params: {
				username: event.target.value
			}
		})


		validUsername.value = data.username_available
	} catch (error) {
		console.log(error)
	} finally {

	}
}

const checkForUsernameDebounced = _.debounce(checkForUsername, 500)
</script>
<template>
	<div class="d-flex align-items-center justify-content-center" id="register-form">
		<div class="card shadow-sm border-0" id="register-card">
			<div class="card-body">
				<h4>Register</h4>
				<form @submit.prevent="onFinish" class="">
					<div class="mb-3">
						<label class="form-label">Username</label>
						<input type="text" class="form-control" :class="{ 'is-invalid': !validUsername }"
							v-model="registerForm.username" @input="checkForUsernameDebounced" />
						<div class="invalid-feedback">
							This username is not available.
						</div>
					</div>

					<div class="mb-3">
						<label class="form-label">Email</label>
						<input type="email" class="form-control" v-model="registerForm.email" />
					</div>

					<div class="mb-3">
						<label class="form-label">Full name</label>
						<input type="text" class="form-control" v-model="registerForm.full_name" />
					</div>

					<div class="mb-3">
						<label class="form-label">Password</label>
						<input type="password" class="form-control" v-model="registerForm.password" />
					</div>

					<div class="d-grid">
						<button class="btn btn-sm btn-primary" type="submit" :disabled="disabled">Register</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<style scoped>
#register-form {
	height: 100vh;
}

#register-card {
	width: 350px
}
</style>
