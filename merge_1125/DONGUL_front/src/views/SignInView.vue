<script setup>
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()

const show = ref(false)
const username = ref('')
const password = ref('')
const isRight = ref(true)
const shake = ref(false)

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  const temp = userStore.logIn(payload)
  
  setTimeout(() => {
    isRight.value = temp
    if (!isRight.value) {
      username.value = password.value = ''
      shake.value = true
      setTimeout(() => (shake.value = false), 500) // 애니메이션 0.5초 후 초기화
    }
  }, 200)
}
</script>

<template>
  <v-card :class="['container', { shake }]" outlined>
    <h1><span class="color">로그인</span></h1>

    <v-form @submit.prevent="logIn" @keypress.enter="logIn">
      <v-text-field
        variant="outlined"
        color="#3CB371"
        label="아이디"
        v-model="username"
        class="input-field"
        placeholder="아이디를 입력하세요"
      ></v-text-field>
      <v-text-field
        variant="outlined"
        color="#3CB371"
        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show ? 'text' : 'password'"
        label="비밀번호"
        v-model="password"
        @click:append="show = !show"
        class="input-field"
        placeholder="비밀번호를 입력하세요"
      ></v-text-field>
      <div v-show="!isRight" class="warning text-red">
        <p>아이디(로그인 전용 아이디) 또는 비밀번호를 잘못 입력했습니다.</p>
        <p>입력하신 내용을 다시 확인해주세요.</p>
      </div>
      <v-btn
        block
        variant="flat"
        color="#3CB371"
        class="sign-in-btn"
        @click.prevent="logIn"
      >
        Sign in
      </v-btn>
    </v-form>
  </v-card>
</template>

<style scoped>
/* 컨테이너 스타일 */
.container {
  width: 500px;
  margin: 3rem auto;
  padding: 2rem;
  text-align: center;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  
  border-radius: 12px;
  transition: transform 0.3s;
}

/* 흔들림 애니메이션 */
@keyframes shake-animation {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-10px);
  }
  50% {
    transform: translateX(10px);
  }
  75% {
    transform: translateX(-10px);
  }
}

.shake {
  animation: shake-animation 0.5s;
}

/* 입력 필드 간격 */
.input-field {
  margin-bottom: 1rem;
  
}

/* 경고 메시지 스타일 */
.warning {
  text-align: start;
  margin-bottom: 1.2rem;
  font-size: 15px;
  padding: 10px;
  border: 1px solid #f5c6cb;
  background-color: #f8d7da;
  border-radius: 8px;
}

/* 버튼 스타일 */
.sign-in-btn {
  margin-top: 1rem;
  font-weight: bold;
  font-size: 16px;
  transition: background-color 0.3s;
}

.sign-in-btn:hover {
  background-color: #2e8b57;
}
</style>
