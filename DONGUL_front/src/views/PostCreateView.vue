<template>
  <div class="container">
    <header class="header">
      <h1 class="title">새로운 글 작성</h1>
    </header>
    <v-form class="form-container my-5">
      <!-- 제목 입력 필드 -->
      <v-text-field
        variant="outlined"
        color="#5cb85c"
        label="제목"
        v-model="state.title"
        :error-messages="v$.title.$errors.map(e => e.$message)"
        @input="v$.title.$touch"
        @blur="v$.title.$touch"
        @keypress.enter="createPost"
        class="text-field"
      ></v-text-field>
      
      <!-- 내용 입력 필드 -->
      <v-textarea
        variant="outlined"
        color="#5cb85c"
        label="내용"
        v-model="state.content"
        auto-grow
        rows="15"
        row-height="25"
        shaped
        :error-messages="v$.content.$errors.map(e => e.$message)"
        @input="v$.content.$touch"
        @blur="v$.content.$touch"
        class="textarea-field"
      ></v-textarea>
      
      <!-- 게시 버튼 -->
      <v-btn
        block
        variant="elevated"
        color="#5cb85c"
        @click.prevent="createPost"
        class="post-btn"
      >
        게시물 작성하기
      </v-btn>
    </v-form>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'
import { useVuelidate } from '@vuelidate/core'
import { required, maxLength, helpers } from '@vuelidate/validators'
import axios from 'axios'

const initialState = {
  title: '',
  content: ''
}

const state = ref({
  ...initialState
})

const router = useRouter()
const userStore = useUserStore()

const rules = {
  title: {
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('300자 이하로 입력해야합니다.', maxLength(300))
  },
  content: {
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('10000자 이하로 입력해야합니다.', maxLength(10000))
  }
}

const v$ = useVuelidate(rules, state)

const createPost = function () {
  // state.value.title = title
  // state.value.content = content

  v$.value.$validate()

  if (!v$.value.$error) {
    axios({
      method: 'post',
      url: `${userStore.API_URL}/posts/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: {
        title: state.value.title,
        content: state.value.content
      }
    })
      .then((res) => {
        router.push({ name: 'postDetail', params: { id: res.data.id }, query: { page: 1 } })
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
</script>



<style scoped>
/* 컨테이너 */
.container {
  width: 800px;
  margin: 3rem auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 2rem 3rem;
  padding-top: 100px;
}

/* 헤더 */
.header {
  text-align: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #5cb85c;
}

/* 폼 컨테이너 */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 텍스트 필드 */
.text-field {
  border-radius: 8px;
}

/* 텍스트 영역 */
.textarea-field {
  border-radius: 8px;
}

/* 게시 버튼 */
.post-btn {
  font-size: 1.2rem;
  font-weight: bold;
  background-color: #1089FF;
  color: white;
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
}

.post-btn:hover {
  background-color: #0a6fce;
}
</style>
