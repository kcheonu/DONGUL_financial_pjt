<template>
  <div class="container">
    <div class="header">
      <h1>자유게시판</h1>
      <button
        v-if="userStore.isLogin"
        class="btn-create"
        @click="() => router.push({ name: 'postCreate' })"
      >
        글 쓰기
      </button>
    </div>
    
    <!-- Custom Table -->
    <div class="table">
      <div class="table-header">
        <div class="table-cell">제목</div>
        <div class="table-cell">작성자</div>
        <div class="table-cell">작성일</div>
      </div>
      <div 
        class="table-row" 
        v-for="post in postStore.posts" 
        :key="post.id" 
        @click="clickTr(post.id)"
      >
        <div class="table-cell">{{ post.title }}</div>
        <div class="table-cell">{{ post.user.nickname }}</div>
        <div class="table-cell">{{ post.created_at.slice(0,10) }}</div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button 
        class="page-btn"
        v-for="n in postStore.totalPage" 
        :key="n"
        :class="{ active: n === page }"
        @click="page = n"
      >{{ n }}</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'
import { useUserStore } from '@/stores/users'

const postStore = usePostStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const queryPage = route.query?.page
const page = ref(Number(queryPage))

watch(page, () => {
  postStore.getPosts(page.value)
  window.scrollTo({ left: 0, top: 0, behavior: "smooth" });
  router.push({ name: 'postList', query: { page: page.value }})
})

const clickTr = (postId) => {
  router.push({ name: 'postDetail', params: { id: postId }, query: { page: page.value }})
}

onMounted(() => {
  postStore.getPosts(page.value)
})
</script>



<style scoped>
/* 컨테이너에 상단 여백 추가 */
.container {
  width: 1000px;
  margin: 2rem auto;
  padding-top: 120px; /* 네비게이션 바 높이 + 여유 공간 */
  position: relative; /* 레이아웃 충돌 방지 */
}

/* 헤더 섹션 */
.header {
  display: flex;
  justify-content: space-between; /* 제목과 버튼 좌우 배치 */
  align-items: center;
  margin-bottom: 1rem;
}

h1 {
  font-size: 28px; /* 크기를 더 키움 */
  font-weight: 700; /* 굵은 텍스트 */
  color: #005C53; /* 눈에 띄는 녹색 톤 */
  font-family: "Poppins", sans-serif; /* 현대적이고 깔끔한 폰트 */
  text-transform: uppercase; /* 대문자로 변환 */
  letter-spacing: 2px; /* 글자 간격 추가 */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 효과 */
  margin: 0;
  padding: 0;
  border-bottom: 3px solid #D6D58E; /* 하단 밑줄 추가 */
  display: inline-block; /* 밑줄과 크기를 자연스럽게 맞춤 */
}
/* 글쓰기 버튼 스타일 */
.btn-create {
  background-color: #005C53;
  color: white;
  padding: 0.7rem 1.2rem;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  position: relative; /* 상위 요소와의 위치 충돌 방지 */
  z-index: 1; /* 버튼을 다른 요소 위로 올림 */
  transition: all 0.3s ease;
}

.btn-create:hover {
  background-color: #00796B;
}

/* 테이블 스타일 */
.table {
  display: flex;
  flex-direction: column;
  border: 3px solid #D6D58E;
  border-radius: 5px;
  overflow: hidden;
}

.table-header {
  display: flex;
  background-color: #D6D58E;
  font-weight: bold;
  padding: 10px 0;
}

.table-row {
  display: flex;
  border-bottom: 1px solid #dbdbdb;
  cursor: pointer;
  transition: background-color 0.2s;
}

.table-row:hover {
  background-color: #DBF227;
}

.table-cell {
  flex: 1;
  padding: 10px;
  text-align: left;
}

.table-cell:nth-child(1) {
  flex: 2;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.page-btn {
  background-color: transparent;
  border: 1px solid #dbdbdb;
  padding: 5px 10px;
  margin: 0 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.page-btn:hover {
  background-color: #DBF227;
  color: black;
}

.page-btn.active {
  background-color: #005C53;
  color: white;
}
</style>
