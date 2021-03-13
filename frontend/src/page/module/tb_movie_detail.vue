<template>
  <div style="height: 100%;padding: 10px 100px;">
    <el-card class="filter-container" shadow="never">
      <el-row :gutter="30">
        <el-col :span="18">
          <el-row>
            <el-col :span="8"><img :src="movie.imgUrl" class="picture"></el-col>
            <el-col :span="16" class="info">
              <div class="header">{{movie.name}}({{movie.year}})</div>
              <div>导演: {{movie.director}}</div>
              <div>主演: {{movie.actor}}</div>
              <div>类型: {{movie.type}}</div>
              <div>片长: {{movie.timeMinute}}分钟</div>
            </el-col>
          </el-row>
          <el-row>
            <div class="summary">
              <div class="title">{{movie.name}}的剧情简介 · · · · · ·</div>
              <div>{{movie.remarks}}</div>
            </div>
          </el-row>
          <el-row>
            <div class="summary">
              <div class="title">{{movie.name}}的评论 · · · · · ·</div>
              <div v-for="item in commentList" :key="item.remarks" class="comment">{{item.remarks}}</div>
            </div>
          </el-row>
        </el-col>
        <el-col :span="6">
          <div class="rate">
            <div class="flex">
              <el-slider style="width: 200px;margin-right: 10px;" v-model="score" :max="10"></el-slider>
              <span style="line-height: 38px;">{{score}}</span>
            </div>
            <el-button type="success" size="mini" @click="onConfirm">Confirm</el-button>
            <div class="score">
              {{movie.score}}
            </div>
          </div>
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
        score: 5,
        movie: {},
        commentList: []
      }
    },
    created() {
      this.movie = this.$route.query
      this.getCommentList()
    },
    methods: {
      getCommentList() {
        // 查询django
        this.commentList = [
          {remarks: '你以为你已经很爱很爱妈妈了，但妈妈远比你想象中更爱更爱更爱你。'},
          {remarks: '沈腾的戏份约等于欢乐颂男主，其他不评论'},
          {remarks: '贾玲水平有限，奈何感情无比真挚。虽然结尾让我哭的稀里哗啦，但也没能改变前半段就是个低配版夏洛特烦恼的状况。'},
        ]
      },
      onConfirm() {
        // 请求django
      }
    }
  }
</script>

<style lang="less" scoped>
  .picture{
    width:200px;
  }
  .info{
    font-size: 14px;
    color: #666666;
    line-height: 2;
    .header{
      font-size: 26px;
      color: #494949;
    }
  }
  .summary{
    margin-top: 20px;
    font-size: 14px;
    line-height: 2;
    color: #111;
    .title{
      font-size: 18px;
      margin-bottom: 10px;
    }

    .comment{
      border-bottom: solid 1px #ddd;
      line-height: 4;
    }
  }

  .rate {
    border-left: solid 1px #ddd;
    height: 200px;
    padding: 10px 30px;
    .score{
      color: #cd2929;
      text-align: center;
      font-size: 40px;
      margin-top: 20px;
    }
  }
</style>
