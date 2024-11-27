<template>
  <div>
    <h1><span class="color">{{ userStore.userInfo.nickname }}</span>님의 가입 상품 관리 페이지</h1>
    <v-divider class="my-3"></v-divider>
    <v-container>
      <v-row>
        <v-col cols="3">
          <h2>가입한 상품들</h2>
        </v-col>
        <v-col cols="9" class="d-flex flex-column">
          <p
            v-if="products.length !== 0"
            v-for="product in products"
            :key="product.code"
            class="mb-2"
          >
            {{ product.id }} : ({{ product.type }}) {{ product.bankName }} - <span class="color">{{ product.name }}</span>

            <v-btn
              size="small"
              density="comfortable"
              variant="tonal"
              rounded="xl"
              color="red"
              @click.prevent="deleteProductUser(product)"
            >가입 취소하기</v-btn>
          </p>
          <p v-else class="mb-15">가입한 상품이 없네요. 금리 비교를 통해 상품에 가입하시겠어요?</p>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const userStore = useUserStore()

const products = ref([])

const getProducts = function () {
  const deposits = userStore.userContractDeposits
  const savings = userStore.userContractSavings
  let id = 1

  for (const deposit of deposits) {
    const temp = {
      id: id++,
      code: deposit.deposit_code,
      type: '정기예금',
      bankName: deposit.kor_co_nm,
      name: deposit.name,
    }
    products.value.push(temp)
  }

  for (const saving of savings) {
    const temp = {
      id: id++,
      code: saving.saving_code,
      type: '정기적금',
      bankName: saving.kor_co_nm,
      name: saving.name,
    }
    products.value.push(temp)
  }
}

const deleteProductUser = function (data) {
  const answer = window.confirm('정말 가입을 취소하시겠습니까?')

  if (answer) {
    const isDeposit = data.type === '정기예금'
    const url = isDeposit
      ? `${userStore.API_URL}/financial/deposit_list/${data.code}/contract/`
      : `${userStore.API_URL}/financial/saving_list/${data.code}/contract/`

    axios({
      method: 'delete',
      url: url,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then(() => {
        userStore.getUserInfo(userStore.userInfo.username)
        products.value = products.value.filter((product) => product.code !== data.code)
      })
      .catch((err) => console.error(err))
  }
}

onMounted(() => {
  getProducts()
})
</script>




<style scoped>
tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}
</style>
