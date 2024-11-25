<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'
import { useUserStore } from '@/stores/users'
import { useVuelidate } from '@vuelidate/core'
import { required, integer, helpers } from '@vuelidate/validators'
import BarChart from '@/components/BarChart.vue'
import BarChartDetail from '@/components/BarChartDetail.vue'
import axios from 'axios'

const userInfo = ref()
const dialog = ref(false)
const isShowProfileInput = ref(false)
const image = ref()
const selectedKey = ref('')
const state = ref({
  updateValue: ''
})
const selectedMonth = ref()
const months = [
  { title: '6개월', value: 6 },
  { title: '12개월', value: 12 },
  { title: '24개월', value: 24 },
  { title: '36개월', value: 36 },
]

const userStore = useUserStore()
const postStore = usePostStore()
const route = useRoute()
const router = useRouter()

const usernameTemp = userStore.userInfo.username

const queryPage = route.query?.page
const page = ref(Number(queryPage) || 1)

const myPosts = ref([])

const rules = {
  updateValue: {
    required: helpers.withMessage('필수 정보입니다.', required),
    integer: helpers.withMessage('숫자를 입력해야합니다.', integer)
  }
}

const v$ = useVuelidate(rules, state)

const fetchMyPosts = async () => {
  await postStore.getPosts(page.value)
  myPosts.value = postStore.posts.filter(
    (post) => post.user.username === userStore.userInfo.username
  )
}

const clickTr = (postId) => {
  router.push({ name: 'postDetail', params: { id: postId }, query: { page: page.value } })
}

watch(page, () => {
  fetchMyPosts()
  window.scrollTo({ left: 0, top: 0, behavior: 'smooth' })
})

onMounted(() => {
  const storeUserInfo = userStore.userInfo
  userInfo.value = {
    '아이디': storeUserInfo.username,
    '닉네임': storeUserInfo.nickname,
    '이메일': storeUserInfo.email,
    '나이': storeUserInfo.age,
    '자산': storeUserInfo.money,
    '연봉': storeUserInfo.salary,
    '예금 희망 금액': storeUserInfo.desire_amount_deposit,
    '예금 희망 기간 (월)': storeUserInfo.deposit_period,
    '월 적금 희망 금액': storeUserInfo.desire_amount_saving,
    '적금 희망 기간 (월)': storeUserInfo.saving_period,
  }
  fetchMyPosts()
})

const editValue = function (key, value) {
  selectedKey.value = key
  state.updateValue = userInfo.value[key]
  selectedMonth.value = value
  dialog.value = true
}

const close = function () {
  dialog.value = false
}

