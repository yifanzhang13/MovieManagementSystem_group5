<template>
  <div class="page">
    <el-row :gutter="20">
      <el-col v-for="(item, index) in dataList" :key="item.id" style="margin-top:25px;" :span="6">
        <el-card shadow="hover" >
          <div @click="handleCommand('edit',item)">
            <img :src="$baseUrl + '/' + item.imgUrl" class="image"/>
          </div>
          <div @click="handleCommand('edit',item)">
            <div class="text-word ellipsis">
              <span>{{item.no}} {{item.name}} {{item.type}}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col key="add" style="margin-top:25px;" :span="6">
        <el-card shadow="hover">
          <div>
            <i @click="handleCommand('add')" class="el-icon-circle-plus-outline image" style="height: 60px;margin-top: 50px;"></i>
          </div>
          <div>
            <div class="text-word ellipsis">
              <span>{{tbl.label}}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

  </div>

</template>

<script>
  import {oscarMixin} from '@/config/mixins'

  export default {
    name: 'VueProductCard',
    mixins: [oscarMixin],
    props: ['tbl'],
    data() {
      return {
        bannerList: [
          "/static/img/banner1.jpg",
          "/static/img/banner2.jpg",
        ],
        dataList: [],
        allDataList: [],
        searchText: null,
      }
    },
    watch: {
      tbl: (newValue, oldValue) => {
        this.load()
      }
    },
    created() {
      this.load()
    },
    methods: {
      async load(newParam) {
        const param = newParam || this.tbl
        const res = await this.$findList({url: param.url, ...param.search})
        if (res.code === 0) {
          this.dataList = res.data
          this.allDataList = res.data
        }
      },
      search() {
        const searchText = this.searchText
        this.dataList = this.allDataList.filter(x => {
          return x.name.indexOf(searchText) !== -1
        })
      },
      handleCommand(command, item) {
        this.$emit('tbl_edit_event', command,0, item)
      },
      gotoVideoPage(item) {
        this.$router.push({
          path: '/f/detail',
          query: item
        })
      },
    }
  }
</script>

<style scoped lang="less">
  .image {
    width: 260px;
    height: 200px;
  }

  .page /deep/ .el-card__body {
    text-align: center;
  }

  .el-carousel__container img {
    height: 100%;
  }
</style>
