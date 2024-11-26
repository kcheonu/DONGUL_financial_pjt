<template>
  <div class="container">
    <!-- 팝업 구현 -->
    <v-dialog v-model="dialog" persistent width="500" class="custom-dialog">
      <v-card class="custom-card">
        <v-card-title class="custom-title text-center">
          🚫 <span class="text-bold">페이지 오류!</span>
        </v-card-title>
        <v-card-text class="custom-text text-center">
          <p>현재 이동하신 페이지는 <span class="highlight">없는 페이지</span>입니다!</p>
          <p>조만간 새로운 서비스로 찾아뵙겠습니다!</p>
        </v-card-text>
        <v-card-actions class="custom-actions">
          <v-btn color="#3CB371" @click="goToHome" rounded="xl" class="custom-button">홈으로</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const dialog = ref(true) // 페이지 접근 시 팝업 자동 열림
const router = useRouter()

const goToHome = () => {
  router.push({ name: 'home' }) // 홈으로 이동
}
</script>



<style scoped>
.container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9f9f9;
}

.custom-dialog .custom-card {
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  background: linear-gradient(145deg, #ffffff, #f3f3f3);
  padding: 20px;
}

.custom-title {
  font-size: 24px;
  font-weight: 700;
  color: #ff6b6b;
}

.custom-text {
  font-size: 16px;
  color: #555555;
}

.custom-text .highlight {
  font-weight: 600;
  color: #ff6b6b;
}

.custom-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.custom-button {
  font-size: 15px;
  text-align: center;
  /* font-weight: 600; */
  color: white !important;
  background-color: #2a9257;
  
  text-transform: uppercase;
  transition: background-color 0.3s ease;

}

.custom-button:hover {
  background-color: #248a4b;
}
</style>
