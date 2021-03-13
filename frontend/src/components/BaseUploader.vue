<template>
  <div class="vue-uploader">
    <el-upload v-if="facade == 'picture-card'"
               ref="pictureRef"
               action=""
               list-type="picture-card"
               :auto-upload="false"
               :http-request="uploadFile">
      <i class="el-icon-plus"></i>
    </el-upload>

    <el-upload v-else
               class="avatar-uploader"
               :action="action"
               :show-file-list="false"
               :on-success="onUploadSuccess"
               :before-upload="onBeforeUpload">
      <img v-if="fileType == 'image'" :src="previewUrl" class="avatar">
      <video v-else-if="fileType == 'video'" id="myvideo" :src="previewUrl"
             controls="controls" height="200" width="350">
        your browser does not support the video, please use chrome
      </video>
      <i v-else-if="fileType == 'file'" class="el-icon-tickets avatar-uploader-icon"></i>
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
    </el-upload>

  </div>
</template>

<script>

  export default {
    name: "BaseUploader",
    props: {
      imageUrl: {
        type: String,
        default: ''
      },
      facade: {
        type: String,
        default: 'normal'
      }
    },
    data() {
      return {
        action: this.$baseUrl + 'sys/upload',
        fileType: null,
        previewUrl: null,
        defaultUrl: null,
        pictureList: [], // 图片暂存
      }
    },
    watch: {
      imageUrl(newValue, oldValue) {
        this.preview(newValue)
      }
    },
    created() {
      this.preview(this.imageUrl)
    },

    methods: {
      preview(url) {
        this.previewUrl = url
        this.checkFmt(url)
      },
      checkFmt(url) {
        const picture = /\.(png|jpg|gif|jpeg|bmp)$/i
        const video = /\.(mp4|avi|rmvb|flv)$/i
        if (picture.test(url)) {
          this.fileType = 'image'
        } else if (video.test(url)) {
          this.fileType = 'video'
        } else {
          this.fileType = 'file'
        }
      },
      reset() {
        this.fileType = null
      },
      onUploadSuccess(res) {
        if (res.code === 0) {
          if (this.fileType === 'image') {
            // this.defaultUrl = URL.createObjectURL(file.raw)
          }
          console.log(res.data)
          this.preview(res.data)
          this.$emit('vue-upload', res.data)
        } else {
          this.$message.error('上传失败！')
        }
      },
      onBeforeUpload(file) {
        this.checkFmt(file.name)
        const fileSize = file.size / 1024 / 1024 < 30
        if (!fileSize) {
          this.$message.error('上传大小不能超过30MB!')
        }
        return true
      },

      // picture card
      uploadFile(file) {
        this.pictureList.push(file.file)
      },
      // data为表单的其他额外参数 {name:'123'}
      // let formData = this.$refs.img_ref.wrapFormData(this.formData)
      // let res = await form('/upload/multiple',formData)
      wrapFormData(formData) {
        this.$refs.pictureRef.submit() // 触发uploadFile callback 会调用uploadFile多次

        const form = new FormData()
        for (const key in formData) {
          form.append(key, formData[key])
        }

        this.pictureList.forEach(file => {
          form.append('file', file) // 放最后
        })

        return form
      },
    }
  }
</script>

<style lang="less">
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #20a0ff;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 120px;
    height: 120px;
    line-height: 120px;
    text-align: center;
  }

  .avatar {
    width: 120px;
    height: 120px;
    display: block;
  }
</style>
