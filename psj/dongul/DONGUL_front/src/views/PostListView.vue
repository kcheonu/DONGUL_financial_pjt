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
  router.push({ name: 'postDetail', params: {id: postId }, query: { page: page.value }})
}

onMounted(() => {
  postStore.getPosts(page.value)
})
</script>

<template>
  <div class="container">
    <div class="d-flex justify-space-between align-end">
      <h1>자유게시판</h1>
      <button
        v-if="userStore.isLogin"
        class="btn-create"
        @click="() => router.push({ name: 'postCreate' })"
      >글 쓰기</button>
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

<style scoped>
.container {
  width: 1000px;
  margin: 2rem auto;
}

.container > * {
  margin: 1rem;
}

.btn-create {
  background-color: #005C53;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: bold;
}

.btn-create:hover {
  background-color: #005C53;
}

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