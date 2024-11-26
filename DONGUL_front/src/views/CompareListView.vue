<template>
  <div class="container">
    <header class="header">
      <RouterLink
        :to="{ name: 'depositList' }"
        class="tab"
        exact-active-class="active"
      >
        정기예금
      </RouterLink>
      <RouterLink
        :to="{ name: 'savingList' }"
        class="tab"
        exact-active-class="active"
      >
        정기적금
      </RouterLink>
    </header>
    <RouterView />
  </div>
</template>

<script setup>

</script>



<style scoped>
.container {
  width: 100%;
  max-width: 1440px;
  margin: 2rem auto;
  padding-top: 100px;
  text-align: center; /* 전체 컨텐츠 중앙 정렬 */
}

/* 헤더 스타일 */
.header {
  display: flex;
  justify-content: center; /* 버튼 중앙 정렬 */
  gap: 20px; /* 버튼 간 간격 */
  margin-bottom: 2rem;
}

/* 탭 버튼 스타일 */
.tab {
  display: inline-block;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: 600;
  color: #444;
  text-decoration: none;
  border: 2px solid transparent;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.tab:hover {
  background-color: #f1f1f1;
  color: #222;
}

.tab.active {
  border-color: #08ba32;
  background-color: #e7ffe7;
  color: #08ba32;
}
</style>
