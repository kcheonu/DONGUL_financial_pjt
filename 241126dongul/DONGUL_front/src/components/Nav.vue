<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()
</script>

<template>
  <div class="nav">
    <RouterLink class="logo" :to="{ name: 'home' }">
      <img src="@/assets/logo.png" alt="logo" />
      <span class="logo-text">DONGUL</span>
    </RouterLink>

    <div class="menus">
      <RouterLink class="menu-item" :to="{ name: 'depositList' }">
        금리비교
      </RouterLink>
      <RouterLink class="menu-item" :to="{ name: 'exchange' }">
        환율계산
      </RouterLink>
      <RouterLink class="menu-item" :to="{ name: 'bankMap' }">
        주변은행
      </RouterLink>
      <RouterLink class="menu-item" :to="{ name: 'postList', query: { page: 1 } }">
        커뮤니티
      </RouterLink>
    </div>

    <div v-if="!userStore.isLogin" class="sign">
      <v-btn
        
        variant="outlined"
        class="sign-btn"
        :to="{ name: 'signIn' }"
      >
        로그인
      </v-btn>
      <v-btn
        color="#28A745"
        variant="flat"
        class="sign-btn"
        :to="{ name: 'signUp' }"
      >
        회원가입
      </v-btn>
    </div>
    <div v-else class="sign">
      <v-btn
                rounded
                variant="text"
                class="menu-btn"
                size="large"
                :to="{ name: 'myPage', params: { username: userStore.userInfo.username }}"
              >
                마이페이지
              </v-btn>
              <v-btn
                rounded
                variant="text"
                class="menu-btn"
                size="large"
                @click.prevent="userStore.logOut"
              >
                로그아웃
              </v-btn>
      </div>
  </div>
  
</template>

<style scoped>
/* 네비게이션 바 스타일 */
.nav {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 15%;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 10;
}

/* 로고 스타일 */
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo img {
  height: 40px;
}

.logo-text {
  font-size: 30px;
  font-family: "Poppins", sans-serif;
  color: #3CB371;
  font-weight: bold;
  letter-spacing: -0.5px;
}

/* 메뉴 스타일 */
.menus {
  display: flex;
  gap: 20px;
}

.menu-item {
  font-family: "Poppins", sans-serif;
  font-size: 18px;
  font-weight: 500;
  color: #333333;
  text-decoration: none;
  transition: color 0.3s;
}

.menu-item:hover {
  color: #3CB371;
}

/* 로그인/회원가입 버튼 스타일 */
.sign {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sign-btn {
  font-family: "Poppins", sans-serif;
  font-size: 14px;
  font-weight: 600;
  border-radius: 20px;
  padding: 8px 16px;
  transition: background-color 0.3s, color 0.3s;
  color: #3CB371;
}

.sign-btn:hover {
  background-color: #3CB371;
  color: #ffffff;
}

/* 유저 메뉴 스타일 */
.card {
  width: 200px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.username {
  font-size: 20px;
  font-family: "Poppins", sans-serif;
  color: #333333;
  margin: 8px 0;
}

.nickname {
  font-size: 16px;
  font-family: "Poppins", sans-serif;
  color: #666666;
}

.menu-btn {
  color: #3CB371;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s;
}

.menu-btn:hover {
  color: #3CB371;
}
</style>
