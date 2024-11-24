<script setup>
import Nav from '@/components/Nav.vue'
import Footer from '@/components/Footer.vue'
// import DarkMode from '@/components/DarkMode.vue'

</script>

<template>
  <div>
    <header>
      <Nav></Nav>
      <div class="hr"></div>
    </header>
    <!-- <DarkMode></DarkMode> -->
    <RouterView />
    <Footer class="footer"/>
  </div>
</template>

<style scoped>
.hr {
  height: 1px;
  background-color: #dbdbdb;
}

.footer {
  /* position: absolute;
  bottom: -200px; */
  position: relative;
  bottom: -150px;
  transform : translateY(100%);
}
</style>

<style>
.color {
  color: #3CB371;
}
</style>  