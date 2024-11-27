<template>
  <div>
    <h1><span class="color">{{ userStore.userInfo.nickname }}</span>님의 가입 상품 관리 페이지</h1>
    <v-divider class="my-3"></v-divider>

    <div v-if="!isExistInfo" class="d-flex flex-column justify-center align-center">
      
      <h1>마이페이지에서 <span class="color">회원 정보</span> 입력을 완료해주세요!</h1>
    </div>

    <div v-else-if="!loading">

      <v-dialog v-model="dialog" width="800">
        <v-card v-if="selectedProduct" class="py-5 px-3">
          <v-card-title class="d-flex align-center justify-space-between">
            <h3>{{ selectedProduct['금융 상품명'] }}</h3>
            <div v-if="userStore.isLogin">
              <v-btn
              v-if=" isContractDeposit"
              color="#DBF227"
              variant="flat"
              @click.prevent="deleteDepositUser"
            >가입 취소하기</v-btn>
            <v-btn
              v-else
              color="#3CB371"
              variant="flat"
              @click.prevent="addDepositUser"
            >가입하기</v-btn>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="#3CB371" variant="text" @click="close">
                [닫기]
              </v-btn>
            </v-card-actions>
            </div>
          </v-card-title>

          <v-card-text>
            <v-table>
              <tbody>
                <tr
                  v-for="(value, key) in selectedProduct"
                  :key="key"
                >
                  <td width="25%" class="font-weight-bold">{{ key }}</td>
                  <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                  <td v-else>{{ value }}</td>
                </tr>
              </tbody>
            </v-table>
            <v-divider class="my-3"></v-divider>

      
            
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="#1089FF" variant="text" @click="close">
              [닫기]
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-card class="elevation-3" outlined>
      <!-- 탭 영역 -->
      <v-tabs
        v-model="tab"
        grow
        color="#3CB371"
        background-color="#3CB371"
        align-tabs="center"
        class="py-2"
      >
        <v-tab value="one" class="font-weight-bold text-primary green-text">
          비슷한 사람들의 추천
        </v-tab>
        <v-tab value="two" class="font-weight-bold text-primary green-text">
          희망 조건 기반 추천
        </v-tab>
      </v-tabs>

      <!-- 카드 텍스트 영역 -->
      <v-card-text class="px-6 py-4">
        <v-window v-model="tab" class="mt-4">
          <!-- 첫 번째 탭 내용 -->
          <v-window-item value="one">
            <p class="font-weight-medium text-h6 mb-2">
              고객님과 나이, 자산, 연봉이 비슷한 유저들이 가입한 상품을 추천합니다!
            </p>
            <p class="text-body-2 text-secondary mb-4">
              나이에 따라 자산과 연봉의 가중치가 다릅니다.
              자산이 많으면 최대가입금액이 높은 상품을, 연봉이 많으면 금리가 높은상품을 추천합니다!  
            </p>
            <p
              v-if="isNotSimilarUsers"
              class="ml-5"
            ><br>비슷한 유저가 없습니다<br>대신 모든 유저들이 많이 가입한 상품 top 20을 준비했습니다!
            <br>
            <br>
            </p>
            <!-- 은행 선택 드롭다운 -->
            <v-select
              v-model="selectedBank2"
              :items="uniqueBanks2"
              label="선호 은행 선택"
              variant="outlined"
              color="#3CB371"
              density="compact"
              class="mb-4"
            ></v-select>

            <!-- 추천 리스트 -->
            <v-data-table-virtual
              :headers="headers"
              fixed-header
              :items="sortedRecommend2"
              item-value="code"
              height="600"
              class="elevation-1"
              @change="handleBankChange2"
            >
              <template v-slot:item="{ item }" class="bgc-color">
                <tr @click="clickRow(item)">
                  <td>{{ item['type'] }}</td>
                  <td>{{ item['kor_co_nm'] }}</td>
                  <td align="center">{{ item['name'] }}</td>
                  <td align="center">{{ item['6month'] }}</td>
                  <td align="center">{{ item['12month'] }}</td>
                  <td align="center">{{ item['24month'] }}</td>
                  <td align="center">{{ item['36month'] }}</td>
                </tr>
              </template>
            </v-data-table-virtual>
          </v-window-item>

          <!-- 두 번째 탭 내용 -->
          <v-window-item value="two">
            <p class="font-weight-medium text-h6 mb-2">
              희망 예치 금액과 기간에서 ±33% 이내의 상품들입니다.
            </p>
            <p class="text-body-2 text-secondary mb-4">
              선호은행을 선택하시면, 해당 은행상품이 최상단에 나옵니다.
            </p>

            <!-- 은행 선택 드롭다운 -->
            <v-select
              v-model="selectedBank1"
              :items="uniqueBanks1"
              label="선호 은행 선택"
              variant="outlined"
              color="#3CB371"
              density="compact"
              class="mb-4"
            ></v-select>

            <!-- 추천 리스트 -->
            <v-data-table-virtual
              :headers="headers"
              fixed-header
              :items="sortedRecommend1"
              item-value="code"
              height="600"
              class="elevation-1"
              @change="handleBankChange1"
            >
              <template v-slot:item="{ item }" class="bgc-color">
                <tr @click="clickRow(item)">
                  <td>{{ item['type'] }}</td>
                  <td>{{ item['kor_co_nm'] }}</td>
                  <td align="center">{{ item['name'] }}</td>
                  <td align="center">{{ item['6month'] }}</td>
                  <td align="center">{{ item['12month'] }}</td>
                  <td align="center">{{ item['24month'] }}</td>
                  <td align="center">{{ item['36month'] }}</td>
                </tr>
              </template>
            </v-data-table-virtual>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

    </div>

    <div v-else class="loading">
      <v-progress-circular
        color="#3CB371"
        indeterminate
        size="80"
        ></v-progress-circular>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()

