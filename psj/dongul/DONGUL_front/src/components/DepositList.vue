<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/users'

const headers = [
  { title: '금융회사명', align: 'start', sortable: true, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월', align: 'center', width: '12%', key: '6month' },
  { title: '12개월', align: 'center', width: '12%', key: '12month' },
  { title: '24개월', align: 'center', width: '12%', key: '24month' },
  { title: '36개월', align: 'center', width: '12%', key: '36month' },
]

const deposits = ref([]) // Filtered deposit list
const depositLength = computed(() => deposits.value.length) // Total number of items

// Bank filter
const bankOptions = ref([])
const selectedBanks = ref([])
const showAllBanks = ref(false) // Toggle for showing more banks
const bankSearch = ref('') // Search input for banks

// Join way filter
const joinWayOptions = ref(['영업점', '인터넷', '스마트폰', '전화(텔레뱅킹)', '모바일', '창구'])
const selectedJoinWays = ref([])

// Month filter
const monthOptions = ref(['6개월', '12개월', '24개월', '36개월'])
const selectedMonths = ref([])

// User store
const userStore = useUserStore()

// Create item structure
const makeItems = (item) => ({
  deposit_code: item.deposit_code,
  kor_co_nm: item.kor_co_nm,
  name: item.name,
  join_way: item.join_way,
  '6month': null,
  '12month': null,
  '24month': null,
  '36month': null,
  ...item.depositoption_set.reduce((options, option) => {
    options[`${option.save_trm}month`] = option.intr_rate
    return options
  }, {}),
})

// Fetch all deposits
const getAllDeposit = () => {
  axios.get(`${userStore.API_URL}/financial/deposit_list/`)
    .then((res) => {
      const results = res.data
      deposits.value = results.map(makeItems)
      bankOptions.value = [...new Set(results.map((item) => item.kor_co_nm))]
    })
    .catch((err) => console.error(err))
}

// Filter logic
const filterDeposits = () => {
  axios.get(`${userStore.API_URL}/financial/deposit_list/`)
    .then((res) => {
      const results = res.data
      deposits.value = results
        .map(makeItems)
        .filter((item) => {
          const bankMatch =
            selectedBanks.value.length === 0 ||
            selectedBanks.value.includes(item.kor_co_nm)
          const joinWayMatch =
            selectedJoinWays.value.length === 0 ||
            selectedJoinWays.value.every((way) => item.join_way.includes(way))
          const monthMatch =
            selectedMonths.value.length === 0 ||
            selectedMonths.value.some((month) => {
              const monthKey = month.replace('개월', '') + 'month'
              return item[monthKey] !== null
            })
          return bankMatch && joinWayMatch && monthMatch
        })
    })
    .catch((err) => console.error(err))
}

// Apply filters
const applyFilters = () => {
  filterDeposits()
}

// Toggle show all banks
const toggleShowAllBanks = () => {
  showAllBanks.value = !showAllBanks.value
}

onMounted(() => {
  getAllDeposit()
})
</script>

<template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">정기예금</span> 검색하기</h1>
    </header>

    <!-- 필터 섹션 -->
    <section class="filter-section">
      <div class="filter-category">
        <!-- 은행 필터 -->
        <div class="filter-group card">
          <h3>은행</h3>
          <input
            type="text"
            v-model="bankSearch"
            placeholder="은행 이름 검색"
            class="filter-search"
          />
          <div class="checkbox-list bank-checkbox-list">
            <v-checkbox
              v-for="(bank, index) in bankOptions.filter((bank) => bank.includes(bankSearch)).slice(0, showAllBanks ? bankOptions.length : 5)"
              :key="bank"
              :label="bank"
              v-model="selectedBanks"
              :value="bank"
              @change="applyFilters"
            />
            <button v-if="bankOptions.length > 5" @click="toggleShowAllBanks">
              {{ showAllBanks ? '접기' : '더 보기' }}
            </button>
          </div>
        </div>

        <!-- 가입방법 필터 -->
        <div class="filter-group card">
          <h3>가입방법</h3>
          <div class="checkbox-list">
            <v-checkbox
              v-for="way in joinWayOptions"
              :key="way"
              :label="way"
              v-model="selectedJoinWays"
              :value="way"
              @change="applyFilters"
            />
          </div>
        </div>

        <!-- 개월 필터 -->
        <div class="filter-group card">
          <h3>가입 기간 (개월)</h3>
          <div class="checkbox-list">
            <v-checkbox
              v-for="month in monthOptions"
              :key="month"
              :label="month"
              v-model="selectedMonths"
              :value="month"
              @change="applyFilters"
            />
          </div>
        </div>
      </div>
    </section>

    <v-divider class="my-3"></v-divider>

    <!-- 데이터 테이블 -->
    <v-data-table-virtual
      v-if="depositLength !== 0"
      fixed-header
      :headers="headers"
      :items-length="depositLength"
      :items="deposits"
      item-value="deposit_code"
      height="600"
      class="table elevation-6"
    >
      <template v-slot:item="{ item }">
        <tr>
          <td>{{ item.kor_co_nm }}</td>
          <td align="center">{{ item.name }}</td>
          <td align="center">{{ item['6month'] }}</td>
          <td align="center">{{ item['12month'] }}</td>
          <td align="center">{{ item['24month'] }}</td>
          <td align="center">{{ item['36month'] }}</td>
        </tr>
      </template>
    </v-data-table-virtual>

    <!-- 상품이 없을 경우 표시 -->
    <div v-else class="no-data">
      선택 옵션에 맞는 금융상품이 없습니다.
    </div>
  </div>
</template>

<style scoped>
/* 은행 필터 전용 스타일 */
.bank-checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 0; /* 간격을 완전히 제거 */
  max-height: 300px; /* 최대 높이를 설정 */
  overflow-y: auto; /* 스크롤 가능하도록 설정 */
}

.bank-checkbox-list v-checkbox {
  margin-bottom: 0; /* 체크박스 간의 마진 제거 */
}

/* 공통 카드 스타일 */
.filter-section {
  background-color: #d8f5a2;
  padding: 1.5rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
}

.filter-category {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
}

.card {
  flex: 1 1 calc(33% - 1rem);
  max-width: 300px;
  background-color: #d5ecd3;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-group h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* 다른 필터의 기본 간격 */
}

.filter-search {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.no-data {
  text-align: center;
  color: #888;
  font-size: 1.2rem;
  margin-top: 2rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .filter-category {
    flex-direction: column;
    max-width: 100%;
  }

  .card {
    flex: 1 1 100%;
    max-width: 100%;
  }
}
</style>
