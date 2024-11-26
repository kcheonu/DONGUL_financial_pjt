<script setup>
import { ref } from "vue";
import ExchangeCalculater from "@/components/ExchangeCalculater.vue";
import ExchangeCard from "@/components/ExchangeCard.vue";

const currencies = [
  { unit: "USD", name: "미국 달러" },
  { unit: "CAD", name: "캐나다 달러" },
  { unit: "CHF", name: "스위스 프랑" },
  { unit: "JPY(100)", name: "일본 옌" },
  { unit: "HKD", name: "홍콩 달러" },
  { unit: "GBP", name: "영국 파운드" },
  { unit: "EUR", name: "유로" },
  { unit: "CNH", name: "위안화" },
];
</script>

<template>
  <div class="container">
    <br>
    <h1 class="mb-5"><span class="color">환율</span> 변화 그래프</h1>
    <div class="elevation-6">
      <div class="grid-container">
        <ExchangeCard
          v-for="currency in currencies"
          :key="currency.unit"
          :currency="currency.unit"
          :title="`${currency.name} 환율 변화`"
        />
      </div>
    </div>
    <br>
    <h1 class="mb-5"><span class="color">환율</span> 계산기</h1>
    <ExchangeCalculater class="elevation-6" />
  </div>
</template>

<style scoped>
.container {
  width: 100%;
  margin: 2rem auto;
  text-align: center;
  padding-top: 100px;
}
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
</style>