const tab = ref('one')
const isExistInfo = ref(false)
const loading = ref(false)
const isNotSimilarUsers = ref(false)

const headers = [
  { title: '타입', align: 'start', sortable: false, width:'7%',key: 'type' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width:'27%', key: 'name' },
  { title: '6개월', align: 'center', width:'11%', key: '6month' },
  { title: '12개월', align: 'center', width:'11%', key: '12month' },
  { title: '24개월', align: 'center',  width:'11%', key: '24month' },
  { title: '36개월', align: 'center', width:'11%', key: '36month' },
]

const recommend1 = ref([]) // 희망 예치 금액, 기간과 비슷한 상품 추천
const recommend2 = ref([]) // 나와 비슷한 사람들이 많이 가입한 상품 추천

const makeItems = function (item, isDeposit=true) {
  const codeName = isDeposit ? 'deposit_code' : 'saving_code'
  const state = isDeposit ? '정기예금' : '정기적금'

  const result = {
    'code': item[codeName],
    'type': state,
    'dcls_month': item['dcls_month'],
    'kor_co_nm': item['kor_co_nm'],
    'name': item['name'],
    '6month': null,
    '12month': null,
    '24month': null,
    '35month': null,
  }

  const setName = isDeposit ? 'depositoption_set' : "savingoption_set"

  for (const option of item[setName]) {
    const saveTrm = option['save_trm']

    if (saveTrm === "6") {
      result['6month'] = option['intr_rate']
    } else if (saveTrm === "12") {
      result['12month'] = option['intr_rate']
    } else if (saveTrm === "24") {
      result['24month'] = option['intr_rate']
    } else if (saveTrm === "36") {
      result['36month'] = option['intr_rate']
    }
  }

  return result
}


