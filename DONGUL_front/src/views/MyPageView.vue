<template>
  <div class="container">
    <header class="tabs">
      <RouterLink 
        :to="{ name: 'myPage', params: { username: userStore.userInfo.username }}" 
        exact-active-class="active"
        class="tab"
      >
        회원 정보 관리
      </RouterLink>

      <RouterLink 
        :to="{ name: 'productRecommend', params: { username: userStore.userInfo.username }}" 
        exact-active-class="active"
        class="tab"
      >
        상품 추천 받기
      </RouterLink>
    </header>
    <RouterView />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()
</script>



<style scoped>
/* 컨테이너 스타일 수정 */
.container {
  width: 1000px;
  margin: 2rem auto;
  padding-top: 100px; /* 네비게이션 바 높이 + 여유 공간 */
  justify-content: center;
}

/* 탭 컨테이너 스타일 */
.tabs {
  display: flex;
  justify-content: center; /* 중앙 정렬 */
  gap: 30px; /* 탭 간 간격 */
  margin-bottom: 20px; /* 하단 여백 */
  border-bottom: 2px solid #e0e0e0; /* 하단 경계선 */
  padding-bottom: 10px;
}

/* 탭 링크 스타일 */
.tab {
  font-weight: 600;
  font-size: 20px;
  letter-spacing: -0.5px;
  color: #222;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 10px;
  transition: all 0.3s ease;
}

/* 활성 탭 스타일 */
.tab.active {
  color: white;
  background-color: #3CB371;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 그림자 효과 */
}

/* 탭 링크 호버 효과 */
.tab:hover {
  color: #3CB371;
  background-color: #f5f5f5;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
