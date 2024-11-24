<script setup>
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()
</script>

<template>
  <div>
    <v-carousel
      cycle
      hide-delimiters
      show-arrows="hover"
      height="400"
    >
      <v-carousel-item>
        <div class="caro-item-text">
          <p><span class="color">예 ∙ 적금 금리</span>를 쉽게 비교하고</p>
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
        <img src="@/assets/happy.jpg" class="caro-item-img" width="400">
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
        <img src="@/assets/sleep.jpg" class="caro-item-img" width="500">
      </v-carousel-item>

      <v-carousel-item>
        <div class="item3">
          <p><span class="color">돈</span>을 굴려보자</p>
          <div class="title">
            <p><span class="color text-h1 font-weight-bold">돈굴</span></p>
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
        <img src="@/assets/sleep2.jpg" class="caro-item-img" width="400">
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<style scoped>
.v-carousel {
  background-color: #ceb424;
  border-bottom: 1px solid #ceb424;
  width: 70%; /* 화면 너비의 70% */
  margin: 0 auto; /* 중앙 정렬 */
}
.caro-item-text {
  position: absolute;
  top: 26%;
  left: 5%;
}

.item3 {
  position: absolute;
  top: 26%;
  left: 5%;
}

.caro-item-img {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  right: 5%;
}

@media (max-width: 1250px) {
  .caro-item-img {
    right: 3%;
  }

  .caro-item-text,
  .item3 {
    left: 3%;
  }
}

@media (min-width: 1600px) {
  .caro-item-img {
    right: 7%;
  }

  .caro-item-text,
  .item3 {
    left: 7%;
  }
}


.caro-item-text {
  position: absolute;
  top: 26%;
  left: 15vw;
}

.item3 {
  position: absolute;
  top: 26%;
  left: 28vw;
}

.item3 > p {
  margin-left: 5px;
  font-size: 20px;
  font-weight: 600;
}

.caro-item-text > p {
  margin-left: 5px;
  font-size: 20px;
  font-weight: 600;
}

.title {
  margin: 5px 0;
  font-size: 40px;
  font-weight: 900;
  letter-spacing: -2px;
}

.caro-item-btn {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -1px;
}

.caro-item-img {
  position: absolute;
  right: 17vw;
}

@media (max-width: 1250px) {
  .caro-item-img {
    right: 10vw;
  }
}

@media (min-width: 1600px) {
  .caro-item-img {
    right: 20vw;
  }

  .caro-item-text {
    left: 20vw;
  }
}
</style>