onMounted(() => {
  loading.value = true
  userStore.getUserInfo(userStore.userInfo.username)

  if (userStore.userInfo.age && userStore.userInfo.money && userStore.userInfo.salary && userStore.userInfo.desire_amount_deposit
      && userStore.userInfo.desire_amount_saving && userStore.userInfo.deposit_period && userStore.userInfo.saving_period
    ) {
    isExistInfo.value = true
    
    // 나와 비슷한 사람들이 많이 가입한 상품 추천
    axios({
      method: 'get',
      url: `${userStore.API_URL}/financial/recommend_product_two/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        isNotSimilarUsers.value = res.data.is_not_similar_users

        const deposits2 = res.data.deposit
        const savings2 = res.data.saving

        for (const deposit of deposits2) {
          recommend2.value.push(makeItems(deposit.deposit))
        }

        for (const saving of savings2) {
          recommend2.value.push(makeItems(saving.saving, false))
        }
        loading.value = false
        // console.log(recommend2.value)
      })
      .catch((err) => {
        console.log(err)
      })

    // 희망 예치 금액, 기간과 비슷한 상품 추천
    axios({
      method: 'get',
      url: `${userStore.API_URL}/financial/recommend_product_one/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        // console.log(res.data)

        const deposits1 = res.data.deposit
        const savings1 = res.data.saving

        for (const deposit of deposits1) {
          recommend1.value.push(makeItems(deposit))
        }

        for (const saving of savings1) {
          recommend1.value.push(makeItems(saving, false))
        }
        
        // console.log(recommend1.value)
      })
      .catch((err) => {
        console.log(err)
      })
  }
})

const dialog = ref(false)

const chartReady = ref(false)
const selectedProduct = ref()
const selectedProductSimple = ref()
const selectedProductCode = computed(() => {
  return selectedProductSimple.value?.code
})

const isContractProduct = computed(() => {
  if (selectedProductSimple.value?.type === '정기예금'){
    return userStore.userInfo?.contract_deposit.some(e => e['deposit_code'] === selectedProductCode.value)
  } else if (selectedProductSimple.value?.type === '정기적금'){
    return userStore.userInfo?.contract_saving.some(e => e['saving_code'] === selectedProductCode.value)
  }
})

const isDeposit = ref()

const averageIntrRateDeposit = [3, 3.08, 3.1, 3.2]
const intrRateDeposit = ref([null, null, null, null])
const intrRate2Deposit = ref([null, null, null, null])

const averageIntrRateSaving = [2.7, 3.32, 3.4, 3.52]
const intrRateF = ref([null, null, null, null])
const intrRate2F = ref([null, null, null, null])
const intrRateS = ref([null, null, null, null])
const intrRate2S = ref([null, null, null, null])

const clickRow = function (data) {
  chartReady.value = false
  selectedProductSimple.value = data
  isDeposit.value = data.type === '정기예금' ? true : false
  intrRateDeposit.value = []
  intrRate2Deposit.value = []
  intrRateF.value = []
  intrRate2F.value = []
  intrRateS.value = []
  intrRate2S.value = []
  getProduct()
  dialog.value = true
}

const getProduct = function () {
  let url = ''
  if (isDeposit.value) {
    url = `${userStore.API_URL}/financial/deposit_list/${selectedProductCode.value}/`
  } else {
    url = `${userStore.API_URL}/financial/saving_list/${selectedProductCode.value}/`
  }

  axios({
    method: 'get',
    url: url
  })
    .then((res) => {
      const data = res.data
      console.log(res.data)
      selectedProduct.value = {
        '가입자 수': data.count,
        '공시 제출월': data.data['dcls_month'],
        '금융 회사명': data.data['kor_co_nm'],
        '금융 상품명': data.data['name'],
        '가입 방법': data.data['join_way'],
        '만기 후 이자율': data.data['mtrt_int'],
        '우대 조건': data.data['spcl_cnd'],
        '가입 대상': data.data['join_member'],
        '가입 제한': data.data['join_deny'] === 1 ? '제한없음' : data.data['join_deny'] === 2 ? '서민전용' : '일부제한',
        '최고 한도': data.data['max_limit'],
        '기타 유의사항': data.data['etc_note']
      }

      if (isDeposit.value) {
        const optionList = res.data.depositoption_set

        for (const option of optionList) {
          if (option.save_trm === "6") {
            intrRateDeposit.value[0] = option.intr_rate
            intrRate2Deposit.value[0] = option.intr_rate2
          } else if (option.save_trm === "12") {
            intrRateDeposit.value[1] = option.intr_rate
            intrRate2Deposit.value[1] = option.intr_rate2
          } else if (option.save_trm === "24") {
            intrRateDeposit.value[2] = option.intr_rate
            intrRate2Deposit.value[2] = option.intr_rate2
          } else if (option.save_trm === "36") {
            intrRateDeposit.value[3] = option.intr_rate
            intrRate2Deposit.value[3] = option.intr_rate2
          }
        }
      } else {
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
      }
      chartReady.value = true
    })
    .catch((err) => {
      console.log(err)
    })
}

