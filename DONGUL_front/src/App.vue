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

<script setup>
import Nav from '@/components/Nav.vue'
import Footer from '@/components/Footer.vue'
// import DarkMode from '@/components/DarkMode.vue'

</script>

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

.color2 {
  color: #DBF227;
}

</style>  
