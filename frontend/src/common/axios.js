import axios from 'axios'
import {Storage, NetworkPretty, toCamels,parseFileType} from '@/common/tool'

export default async(url = '', data = {}, type = 'GET', contentType) => {
  if (url === '') {
    console.error("fetch url is missing.")
    return {
      code: -1, message: "fetch url is missing."
    }
  }

  // useless attribute fliter
  for (const key in data) {
    if (data[key] == null || data[key] === undefined) delete data[key]
  }

  if (url.indexOf("http") === -1) {
    url = process.env.VUE_APP_BASE_API + '/' + url
  }

  axios.defaults.headers.common["Authorization"] = Storage.get("token")
  // axios.interceptors.request.use(config =>{})

  type = type.toUpperCase()
  let xhr
  if (type === 'GET') {
    xhr = await axios.get(url, {params: data})
  } else if (type === 'POST') {
    if (contentType) {
      xhr = await axios.post(url, data, {headers: {'Content-Type': 'multipart/form-data'}}) // 有file的时候
    } else {
      xhr = await axios.post(url, {...data}) // 默认Content-Type: application/json
    }
  } else if (type === 'DELETE') {
    xhr = await axios.delete(url, {data: data})
  }
  if (xhr.data.code === -1) {
    Storage.removeToken()
  } else {
    Storage.tokenFresh()
  }

  const request = type + " " + url, result = xhr.data
  NetworkPretty(request, data, result)

  const XHRData = xhr.data
  if (XHRData.data && Storage.get('OSCAR_VERSION') === 'koa') {
    XHRData.data = toCamels(XHRData.data)
  }

  return urlHandle(XHRData)
}

const urlHandle = data => {
  const imageProcess = url => {
    return url
    /* if (url.indexOf("http") === -1) {
      return process.env.VUE_APP_BASE_API + '/' + url
    } else {
      return url
    } */
  }
  const listProcess = list => { // 处理list数组中每一个对象的url
    return list.map(x => {
      if (x.imgUrl) {
        x.fmt = parseFileType(x.imgUrl)
        x.imgUrl = imageProcess(x.imgUrl)
      }
      if (x.headPhoto) {
        x.headPhoto = imageProcess(x.headPhoto)
      }
      if (x.replyList) { // 递归处理replyList回复列表
        x.replyList = listProcess(x.replyList)
      }
      return x
    })
  }

  if (Array.isArray(data.list)) { // page接口
    data.list = listProcess(data.list)
  } else if (Array.isArray(data.data)) {
    data.data = listProcess(data.data)
  }

  if (data.code !== 0) {
    return data
  }

  if (data.data != null && !Array.isArray(data.data)) {
    if (data.data.user && data.data.user.headPhoto) {
      data.data.user.headPhoto = imageProcess(data.data.user.headPhoto)
    }
  }
  return data
}

