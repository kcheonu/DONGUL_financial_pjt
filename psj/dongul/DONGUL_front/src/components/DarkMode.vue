<template>
 <div id="app">
    <div class="flex">
        <h1>Dark Mode toggle</h1>
        <div class="mode-toggle" @click="modeToggle" :class="darkDark">
            <div class="toggle">
                <div id="dark-mode" type="checkbox"></div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
var app = new Vue({
    el: '#app',
    
    data() {
        return {
            darkMode: false
        }
    },
    
    methods: {
        dark() {
            document.querySelector('body').classList.add('dark-mode')
            this.darkMode = true
            this.$emit('dark')
        },

        light() {
            document.querySelector('body').classList.remove('dark-mode')
            this.darkMode = false
            this.$emit('light')
        },

        modeToggle() {
            if(this.darkMode || document.querySelector('body').classList.contains('dark-mode')) {
                this.light()
            } else {
                this.dark()
            }
        },
    },
    
    computed: {
        darkDark() {
            return this.darkMode && 'darkmode-toggled'
        }
    }
})
</script>

<style>
/* 변수 대신 실제 색상 값 사용 */
body {
  background-color: #fff;
  color: #171717;
  transition: background-color 0.2s ease, color 0.2s ease;
}

body.dark-mode {
  background-color: #2a2a2a; /* lighten(#171717, 10%) */
}

.flex h1 {
  color: #171717;
}

body.dark-mode .flex h1 {
  color: #fff;
}

.mode-toggle {
  position: relative;
  padding: 0;
  width: 44px;
  height: 24px;
  background-color: #262626;
  border: 0;
  border-radius: 24px;
  outline: 0;
  cursor: pointer;
  transition: background-color 0.5s ease;
}

.mode-toggle .toggle {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: #fff;
  border-radius: 50%;
  transition: transform 0.5s ease;
}

body.dark-mode .mode-toggle {
  background-color: #313131; /* lighten(#262626, 5%) */
}

body.dark-mode .mode-toggle .toggle {
  transform: translateX(20px);
}

.flex {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
}

h1 {
  font-weight: 400;
  transition: color 0.5s ease;
}
</style>
