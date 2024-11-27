<template>
  <div class="main-container">
    <div class="carousel-board-wrapper">
      <v-carousel 
        cycle 
        hide-delimiters 
        show-arrows="hover" 
        height="400" 
        class="custom-carousel"
      >
        <!-- 첫 번째 슬라이드 -->
        <v-carousel-item @click="goToSignIn">
          <img src="@/assets/dongul1.png" class="carousel-image" alt="bank image">
        </v-carousel-item>

        <!-- 두 번째 슬라이드 -->
        <v-carousel-item @click="goToPostList">
          <img src="@/assets/dongul2.png" class="carousel-image" alt="sleep image">
        </v-carousel-item>

        <!-- 세 번째 슬라이드 -->
        <v-carousel-item @click="goToSavingList">
          <img src="@/assets/dongul3.png" class="carousel-image" alt="recommend image">
        </v-carousel-item>

        <!-- 네 번째 슬라이드 -->
        <v-carousel-item @click="goToNotFound">
          <img src="@/assets/dongul4.png" class="carousel-image" alt="bitcoin image">
        </v-carousel-item>
      </v-carousel>
      <br>
      <!-- 자유게시판 -->
      <!-- 자유게시판과 환율 그래프 -->
      <div class="board-graph-wrapper">
        <div class="board-container">
          <div class="board-header">
            <h2>자유게시판</h2>
            <span class="more-link" @click="goToPostList">더 보기</span>
          </div>
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
                  <td>{{ post.created_at.slice(0, 10) }}</td>
                </tr>
              </tbody>
            </v-table>
          </div>
          <p v-else class="no-posts">아직 쓴 글이 없습니다.</p>
        </div>
        <!-- 환율 그래프 -->
        <div class="exchange-container">
          <div class="board-header">
            <h2>환율 그래프</h2>
            <span class="more-link" @click="goToExchange">더 보기</span>
          </div>
          <v-carousel cycle interval="3000" hide-delimiters height="200" show-arrows="hover">
            <!-- 그래프 반복 출력 -->
            <v-carousel-item v-for="currency in ['USD', 'CAD', 'JPY(100)', 'EUR', 'GBP', 'HKD', 'CNH', 'CHF']"
              :key="currency">
              <ExchangeCard :currency="currency" :title="`${currency} 환율 그래프`" />
            </v-carousel-item>
          </v-carousel>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { useUserStore } from '@/stores/users'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'

// 추가
import ExchangeCard from '@/components/ExchangeCard.vue'

const userStore = useUserStore()
const postStore = usePostStore()
const myPosts = ref([])
const router = useRouter()

const fetchMyPosts = async () => {
  await postStore.getPosts(1) // 1페이지의 게시글만 가져옴
  myPosts.value = postStore.posts.slice(0, 5) // 최신 글 5개만 저장
}

const clickTr = (postId) => {
  router.push({ name: 'postDetail', params: { id: postId } })
}

const goToPostList = () => {
  router.push({ name: 'postList' }) // 자유게시판 라우터로 이동
}
const goToSignIn = () => {
  router.push({ name: 'signIn' }) // 자유게시판 라우터로 이동
}
const goToSavingList = () => {
  router.push({ name: 'savingList' }) // 자유게시판 라우터로 이동
}
const goToNotFound = () => {
  router.push({ name: 'notFound' }) // 자유게시판 라우터로 이동
}

onMounted(() => {
  fetchMyPosts()
})

// 추가
const goToExchange = () => {
  router.push({ name: 'exchange' }) // "더 보기" 클릭 시 환율 페이지로 이동
}
</script>



<style scoped>
/* 메인 컨테이너를 Flexbox로 설정 */
.main-container {
  display: flex;
  /* Flexbox 사용 */
  flex-direction: column;
  /* 세로 방향 정렬 */
  align-items: center;
  /* 부모 컨테이너 중앙 정렬 */
  gap: 20px;
  /* 섹션 간 간격 */
  padding-top: 100px;
  /* 네비게이션 바 높이 + 여유 공간 */
  background-color: #fff;
  /* 전체 배경 설정 */
}

/* 캐러셀과 게시판을 묶는 컨테이너 */
.carousel-board-wrapper {
  display: flex;
  /* Flexbox 사용 */
  flex-direction: column;
  /* 세로 방향 정렬 */
  align-items: flex-start;
  /* 왼쪽 기준 정렬 */
  width: 70%;
  /* 캐러셀과 동일한 너비 */
  max-width: 1000px;
  /* 최대 너비 제한 */
  margin: 0 auto;
  /* 화면 중앙 정렬 */
}

/* 캐러셀 스타일 */
.custom-carousel {
  background-color: white;
  width: 100%;
  /* 부모 컨테이너 너비를 차지 */
  height: 400px;
  /* 캐러셀 높이 */
}

/* 게시판 컨테이너 */
.board-container {
  background-color: #f9f9f9;
  width: 48%; /* 환율 그래프와 동일한 너비 */
  height: 400px; /* 동일 높이 */
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* 자유게시판과 환율 그래프를 묶는 래퍼 */
.board-graph-wrapper {
  display: flex;
  justify-content: space-between;
  /* 두 섹션 나란히 배치 */
  width: 100%;
  /* 캐러셀 너비와 동일 */
  max-width: 1000px;
}

/* 환율 그래프 스타일 */
.exchange-container {
  background-color: #f9f9f9;
  width: 48%; /* 자유게시판과 동일한 너비 */
  height: 400px; /* 자유게시판과 동일한 높이 */
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* 이미지 크기 조정 */
.carousel-image {
  cursor: pointer;
  width: 100%;
  /* 캐러셀 너비에 맞춤 */
  height: 100%;
  /* 캐러셀 높이에 맞춤 */
  object-fit: cover;
  /* 이미지 비율 유지하면서 캐러셀을 채움 */
}

.board-header {
  display: flex;
  justify-content: space-between;
  /* 제목과 "더 보기" 간 간격 배치 */
  align-items: center;
  margin-bottom: 10px;
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
  right: 5%;
  /* 오른쪽으로 배치 */
  text-align: right;
  /* 텍스트 정렬을 오른쪽으로 */
}

.item1 {
  position: absolute;
  justify-content: center;
}

.item4 {
  position: absolute;
  left: 3%;
  bottom: 20%;
  text-align: left;
  /* 텍스트 정렬을 오른쪽으로 */
}


/* 버튼 스타일 */
.caro-item-btn {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -1px;
  width: 60px;
}

.more-link {
  font-size: 14px;
  color: #3CB371;
  cursor: pointer;
  text-decoration: underline;
}

.more-link:hover {
  color: #2a9257;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  text-align: left;
  padding: 8px;
  border-bottom: 1px solid #ddd;
}

.no-posts {
  text-align: center;
  color: #999;
}
</style>