const close = function () {
  dialog.value = false
}

const addSavingUser = function () {
  let url = ''
  if (isDeposit.value) {
    url = `${userStore.API_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
  } else {
    url = `${userStore.API_URL}/financial/saving_list/${selectedProductCode.value}/contract/`
  }

  axios({
    method: 'post',
    url: url,
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

const deleteProductUser = function (data) {
  const anwser = window.confirm('정말 가입을 취소하시겠습니까?')

  if (anwser) {
    selectedProductSimple.value = data
    let url = ''
    if (isDeposit.value) {
      url = `${userStore.API_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
    } else {
      url = `${userStore.API_URL}/financial/saving_list/${selectedProductCode.value}/contract/`
    }

    axios({
      method: 'delete',
      url: url,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        loading.value = true
        userStore.getUserInfo(userStore.userInfo.username)
        dialog.value = false
        setTimeout(() => {
          loading.value = false
        }, 300)
        
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
}

const selectedBank1 = ref('') // 선택된 은행
const uniqueBanks1 = computed(() => {
  // 추천 리스트(recommend1)에서 고유한 은행 이름 추출
  return [...new Set(recommend1.value.map(item => item['kor_co_nm']))]
})
// 추천 리스트를 선택된 은행에 따라 정렬
const sortedRecommend1 = computed(() => {
  if (!selectedBank1.value) return recommend1.value // 선택된 은행이 없으면 정렬하지 않음
  return recommend1.value.sort((a, b) => {
    const isSelectedA = a['kor_co_nm'] === selectedBank1.value
    const isSelectedB = b['kor_co_nm'] === selectedBank1.value
    if (isSelectedA && !isSelectedB) return -1
    if (!isSelectedA && isSelectedB) return 1
    return 0
  })
})

const selectedBank2 = ref('') // 선택된 은행
const uniqueBanks2 = computed(() => {
  // 추천 리스트(recommend2)에서 고유한 은행 이름 추출
  return [...new Set(recommend2.value.map(item => item['kor_co_nm']))]
})

// 추천 리스트를 선택된 은행에 따라 정렬
const sortedRecommend2 = computed(() => {
  if (!selectedBank2.value) return recommend2.value // 선택된 은행이 없으면 정렬하지 않음
  return recommend2.value.sort((a, b) => {
    const isSelectedA = a['kor_co_nm'] === selectedBank2.value
    const isSelectedB = b['kor_co_nm'] === selectedBank2.value
    if (isSelectedA && !isSelectedB) return -1
    if (!isSelectedA && isSelectedB) return 1
    return 0
  })
})
// 선택한 은행 변경 처리
const handleBankChange1 = (bank) => {
  selectedBank1.value = bank
}
const handleBankChange2 = (bank) => {
  selectedBank2.value = bank
}

</script>


<style scoped>
.loading {
  position: absolute;
  left: 0;
  top: 0;
  background-color: rgba(255, 255, 255, 0.6);
  display: flex;
  width: 100vw;
  height: 100vh;
  align-items: center;
  justify-content: center;
}

tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
  color: #3CB371;
}

.green-text {
  color: #3CB371 !important;
}

.bgc-color {
  color: grey;
}
</style>