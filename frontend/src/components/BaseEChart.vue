<template>
  <div class="chartId">
    <div :id="id" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<!--<base-chart-line :option="option"></base-chart-line>-->
<script>
  import * as echarts from 'echarts'

  export default {
    name: 'BaseEChart',
    props: {
      eOption: {
        type: Object,
        default: () => {}
      },
      id: {
        type: String,
        required: true
      },
      height: {
        type: Number,
        required: false
      }
    },
    data() {
      return {
        myChart: null
      }
    },
    mounted() {
      if (this.height) document.getElementById(this.id).style.height = this.height + "px"

      this.myChart = echarts.init(document.getElementById(this.id))
      this.initData()
    },
    methods: {
      initData() {
        const that = this
        setTimeout(() => {
          that.myChart.setOption(that.eOption)
        }, 500)
      }
    },
    watch: {
      eOption: function() {
        this.initData()
      }
    }
  }
</script>

<style lang="less" scoped>
</style>
