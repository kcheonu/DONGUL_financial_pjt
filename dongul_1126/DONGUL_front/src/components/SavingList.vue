<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/users'
import { useRouter } from 'vue-router'
import BarChartDetail from '@/components/BarChartDetail.vue'

const headers = [
  { title: '금융회사명', align: 'start', sortable: true, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월', align: 'center', width: '12%', key: '6month' },
  { title: '12개월', align: 'center', width: '12%', key: '12month' },
  { title: '24개월', align: 'center', width: '12%', key: '24month' },
  { title: '36개월', align: 'center', width: '12%', key: '36month' },
]

const results = ref()
const savings = ref([]) // 전체 금융상품 리스트
const filteredSavings = ref([]) // 필터링된 금융상품 리스트
const savingLength = computed(() => filteredSavings.value.length) // 필터링된 금융상품 개수

// Bank filter
const bankOptions = ref([])
const selectedBanks = ref([])
const bankSearch = ref('') // Search input for banks
const showAllBanks = ref(false) // Toggle for showing more banks

// Join way filter
const joinWayOptions = ref(['영업점', '인터넷', '스마트폰', '전화(텔레뱅킹)', '모바일', '창구'])
const selectedJoinWays = ref([])

// Month filter
const monthOptions = ref(['6개월', '12개월', '24개월', '36개월'])
const selectedMonths = ref([])

// Saving type filter (자유적립식 / 정액적립식)
const savingTypes = ref(['자유적립식', '정액적립식'])
const selectedSavingTypes = ref([]) // 자유/정액 적립식 선택

// User store
const userStore = useUserStore()
const router = useRouter()

const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref()
const selectedSaving = ref()
const selectedSavingCode = computed(() => {
  return selectedSavingSimple.value?.['saving_code']
})
const dialog = ref(false)

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const intrRateF = ref([null, null, null, null])
const intrRate2F = ref([null, null, null, null])
const intrRateS = ref([null, null, null, null])
const intrRate2S = ref([null, null, null, null])

const selectedTypeRsrv = ref('자유적립식')

const isContractSaving = computed(() => {
  return userStore.userInfo?.contract_saving.some(e => e['saving_code'] === selectedSavingCode.value)
})


// Create item structure
const makeItems = (item) => ({
  saving_code: item.saving_code,
  kor_co_nm: item.kor_co_nm,
  name: item.name,
  join_way: item.join_way,
  saving_type: item.saving_type, // 자유적립식 or 정액적립식
  '6month': null,
  '12month': null,
  '24month': null,
  '36month': null,
  ...item.savingoption_set.reduce((options, option) => {
    options[`${option.save_trm}month`] = option.intr_rate
    return options
  }, {}),
})

// Fetch all savings
const getAllSavings = () => {
  axios.get(`${userStore.API_URL}/financial/saving_list/`)
    .then((res) => {
      const results = res.data
      savings.value = results.map(makeItems)
      filteredSavings.value = savings.value // 초기 데이터 설정
      bankOptions.value = [...new Set(results.map((item) => item.kor_co_nm))]
    })
    .catch((err) => console.error(err))
}

// Filter logic
const applyFilters = () => {
  filteredSavings.value = savings.value.filter((item) => {
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
    const savingTypeMatch =
      selectedSavingTypes.value.length === 0 ||
      selectedSavingTypes.value.includes(item.saving_type)
    return bankMatch && joinWayMatch && monthMatch && savingTypeMatch
  })
}

// Toggle show all banks
const toggleShowAllBanks = () => {
  showAllBanks.value = !showAllBanks.value
}

onMounted(() => {
  getAllSavings()
})


watch(selectedTypeRsrv, () => {
  savings.value = []
  selectedBank.value = '전체 보기'
  for (const item of results.value){
    savings.value.push(makeItems(item))
    if (!banks.value.includes(item['kor_co_nm'])) {
      banks.value.push(item['kor_co_nm'])
    }
  }
})

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  // router.push({ name: 'savingDetail', params: { savingCode: data['saving_code']}})
  selectedSavingSimple.value = data
  intrRateF.value = []
  intrRate2F.value = []
  intrRateS.value = []
  intrRate2S.value = []
  getSaving()
  dialog.value = true
}

