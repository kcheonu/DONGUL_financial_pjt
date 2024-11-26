<template>
  <div>
    <div v-if="post" class="container">
      
      <!-- 게시물 제목 및 작성자 -->
      <header class="post-header">
        <h1 class="post-title">{{ post.title }}</h1>
        <div class="author-info d-flex align-center">
          <v-avatar size="small" class="mr-2">
            <v-img
              cover
              :src="`${userStore.API_URL}${post.user.profile_img}`"
              alt="profile-img"
            ></v-img>
          </v-avatar>
          <p class="author-name">{{ post.user.nickname }}</p>
        </div>
        <div class="post-meta">
          <span class="text-caption">작성일 : 
            {{ post.created_at.slice(0, 4) }}년 
            {{ post.created_at.slice(5, 7) }}월 
            {{ post.created_at.slice(8, 10) }}일 
            {{ post.created_at.slice(11, 16) }}  
          </span>
          <br>
          <span v-if="isPostedUser" class="text-caption">수정일 : 
            {{ post.updated_at.slice(0, 4) }}년 
            {{ post.updated_at.slice(5, 7) }}월 
            {{ post.updated_at.slice(8, 10) }}일 
            {{ post.updated_at.slice(11, 16) }} 
          </span>
        </div>
        <div v-if="isPostedUser" class="action-buttons">
          <v-btn
            size="small"
            color="#5cb85c"
            class="mr-2"
            :to="{ name: 'postUpdate', params: { id: postId }, query: { page: pageNum }}"
          >수정</v-btn>
          <v-btn
            size="small"
            color="#d9534f"
            @click.prevent="deletePost"
          >삭제</v-btn>
        </div>
      </header>
      
      <v-divider class="my-4"></v-divider>

      <!-- 게시물 내용 -->
      <main class="post-content">
        <article v-html="post.content" class="text-body-1"></article>
      </main>

      <v-divider class="my-4"></v-divider>

      <!-- 댓글 섹션 -->
      <section class="comments-section">
        <h3 class="comments-title">댓글</h3>
        <div v-if="userStore.isLogin" class="comment-input">
          <v-form @submit.prevent="createComment">
            <v-text-field
              label="댓글 작성"
              color="#5cb85c"
              variant="outlined"
              v-model="commentContent"
              class="mr-3"
            ></v-text-field>
            <v-btn
              color="#5cb85c"
              @click.prevent="createComment"
            >
              작성
            </v-btn>
          </v-form>
        </div>

        <!-- 댓글 목록 -->
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="comment-card d-flex flex-column"
        >
          <div class="d-flex align-center mb-2">
            <v-avatar size="x-small" class="mr-2">
              <v-img
                cover
                :src="`${userStore.API_URL}${comment.user.profile_img}`"
                alt="profile-img"
              ></v-img>
            </v-avatar>
            <p class="comment-author">{{ comment.user.nickname }}</p>
          </div>
          <div class="comment-content" v-html="comment.content"></div>
          <div v-if="comment.user.username === userStore.userInfo.username" class="comment-actions">
            <v-btn
              size="small"
              color="#5cb85c"
              class="mr-2"
              @click="editComment(comment.id, comment.content)"
            >수정</v-btn>
            <v-btn
              size="small"
              color="#d9534f"
              @click="deleteComment(comment.id)"
            >삭제</v-btn>
          </div>
        </div>
      </section>
    </div>

    <!-- 로딩 스피너 -->
    <div v-else class="loading">
      <v-progress-circular
        color="#1089FF"
        indeterminate
        size="80"
      ></v-progress-circular>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, createCommentVNode } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const route = useRoute()
const postId = route.params.id
const router = useRouter()
const pageNum = route.query.page

const post = ref()
const comments = ref()

const dialog = ref(false)
const isPostedUser = ref(false)
const commentContent = ref('')
const updatedCommentId = ref()
const updatedCommentContent = ref('')

const userStore = useUserStore()

const getComments = function () {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/posts/${postId}/comments/`
  })
    .then((res) => {
      comments.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
}

onMounted(() => {
  axios({
      method: 'get',
      url: `${userStore.API_URL}/posts/${postId}/`
    })
      .then((res) => {
        // setTimeout(() => {
        //   post.value = res.data
        //   if (post.value.user.username === userStore.userInfo.username) {
        //     isPostedUser.value = true
        //   }
        // }, 300)
        post.value = res.data
        post.value.content = res.data.content.replaceAll("\n", "<br />")
        
        if (post.value.user.username === userStore.userInfo.username) {
          isPostedUser.value = true
        }
      })
      .catch((err) => {
        console.log(err)
      })

  getComments()
})

const deletePost = function () {
  const answer = window.confirm('정말 삭제하시겠습니까?')

  if (answer) {
    axios({
      method: 'delete',
      url: `${userStore.API_URL}/posts/${postId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        router.push({ name: 'postList', query: { page: pageNum }})
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const createComment = function () {
  axios({
    method: 'post',
    url: `${userStore.API_URL}/posts/${postId}/comments/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    },
    data: {
      content: commentContent.value
    }
  })
    .then((res) => {
      comments.value.push(res.data)
      commentContent.value = ''
      setTimeout(() => {
        window.scrollTo({ left: 0, top: document.body.scrollHeight+100, behavior: "smooth" });
      }, 200)
      
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteComment = function (commentId) {
  const answer = window.confirm('정말 삭제하시겠습니까?')

  if (answer) {
    axios({
      method: 'delete',
      url: `${userStore.API_URL}/posts/${postId}/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        comments.value = comments.value.filter((comment) => comment.id != commentId)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const close = function () {
  dialog.value = false
}

const editComment = function (commentId, value) {
  updatedCommentId.value = commentId
  updatedCommentContent.value = value
  
  dialog.value = true
}

const save = function () {
  axios({
    method: 'put',
    url: `${userStore.API_URL}/posts/${postId}/comments/${updatedCommentId.value}/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    },
    data: {
      content: updatedCommentContent.value
    }
  })
    .then((res) => {
      getComments()
      dialog.value = false
    })
    .catch((err) => {
      console.log(err)
    })
}
</script> 



<style scoped>
.container {
  width: 900px;
  margin: 2rem auto;
  font-family: 'Arial', sans-serif;
  padding-top: 100px;
}

/* 게시물 제목 및 작성자 */
.post-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.post-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.author-info {
  font-size: 14px;
  color: #6c757d;
}

.post-meta {
  font-size: 12px;
  color: #adb5bd;
}

.action-buttons {
  margin-top: 10px;
}

/* 게시물 내용 */
.post-content {
  font-size: 16px;
  line-height: 1.6;
  color: #343a40;
}

/* 댓글 섹션 */
.comments-section {
  margin-top: 20px;
}

.comments-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.comment-input {
  margin-bottom: 20px;
  
  align-items: center;
  width: 100%;
}

.comment-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #f8f9fa;
}

.comment-author {
  font-size: 14px;
  font-weight: bold;
  color: #495057;
}

.comment-content {
  font-size: 14px;
  margin: 10px 0;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.comment-text-field {
  flex: 1; /* 부모 컨테이너 안에서 남은 공간을 차지 */
  max-width: 800px; /* 최대 너비 제한 */
}
/* 로딩 스피너 */
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

</style>
