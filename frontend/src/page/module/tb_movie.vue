<template>
  <div style="height: 100%;padding: 10px;">
    <el-card class="filter-container" shadow="never">
      <div style="margin: 30px 5px;padding: 0 30%;">
        <el-input placeholder="Please input movie keyword" v-model="movieName">
          <el-button slot="append" icon="el-icon-search" style="background: #fc3737;color: #fff;" @click="search">Search</el-button>
        </el-input>
      </div>

      <el-row :gutter="20">
        <el-col v-for="(item, index) in movieList" :key="item.id"
                style="margin-top:25px;" :span="6">
          <el-card shadow="hover" style="text-align: center;">
            <div>
              <img :src="item.imgUrl" style="width:135px;height:193px;cursor: pointer;" @click="onImageClick(item)"/>
            </div>
            <div>
              <div class="text-word ellipsis">
                {{item.name}} Score{{item.score}}
              </div>
              <el-button class="button" @click="onUpClick(item.id)">UP {{item.up}}</el-button>
              <el-button class="button" @click="onDownClick(item.id)">DOWN {{item.down}}</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

  </div>
</template>

<script>
  import {oscarMixin} from '@/config/mixins'

  export default {
    mixins: [oscarMixin],
    data() {
      return {
        movieName: null,
        movieList: [
          {
            id: 1,
            imgUrl: '/static/img/hellohuanying.png',
            name: '你好，李焕英',
            director: '贾玲',
            actor: '贾玲 / 张小斐 / 沈腾 / 陈赫',
            type: '剧情 / 喜剧 / 奇幻',
            year: '2021',
            timeMinute: 128,
            score: 8.1,
            up: 100,
            down: 12,
            remarks: '2001年的某一天，刚刚考上大学的贾晓玲（贾玲 饰）经历了人生中的一次大起大落。一心想要成为母亲骄傲的她却因母亲突遭严重意外，而悲痛万分。在贾晓玲情绪崩溃的状态下，竟意外的回到了1981年，并与年轻的母亲李焕英（张小斐 饰）相遇，二人形影不离，宛如闺蜜。与此同时，也结识了一群天真善良的好朋友。晓玲以为来到了这片“广阔天地”，她可以凭借自己超前的思维，让母亲“大有作为”，但结果却让晓玲感到意外......'
          },
        ]
      }
    },
    created() {
    },
    methods: {
      search() {
        // 请求django
      },
      onUpClick(id) {
        // 请求django
      },
      onDownClick(id) {
        // 请求django
      },
      onImageClick(item) {
        this.$router.push({
          path: '/tb_movie_detail',
          query: item
        })
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
