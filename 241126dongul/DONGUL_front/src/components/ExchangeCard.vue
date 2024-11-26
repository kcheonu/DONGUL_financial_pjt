<template>
  <v-card>
    <v-form>
      <div class="exchange-graph">
        <h2>{{ title }}</h2>
        <div v-if="isLoading" class="loading-message">
          데이터를 로딩 중입니다...
        </div>
        
        <div v-else>
          <canvas :id="`${currency}Chart`" v-if="exchangeData.length"></canvas>
        </div>
      </div>
    </v-form>
  </v-card>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  props: {
    currency: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isLoading: true,
      exchangeData: [],
      chartInstance: null,
      currencyColors: {
        USD: "rgba(75, 192, 192, 1)",
        CAD: "rgba(255, 99, 132, 1)",
        CHF: "rgba(153, 102, 255, 1)",
        JPY: "rgba(255, 206, 86, 1)",
        HKD: "rgba(54, 162, 235, 1)",
        GBP: "rgba(255, 159, 64, 1)",
        EUR: "rgba(201, 203, 207, 1)",
        CNY: "rgba(50, 255, 132, 1)",
      },
    };
  },
  methods: {
    async fetchExchangeRates() {
      try {
        const response = await axios.get(
          "http://localhost:8000/exchange/selected_currencies/"
        );
        if (response.data) {
          this.processData(response.data);
        } else {
          console.error("환율 데이터를 불러올 수 없습니다.");
        }
      } catch (error) {
        console.error("환율 데이터를 가져오는 중 오류 발생:", error);
      } finally {
        this.isLoading = false;
      }
    },

    processData(data) {
      const filteredData = data
        .filter((item) => item.cur_unit === this.currency)
        .map((item) => ({
          id: item.id,
          rate: parseFloat(item.deal_bas_r.replace(/,/g, "")),
        }));

      filteredData.sort((a, b) => a.id - b.id);
      this.exchangeData = filteredData;

      this.$nextTick(() => {
        this.ensureCanvasReady();
      });
    },

    ensureCanvasReady(attempts = 0, maxAttempts = 5) {
      const canvas = document.getElementById(`${this.currency}Chart`);
      if (canvas) {
        this.renderChart(canvas);
      } else if (attempts < maxAttempts) {
        console.warn(`Canvas not found for ${this.currency}, retrying...`);
        setTimeout(() => {
          this.ensureCanvasReady(attempts + 1, maxAttempts);
        }, 500);
      } else {
        console.error(`Canvas not found for ${this.currency} after ${maxAttempts} attempts.`);
      }
    },

    renderChart(canvas) {
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      const ctx = canvas.getContext("2d");
      const color = this.currencyColors[this.currency] || "rgba(0, 0, 0, 1)"; // 기본 색상은 검정

      this.chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: this.exchangeData.map((_, index) => index + 1),
          datasets: [
            {
              label: `${this.currency} 환율`,
              data: this.exchangeData.map((entry) => entry.rate),
              borderColor: color,
              backgroundColor: color.replace("1)", "0.2)"), // 투명도 적용
              borderWidth: 2,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
          },
          scales: {
            x: {
              ticks: {
                display: false,
              },
            },
            y: {
              title: {
                display: true,
                text: "환율",
              },
            },
          },
        },
      });
    },
  },
  mounted() {
    this.fetchExchangeRates();
  },
};
</script>

<style scoped>
.exchange-graph {
  max-width: 350px;
  margin: 10px auto;
  text-align: center;
}
.loading-message {
  text-align: center;
  font-size: 1.5em;
  color: #666;
  margin: 20px 0;
}
</style>
