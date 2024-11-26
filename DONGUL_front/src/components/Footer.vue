<template>
  <footer class="px-5 py-10">
    <div class="upper mx-3">
      <RouterLink class="logo" :to="{ name: 'home' }">
        <img src="@/assets/logo.png" alt="logo" />
        DONGUL
      </RouterLink>
    </div>
    <v-divider class="my-3"></v-divider>
    <div class="d-flex flex-row-reverse mx-3">
      <div>
        <p class="font-weight-bold" style="color: white;">본 사이트의 콘텐츠는 저작권법의 보호를 받는 바 무단 전재, 복사, 배포 등을 금합니다.</p>
        <p class="font-italic" style="color: white;">Copyright ©DONGUL All Rights Reserved.</p>

      </div>
      
    </div>
    
  </footer>
</template>

<script setup>

</script>



<style scoped>
.container {
  width: 100vw;
}

footer {
  width: 100%;
  background-color: #042940;
}

.logo {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #3CB371 !important;
  font-size: 30px;
  text-decoration: none;
  font-family: 'Francois One', sans-serif;
  margin: 0 1rem;
}

.logo img {
  height: 36px;
}
</style>