const getSaving = function () {
  const savingCode = selectedSavingSimple.value['saving_code']
  axios({
    method: 'get',
    url: `${userStore.API_URL}/financial/saving_list/${selectedSavingCode.value}/`
  })
    .then((res) => {
      const data = res.data
      selectedSaving.value = {
        '가입자 수 (MYFI 기준)': data.contract_user.length,
        '공시 제출월': data['dcls_month'],
        '금융 회사명': data['kor_co_nm'],
        '금융 상품명': data['name'],
        '가입 방법': data['join_way'],
        '만기 후 이자율': data['mtrt_int'],
        '우대 조건': data['spcl_cnd'],
        '가입 대상': data['join_member'],
        '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
        '최고 한도': data['max_limit'],
        '기타 유의사항': data['etc_note']
      }

      const optionList = res.data.savingoption_set

      for (const option of optionList) {
        if (option.rsrv_type_nm === '자유적립식') {
          if (option.save_trm === "6") {
            intrRateF.value[0] = option.intr_rate
            intrRate2F.value[0] = option.intr_rate2
          } else if (option.save_trm === "12") {
            intrRateF.value[1] = option.intr_rate
            intrRate2F.value[1] = option.intr_rate2
          } else if (option.save_trm === "24") {
            intrRateF.value[2] = option.intr_rate
            intrRate2F.value[2] = option.intr_rate2
          } else if (option.save_trm === "36") {
            intrRateF.value[3] = option.intr_rate
            intrRate2F.value[3] = option.intr_rate2
          }
        } else {
          if (option.save_trm === "6") {
            intrRateS.value[0] = option.intr_rate
            intrRate2S.value[0] = option.intr_rate2
          } else if (option.save_trm === "12") {
            intrRateS.value[1] = option.intr_rate
            intrRate2S.value[1] = option.intr_rate2
          } else if (option.save_trm === "24") {
            intrRateS.value[2] = option.intr_rate
            intrRate2S.value[2] = option.intr_rate2
          } else if (option.save_trm === "36") {
            intrRateS.value[3] = option.intr_rate
            intrRate2S.value[3] = option.intr_rate2
          }
        }
      }

    })
    .catch((err) => {
      console.log(err)
    })
}

const addSavingUser = function () {
  axios({
    method: 'post',
    url: `${userStore.API_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      userStore.getUserInfo(userStore.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: userStore.userInfo.username }})
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteSavingUser = function () {
  axios({
    method: 'delete',
    url: `${userStore.API_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      userStore.getUserInfo(userStore.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
}


</script>

<template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">정기적금</span> 검색하기</h1>
    </header>

    <div class="w-50 d-flex align-center">

    </div>
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
              v-for="bank in bankOptions.filter((bank) => bank.includes(bankSearch)).slice(0, showAllBanks ? bankOptions.length : 5)"
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

        <!-- 가입 기간 필터 -->
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

    <v-dialog v-model="dialog" width="800">
      <v-card v-if="selectedSaving" class="py-5 px-3">
        <v-card-title class="d-flex align-center justify-space-between">
          <h3>{{ selectedSaving['금융 상품명'] }}</h3>
          <div v-if="userStore.isLogin">
            <v-btn
              v-if="isContractSaving"
              color="red"
              variant="flat"
              @click.prevent="deleteSavingUser"
            >가입 취소하기</v-btn>
            <v-btn
              v-else
              color="#1089FF"
              variant="flat"
              @click.prevent="addSavingUser"
            >가입하기</v-btn>
          </div>
        </v-card-title>

        <v-card-text>
          <v-table>
            <tbody>
              <tr
                v-for="(value, key) in selectedSaving"
                :key="key"
              >
                <td width="28%" class="font-weight-bold">{{ key }}</td>
                <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                <td v-else>{{ value }}</td>
              </tr>
            </tbody>
          </v-table>
          <v-divider class="my-3"></v-divider>

          <div class="mx-auto">
            <BarChartDetail
              :title="`${selectedSavingSimple.name} (자유적립식)`"
              :average-intr-rate="averageIntrRate"
              :intr-rate="intrRateF"
              :intr-rate2="intrRate2F"
            />
            <BarChartDetail
              :title="`${selectedSavingSimple.name} (정액적립식)`"
              :average-intr-rate="averageIntrRate"
              :intr-rate="intrRateS"
              :intr-rate2="intrRate2S"
            />
            <p class="text-caption">* 개월별 평균 예금 금리는 2023년 11월 기준입니다.</p>
            <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
          </div>

        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#1089FF" variant="text" @click="close">
            닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- 데이터 테이블 -->
    <v-data-table-virtual
      v-if="savingLength !== 0"
      :headers="headers"
      fixed-header
      :items-length="savingLength"
      :items="filteredSavings"
      item-value="saving_code"
      height="600"
      class="table elevation-6"
    >
      <template v-slot:item="{ item }">
        <tr @click="clickRow(item)">
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
  gap: 0.5rem;
}

.bank-checkbox-list {
  gap: 0.25rem;
  max-height: 300px;
  overflow-y: auto;
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
</style>
