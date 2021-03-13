<template>
  <div style="height: 100%;padding: 10px 200px;">
    <el-card class="filter-container" shadow="never">
      <el-row :gutter="30">
        <el-col :span="18">
          <el-row>
            <div class="summary">
              <div class="title">Movie Star Rating</div>
              <div v-for="item in movieList" :key="item.remarks" class="comment">
                <el-row :gutter="30">
                  <el-col :span="4">
                    <img :src="item.imgUrl" class="picture">
                  </el-col>
                  <el-col :span="20">
                    <div>{{item.name}}</div>
                    <div>{{item.year}} / {{item.director}} / {{item.actor}} / {{item.timeMinute}}分钟 </div>
                    <div>Score <span class="red">{{item.score}}</span></div>
                  </el-col>
                </el-row>
              </div>
            </div>
          </el-row>
        </el-col>
        <el-col :span="6">
          <div>
            <h2>分类排行榜</h2>
            <div class="types">
              <span v-for="item in categoryList" :key="item">
                <a href="#">{{item}}</a>
              </span>
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
        movieList: [],
        categoryList: ['喜剧','动作','爱情','科幻','动画','悬疑','恐怖','历史','战争','犯罪','西部','奇幻','冒险','灾难']
      }
    },
    created() {
      this.getMovieList()
    },
    methods: {
      getMovieList() {
        // 查询django
        this.movieList = [
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
      },
    }
  }
</script>

<style lang="less" scoped>
  .picture{
    width:75px;
  }
  .summary{
    margin-top: 20px;
    font-size: 14px;
    color: #111;
    .title{
      font-size: 26px;
      margin-bottom: 10px;
    }

    .comment{
      border-bottom: solid 1px #ddd;
      line-height: 2;
    }
  }

  .types span{
    display: inline-block;
    margin: 5px 10px 5px 0;
    min-width: 36px;
    font-size: 13px;
  }
</style>
