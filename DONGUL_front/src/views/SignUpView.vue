<template>
  <v-card class="container">
    <h1>회원가입</h1>

    <div class="checkbox">
      <p class="warning" v-text="errorAgree"></p>
      <v-checkbox color="#3CB371" value="service" v-model="selected">
        <template #label>
          <!-- 서비스 이용약관 동의 -->
          <span @click="serviceDialog = true" style="cursor: pointer; text-decoration: underline;">
            (필수) 서비스 이용약관 동의
          </span>
        </template>
      </v-checkbox>
      <v-checkbox color="#3CB371" value="info" v-model="selected">
        <template #label>
          <!-- 개인정보 처리 동의 -->
          <span @click="infoDialog = true" style="cursor: pointer; text-decoration: underline;">
            (필수) 개인정보 처리 동의
          </span>
        </template>
      </v-checkbox>
      <v-checkbox color="#3CB371" v-model="isAgreeAll">
        <template v-slot:label>
          <span class="color">전체 동의</span>
        </template>
      </v-checkbox>
    </div>

    <form @submit.prevent="signUp" @keypress.enter="signUp">
      <!-- 기존 입력 필드 -->
      <v-text-field variant="outlined" color="#3CB371" label="아이디" v-model="state.username"
        :error-messages="v$.username.$errors.map(e => e.$message)" @input="v$.username.$touch"
        @blur="v$.username.$touch"></v-text-field>

      <v-text-field variant="outlined" color="#3CB371" label="닉네임" v-model="state.nickname"
        :error-messages="v$.nickname.$errors.map(e => e.$message)" @input="v$.nickname.$touch"
        @blur="v$.nickname.$touch"></v-text-field>

      <v-text-field variant="outlined" color="#3CB371" label="이메일" v-model="state.email"
        :error-messages="v$.email.$errors.map(e => e.$message)" @input="v$.email.$touch"
        @blur="v$.email.$touch"></v-text-field>

      <v-text-field variant="outlined" color="#3CB371" :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show1 ? 'text' : 'password'" label="비밀번호" v-model="state.password1" @click:append="show1 = !show1"
        :error-messages="v$.password1.$errors.map(e => e.$message)" @input="v$.password1.$touch"
        @blur="v$.password1.$touch"></v-text-field>

      <v-text-field variant="outlined" color="#3CB371" :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show2 ? 'text' : 'password'" label="비밀번호 확인" v-model="state.password2" @click:append="show2 = !show2"
        :error-messages="v$.password2.$errors.map(e => e.$message)" @input="v$.password2.$touch"
        @blur="v$.password2.$touch"></v-text-field>

      <v-btn block variant="flat" color="#3CB371" @click.prevent="signUp">
        Sign up
      </v-btn>

    </form>
  </v-card>

  <!-- 서비스 이용약관 다이얼로그 -->
  <v-dialog v-model="serviceDialog" max-width="500px">
    <v-card>
      <v-card-title>서비스 이용약관</v-card-title>
      <v-card-text>
        <p>서비스를 이용하기 위해 다음 약관에 동의해야 합니다.</p>
        <ul>
          <li>서비스 제공을 위해 필요한 최소한의 정보를 수집합니다.</li>
          <li>서비스 내 콘텐츠는 이용자의 책임 하에 사용됩니다.</li>
          <li>기타 자세한 약관은 별도로 제공됩니다.</li>
        </ul>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="serviceDialog = false">닫기</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- 개인정보 처리 동의 다이얼로그 -->
  <v-dialog v-model="infoDialog" max-width="500px">
    <v-card>
      <v-card-title>개인정보 처리 내역서</v-card-title>
      <v-card-text>
        <p>저희는 사용자의 개인정보를 안전하게 보호하기 위해 최선을 다하고 있습니다.</p>
        <ul>
          <li>수집 항목: 이름, 이메일, 연락처</li>
          <li>이용 목적: 서비스 제공 및 회원 관리</li>
          <li>보관 기간: 회원 탈퇴 시까지</li>
        </ul>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="infoDialog = false">닫기</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/users'
import { useVuelidate } from '@vuelidate/core'
import { useRouter } from 'vue-router'
import { email, required, minLength, maxLength, alphaNum, sameAs, helpers } from '@vuelidate/validators'

const userStore = useUserStore()
const router = useRouter()

const checkList = ['service', 'info']
const selected = ref([])
const show1 = ref(false)
const show2 = ref(false)

// 다이얼로그 상태 관리
const serviceDialog = ref(false)
const infoDialog = ref(false)

const isAgreeAll = computed({
  get() {
    return checkList.length === selected.value.length
  },
  set(e) {
    selected.value = e ? checkList : []
  }
})

const errorAgree = ref('ㅤ')

const initialState = {
  username: '',
  nickname: '',
  email: '',
  password1: '',
  password2: '',
}

const state = ref({
  ...initialState
})

const rules = {
  username: {
    required: helpers.withMessage('필수 정보입니다.', required),
    alphaNum: helpers.withMessage('영어 대소문자와 숫자만 입력가능합니다.', alphaNum),
    minLength: helpers.withMessage('5자 이상 입력해야합니다.', minLength(5)),
    maxLength: helpers.withMessage('20자 이하로 입력해야합니다.', maxLength(20))
  },
  nickname: {
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('20자 이하로 입력해야합니다.', maxLength(20))
  },
  email: {
    required: helpers.withMessage('필수 정보입니다.', required),
    email: helpers.withMessage('이메일 주소가 정확한지 확인해 주세요.', email),
    maxLength: helpers.withMessage('100자 이하로 입력해야합니다.', maxLength(100))
  },
  password1: {
    required: helpers.withMessage('필수 정보입니다.', required),
    minLength: helpers.withMessage('8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.', minLength(8)),
    maxLength: helpers.withMessage('8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.', maxLength(16)),
    containspasswordrequirement: helpers.withMessage(
      () => `8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.`,
      (value) => /(?=.*[a-z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])/.test(value)
    )
  },
  password2: {
    required: helpers.withMessage('필수 정보입니다.', required),
    sameAsPassword: helpers.withMessage('비밀번호가 일치하지 않습니다.',
      sameAs(computed(() => state.value.password1))
    )
  }
}

const v$ = useVuelidate(rules, state)

function clear() {
  v$.value.$reset()

  for (const [key, value] of Object.entries(initialState)) {
    state[key] = value
  }
}

const signUp = function () {
  v$.value.$validate()

  if (selected.value.length !== checkList.length) {
    errorAgree.value = '약관에 동의하셔야 합니다.'
  } else {
    errorAgree.value = 'ㅤ'
    if (!v$.value.$error) {
      const payload = {
        username: state.value.username,
        nickname: state.value.nickname,
        email: state.value.email,
        password1: state.value.password1,
        password2: state.value.password2,
      }
      userStore.signUp(payload).then(() => {
        router.push({ name: 'signIn' })
      })
    }
  }
}
</script>



<style scoped>
.container {
  width: 500px;
  margin: 3rem auto;
  padding: 2rem;
  text-align: center;
}

.checkbox {
  margin: 1rem 0;
}

.v-checkbox {
  height: 40px;
}

form * {
  text-align: start;
  margin: 0.6rem 0;
}

.warning {
  color: #d61150;
  font-size: 12px;
  margin: 0 0 0 15px;
}
</style>
