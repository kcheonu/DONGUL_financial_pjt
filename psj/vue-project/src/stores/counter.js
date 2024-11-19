import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 회원가입 요청 액션
  const signUp = function (payload) {
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, password1, password2, email, nickname, age } = payload

    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/registration/`,
      data: {
        username, password1, password2, email, nickname, age
      }
    })
    // 팝업없이 회원가입은 잘 됨
      .then((res) => {
        // console.log(res)
        console.log('회원가입 성공')
        // const password = password1
        // logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
      // 팝업창을 띄우려 했는데, 회원가입은 되지만 팝업창을 띄우는데 오류 발생
      // 241119
  //     .then(() => {
  //       // SweetAlert2 팝업 창
  //       Swal.fire({
  //         title: '회원가입 성공',
  //         text: '회원가입이 성공적으로 완료되었습니다!',
  //         icon: 'success',
  //         confirmButtonText: '확인',
  //       }).then(() => {
  //         // 확인 버튼 클릭 시 로그인 화면으로 이동
  //         router.push({ name: 'LogInView' });
  //       });
  //     })
  //     .catch((err) => {
  //       console.error('회원가입 실패', err.response.data);
  
  //       // 오류 팝업
  //       Swal.fire({
  //         title: '회원가입 실패',
  //         text: '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.',
  //         icon: 'error',
  //         confirmButtonText: '확인',
  //       });
  //     });
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    // const username = payload.username
    // const password1 = payload.password
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        router.push({ name: 'ArticleView' })
        // console.log(res.data)
        // console.log('로그인 성공')
      })
      .catch((err) => {
        console.log(err.response.data)
      })
  }
  
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }
  return { articles, API_URL, getArticles, signUp, logIn, token, isLogin, logOut }
}, { persist: true })
