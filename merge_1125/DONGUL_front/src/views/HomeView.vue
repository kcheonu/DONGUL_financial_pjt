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
  <div class="main-container">
    <v-carousel
      cycle
      hide-delimiters
      show-arrows="hover"
      height="400"
      class="custom-carousel"
    >
      <v-carousel-item>
        <div class="caro-item-text item1">
          <p><span class="color2 text-h1 font-weight-bold">돈</span><span class="text-h3 font-weight-bold">을</span> 
            <span class="color2 text-h1 font-weight-bold">굴</span><span class="text-h3 font-weight-bold">리자</span></p>
          <div class="title">
            <p>나에게 맞는</p>
            <p><span class="color">금융상품</span>을 <span class="color">추천</span> 받자!</p>
          </div>
          <v-btn
            block
            rounded="xl"
            size="x-large"
            color="#3CB371"
            class="caro-item-btn"
            :to="userStore.isLogin ? { name: 'productRecommend', params: { username: userStore.userInfo.username }} : { name: 'signUp'}"
          >회원가입하고 추천받기</v-btn>
        </div>
        <img src="@/assets/bank1.jpg" class="carousel-image" alt="bank image">
      </v-carousel-item>

      <v-carousel-item>
        <div class="caro-item-text">
          <p>행복한 금융!!~!</p>
          <div class="title">
            <p><span class="color">김천우</span></p>
            <p>오세요!</p>
          </div>
          <v-btn
            block
            rounded="xl"
            size="x-large"
            color="#3CB371"
            class="caro-item-btn"
            :to="{ name: 'postList'}"
          >금융상품 자유 게시판 바로가기</v-btn>
        </div>
        <img src="@/assets/sleep.jpg" class="carousel-image" alt="sleep image">
      </v-carousel-item>

      <v-carousel-item>
        <div class="item4">
          <p><span class="text-h4 font-weight-bold">어렵게 <span class="color2 text-h4 font-weight-bold">직접</span> 계산하지 마세요!</span></p>
          <p><span class="text-h4 font-weight-bold">저희</span> <span class="color2 text-h4 font-weight-bold">돈굴</span>
            <span class="text-h4 font-weight-bold">이 추천해 드릴게요.</span></p>
          <v-btn
            block
            rounded="xl"
            size="small"
            color="#3CB371"
            class="caro-item-btn"
            :to="userStore.isLogin ? { name: 'productRecommend', params: { username: userStore.userInfo.username }} : { name: 'signUp'}"
          >회원가입</v-btn>
        </div>
        <img src="@/assets/recommend.jpg" class="carousel-image" alt="sleep2 image">
      </v-carousel-item>

      <v-carousel-item>
        <div class="item3">
          <p><span class="color text-h3 font-weight-bold">비트코인</span> <span class="text-h4 font-weight-bold">서비스를</span></p>
          <br>
          <p><span class="text-h4 font-weight-bold">준비중입니다.</span></p>
        </div>
        <img src="@/assets/bitcoin.jpg" class="carousel-image" alt="sleep2 image">
      </v-carousel-item>
    </v-carousel>
    <br>
    <div class="board-container">
      <h2>자유게시판</h2>
      <div v-if="myPosts.length > 0">
        <v-table class="table">
        <thead>
        <tr>
          <th>글 제목</th>
          <th>작성일</th>
        </tr>
        </thead>
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
/* 메인 컨테이너에 상단 여백 추가 */
.main-container {
  padding-top: 100px; /* 네비게이션 바 높이 + 여유 공간 */
  background-color: #fff; /* 전체 배경 설정 */
}

.board-container {
  width: 35%;
  
}

/* 캐러셀 스타일 */
.custom-carousel {
  background-color: #ceb424;
  width: 70%; /* 화면 너비의 70% */
  max-width: 1000px; /* 최대 너비 제한 */
  margin: 0 auto; /* 중앙 정렬 */
  height: 400px; /* 캐러셀 높이 */
}

/* 이미지 크기 조정 */
.carousel-image {
  width: 100%; /* 캐러셀 너비에 맞춤 */
  height: 100%; /* 캐러셀 높이에 맞춤 */
  object-fit: cover; /* 이미지 비율 유지하면서 캐러셀을 채움 */
}

/* 텍스트 스타일 */
.caro-item-text {
  position: absolute;
  top: 26%;
  left: 5%;
}

.item3 {
  position: absolute;
  /* top: 26%; */
  top: 5%;
  right: 5%; /* 오른쪽으로 배치 */
  text-align: right; /* 텍스트 정렬을 오른쪽으로 */
}

.item1 {
  position: absolute;
  justify-content: center; 
}

.item4 {
  position: absolute;
  left: 3%;
  bottom: 20%; 
  text-align: left; /* 텍스트 정렬을 오른쪽으로 */
}


/* 버튼 스타일 */
.caro-item-btn {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -1px;
  width: 60px;
}
</style>