const save = function () {
  v$.value.$validate()

  if (!v$.value.$error || selectedKey.value === '예금 희망 기간 (월)' || selectedKey.value === '적금 희망 기간 (월)') {
    const key = ref('')
    const body = ref(state.value.updateValue)
    if (selectedKey.value === '나이') {
      key.value = 'age'
    } else if (selectedKey.value === '자산') {
      key.value = 'money'
    } else if (selectedKey.value === '연봉') {
      key.value = 'salary'
    } else if (selectedKey.value === '예금 희망 금액') {
      key.value = 'desire_amount_deposit'
    } else if (selectedKey.value === '예금 희망 기간 (월)') {
      key.value = 'deposit_period'
      body.value = selectedMonth.value
    } else if (selectedKey.value === '월 적금 희망 금액') {
      key.value = 'desire_amount_saving'
    } else if (selectedKey.value === '적금 희망 기간 (월)') {
      key.value = 'saving_period'
      body.value = selectedMonth.value
    }

    axios({
      method: 'put',
      url: `${userStore.API_URL}/users/${userStore.userInfo.username}/info/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: {
        [key.value]: body.value
      }
    })
    .then((res) => {
        userStore.getUserInfo(usernameTemp)
        userInfo.value[selectedKey.value] = body.value
        selectedKey.value = state.value.updateValue = ''
        selectedMonth.value = null
        dialog.value = false
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
const editProfileImg = function (event) {
  if (isShowProfileInput.value === false) {
    isShowProfileInput.value = true
  } else {
    axios({
      method: 'put',
      url: `${userStore.API_URL}/users/${usernameTemp}/profile/`,
      headers: {
        Authorization: `Token ${userStore.token}`,
        "Content-Type": 'multipart/form-data'
      },
      data: {
        'profile_img': image.value
      }
    })
      .then((res) => {
        userStore.getUserInfo(usernameTemp)
        isShowProfileInput.value = false
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

</script>

<template>
  <div class="profile-page">
    <h1 class="profile-title">어서오세요, <span class="color">{{ userStore.userInfo.nickname }}</span>님!</h1>
    <v-divider class="my-3"></v-divider>

    <div v-if="userInfo" class="profile-wrapper">
      <div class="profile-image">
        <v-avatar size="300">
          <v-img cover :src="`${userStore.API_URL}${userStore.userInfo.profile_img}`"></v-img>
        </v-avatar>
        <v-btn class="btn-profile-edit" @click="editProfileImg">
          프로필 이미지 변경
        </v-btn>
        <v-file-input
          v-show="isShowProfileInput"
          accept="image/png, image/jpeg, image/bmp"
          variant="underlined"
          label="프로필 이미지"
          v-model="image"
          class="mt-4"
        />
      </div>

      <div class="profile-info">
        <v-table class="table">
          <tbody>
            <tr v-for="(value, key) in userInfo" :key="key">
              <td>{{ key }}</td>
              <td>{{ value }}</td>
              <td>
                <v-icon v-if="key !== '회원번호'" @click="editValue(key, value)">mdi-pencil</v-icon>
              </td>
            </tr>
          </tbody>
        </v-table>
      </div>
    </div>

    <!-- 수정 다이얼로그 -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>정보 수정</v-card-title>
        <v-card-text>
          <v-select
            v-if="selectedKey === '예금 희망 기간 (월)' || selectedKey === '적금 희망 기간 (월)'"
            color="#1089FF"
            variant="outlined"
            :label="selectedKey"
            :items="months"
            item-text="title"
            item-value="value"
            v-model="selectedMonth"
          ></v-select>
          <v-text-field
            v-else
            type="number"
            color="#1089FF"
            variant="outlined"
            v-model="state.updateValue"
            :label="selectedKey"
            :error-messages="v$.updateValue.$errors.map(e => e.$message)"
            @input="v$.updateValue.$touch"
            @blur="v$.updateValue.$touch"
            @keypress.enter="save"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="#1089FF" @click="close">취소</v-btn>
          <v-btn text color="#1089FF" @click="save">저장</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 내가 쓴 글 목록 -->
    <div class="my-posts">
      <h2>내가 쓴 글 목록 ({{ myPosts.length }})</h2>
      <div v-if="myPosts.length > 0">
        <v-table class="table">
          <tbody>
            <tr v-for="post in myPosts" :key="post.id" @click="clickTr(post.id)" style="cursor: pointer;">
              <td>{{ post.title }}</td>
              <td>{{ post.created_at.slice(0,10) }}</td>
            </tr>
          </tbody>
        </v-table>
      </div>
      <p v-else class="no-posts">아직 쓴 글이 없습니다.</p>
    </div>

  </div>
</template>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #042940;
}

.profile-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: white;
}

.profile-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
}

.profile-image {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-input {
  margin-top: 1rem;
}

.btn-profile-edit {
  margin-top: 1rem;
  background-color: #005C53;
  color: white;
}

.profile-info {
  flex: 1;
  background-color: #042940;
}

/* 내가 쓴 글 목록 스타일 */
.my-posts {
  margin-top: 2rem;
  width: 100%;
  max-width: 1000px;
}

.my-posts h2 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.table {
  background-color: #042940;
  color: white;
}

.table tr {
  border-bottom: 1px solid #dbdbdb;
}

.table td {
  padding: 10px;
  text-align: left;
}

.table tr:hover {
  background-color: #005C53;
  cursor: pointer;
}

.no-posts {
  color: white;
  font-size: 1.2rem;
  text-align: center;
  margin-top: 1rem;
}
</style>
