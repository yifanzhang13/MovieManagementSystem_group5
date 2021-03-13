<template>
  <div>
    <el-table :data="page.list" row-key="id" @selection-change="handleSelectionChange"
              border stripe highlight-current-row>
      <!--批量操作-->
      <el-table-column v-if="btn.multipleDelete" type="selection" width="40"></el-table-column>
      <!--<el-table-column type="index" :min-width="30"></el-table-column>-->

      <!--扩展明细-->
      <el-table-column type="expand" v-if="tbl.expandCols">
        <template slot-scope="props">
          <el-form label-position="center" class="demo-table-expand" size="mini">
            <el-form-item v-for="(item,key) in tbl.expandCols" :key="key" :label="item.label">
              <span v-if="item.type == 'image'">
                <img :src="props.row[item.col]" style="width:220px;">
              </span>
              <span v-else>{{ props.row[item.col]}}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>

      <!--图标-->
      <el-table-column v-for="item in tbl.icons" :key="item.col" :prop="item.col" :label="item.label">
        <template slot-scope="scope">
          <i :class="scope.row.icon"> {{scope.row.name}}</i>
        </template>
      </el-table-column>

      <!--普通col-->
      <el-table-column :show-overflow-tooltip="true" v-for="(item,key) in tbl.cols" :key="key" :prop="item.col" :label="item.label"
                       :formatter="item.formatter" :min-width="item.width"></el-table-column>

      <!--图片-->
      <el-table-column v-for="item in tbl.imgCols" :key="item.col" :prop="item.col" :label="item.label">
        <template slot-scope="scope">
          <img v-if="scope.row[item.col] && scope.row[item.col].indexOf('http') == 0" :src="scope.row[item.col]" :style="item.style">
          <img v-else :src="scope.row[item.col]" :style="item.style">
        </template>
      </el-table-column>

      <!--tag-->
      <el-table-column v-for="item in tbl.tagCols" :key="item.col" :prop="item.col" :label="item.label" :min-width="item.width">
        <template slot-scope="scope">
          <el-tag size="mini" :type="scope.row.type?scope.row.type:item.type">{{scope.row[item.col]}}</el-tag>
        </template>
      </el-table-column>

      <!--个性col {col: 'focusBtnName', label: '关注/取关',type:'warning',icon:"el-icon-success"}-->
      <!--{col: 'disabled',displayLabel:'审核', label: '审核',type:'warning',icon:"el-icon-success"},-->
      <el-table-column v-for="item in tbl.btnCols" :key="item.col" :prop="item.col" :label="item.label" :min-width="item.width">
        <template slot-scope="scope">
          <el-button :disabled="scope.row[item.col]" size="mini" :type="item.type"
                     @click="handleCommand('btn_col', scope.$index, scope.row, item.col)"
                     :icon="item.icon">{{item.displayLabel ? item.displayLabel : scope.row[item.col]}}
          </el-button>
        </template>
      </el-table-column>

      <el-table-column v-if="btnCount > 0" label="操作" :width="btnColumnWidth + btnCount*80 + 25">
        <template slot-scope="scope">
          <el-button v-if="!detailBtnHide" size="mini" @click="handleCommand('detail', scope.$index, scope.row)" icon="el-icon-info">查看
          </el-button>
          <el-button v-if="!updateBtnHide" size="mini" @click="handleCommand('edit', scope.$index, scope.row)" icon="el-icon-edit-outline"
                     type="info" plain>编辑
          </el-button>
          <el-button v-if="!delBtnHide" size="mini" type="danger" @click="handleCommand('delete', scope.$index, scope.row)"
                     icon="el-icon-delete">删除
          </el-button>

          <template v-if="userDefined"> <!--数组-->
            <el-button v-for="ud in userDefined" :key="ud.text" size="mini"
                       @click="handleCommand('user_defined_'+ud.text, scope.$index, scope.row)"
                       :type="ud.type" :icon="ud.icon">
              {{ud.text}}
            </el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <div class="Pagination">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page.pageNum"
        :page-sizes="[10,20,30]"
        :page-size="page.pageSize"
        :page-count="page.navigatePages"
        layout="total, sizes, prev, pager, next, jumper"
        :total="page.total">
      </el-pagination>
    </div>

  </div>
</template>

<script>

  export default {
    name: "BaseTable",
    props: {
      tbl: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        page: {
          pageNum: 1,
          navigatePages: 0,
          pageSize: 10,
          total: 0,
        },
        addBtnHide: false,
        delBtnHide: false,
        updateBtnHide: false,
        detailBtnHide: false,
        btnCount: 4,
        userDefined: null,
        btnColumnWidth: 0,
        btn: this.tbl.btn,
      }
    },
    created() {
      this.load()
      if (this.tbl.btn) {
        if (this.tbl.btn.width) {
          this.btnColumnWidth = this.tbl.btn.width
        }

        if (this.tbl.btn.delete === 'hide') {
          this.delBtnHide = true
          this.btnCount -= 1
        }
        if (this.tbl.btn.update === 'hide') {
          this.updateBtnHide = true
          this.btnCount -= 1
        }
        if (this.tbl.btn.detail === 'hide') {
          this.detailBtnHide = true
          this.btnCount -= 1
        }
        if (this.tbl.btn.userDefined) {
          this.userDefined = this.tbl.btn.userDefined
        } else {
          this.btnCount -= 1
        }
      }
    },
    // watch:{
    //   '$route' (to,from){
    //     this.load()
    //   }
    // },
    methods: {
      async load() {
        const s = this.tbl.search
        const _data = await this.$findList({
          ...s,
          url: this.tbl.url,
          pageNum: this.page.pageNum,
          pageSize: this.page.pageSize
        })
        this.page = _data
        // this.$emit('tbl_success',_data.list)  可以emit出数据给parent
      },
      async handleCommand(command, index, row, col) {
        // this.selectTable = row
        this.$emit('tbl_edit_event', command, index, row, col)
      },
      handleSizeChange(val) {
        this.page.pageSize = val
        this.load()
      },
      handleCurrentChange(val) {
        this.page.pageNum = val;
        this.load()
      },
      handleSelectionChange(multipleSelection) {
        this.handleCommand('multipleSelection',0,multipleSelection)
      },

    }

  }
</script>

<style lang="less">
  .el-table__header{
    border-bottom: 1px solid #EBEEF5;
  }
  .el-table thead {
    color: #000000;
  }

  .demo-table-expand {
    font-size: 0;
    color:#000000;
  }

  .demo-table-expand label {
    width: 90px;
    font-weight: bold;
    color: #000000;
  }

  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
    background-color: rgba(0, 166, 90, 0.2);
  }
</style>
