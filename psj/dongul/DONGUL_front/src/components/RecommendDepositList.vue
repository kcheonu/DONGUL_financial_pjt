<template>
    <div>
      <h2>추천 예금 상품</h2>
      <ul>
        <li v-for="product in depositProducts" :key="product.id">
          {{ product.name }} - {{ product.bank }} - {{ product.interest_rate }}%
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        depositProducts: [], // 추천 예금 상품 데이터
      };
    },
    created() {
      // Django API에서 추천 리스트 가져오기
      axios.get('http://localhost:8000/recommendations/')
        .then(response => {
          this.depositProducts = response.data.deposit_products;
        })
        .catch(error => {
          console.error("추천 예금 상품 가져오기 오류:", error);
        });
    }
  };
  </script>
  