<script setup>

</script>

<template>
  <div class="container">
    <header class="d-flex align-center mb-7">
      <RouterLink :to="{ name: 'depositList' }" exact-active-class="active">정기예금</RouterLink>
      <p>|</p>
      <RouterLink :to="{ name: 'savingList' }" exact-active-class="active">정기적금</RouterLink>
    </header>
    <RouterView />
  </div>
</template>

<style scoped>
.container {
  width: 1440px;
  margin: 2rem auto;
  padding-top: 100px;
}

a.active {
  color: #08ba32 !important; /* 활성화된 링크 색상 */
}

header {
  gap: 10px;
  font-size: 17px;
}

header a {
  font-weight: 600;
  font-size: 20px;
  color: #222 !important; /* 기본 링크 색상 */
  text-decoration: none;
}
</style>