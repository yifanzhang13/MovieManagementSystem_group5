import {getList} from '@/api'

export const Storage = {
  set: (key, item) => {
    if (!key) return;
    if (typeof item !== 'string') {
      item = JSON.stringify(item);
    }
    localStorage.setItem(key, item);
  },
  get: key => {
    return key ? localStorage.getItem(key) : ''
  },
  remove: key => {
    if (!key) return;
    localStorage.removeItem(key);
  },
  setToken: (t) => {
    Storage.set('token', t.token)
    Storage.set('timeout', t.timeout)
    Storage.set('expired', new Date().getTime() + t.timeout * 60000)
  },
  removeToken: () => {
    Storage.remove('token')
    Storage.remove('timeout')
    Storage.remove('expired')
  },
  tokenFresh: () => {
    const timeout = Storage.get("timeout")
    Storage.set('expired', new Date().getTime() + timeout * 60000)
  },
  tokenValid: () => {
    return Storage.get('token') && Storage.get('expired') && new Date().getTime() < Storage.get('expired')
  },

  // business
  getUserInfo() {
    const userInfo = Storage.get("user_info")
    return userInfo ? JSON.parse(userInfo) : {}
  },
}

/**
 * 初始化后端的版本类型 koa|java|express
 */
export const backendVersion = async() => {
}

/**
 * 网络请求美化
 */
export const NetworkPretty = (request, inParam, outParam) => {
  // TODO set here
}

const toCamel2 = obj => {
  const camelRow = {}
  for (const key in obj) {
    const camelKey = key.replace(/([^_])(?:_+([^_]))/g, function($0, $1, $2) { // parent_id 转 parentId
      return $1 + $2.toUpperCase()
    })
    camelRow[camelKey] = obj[key]
  }
  if (camelRow._id) { camelRow.id = camelRow._id }
  return camelRow
}
const toCamel = obj => {
  const camelRow = {}
  for (const key in obj) {
    const camelKey = key.replace(/([^_])(?:_+([^_]))/g, function($0, $1, $2) { // parent_id 转 parentId
      return $1 + $2.toUpperCase()
    })
    const value = obj[key]
    if (typeof value === 'object') {
      camelRow[camelKey] = toCamel2(value)
    } else {
      camelRow[camelKey] = value
    }
  }
  if (camelRow._id) { camelRow.id = camelRow._id }
  return camelRow
}
export const toCamels = obj => { // 转驼峰
  if (!obj) return obj

  if (Array.isArray(obj)) {
    return obj.map(x => toCamel(x))
  } else {
    return toCamel(obj)
  }
}

/**
 * 根据文件url获取文件类型  image|video|audio|file
 */
export const parseFileType = fileUrl => {
  if (!fileUrl) return ''

  const split = fileUrl.split("\.")
  let postfix = split[split.length - 1]
  postfix = postfix.toLowerCase()
  const videoFmt = ['mp4', 'ogg', 'webm']
  const audioFmt = ['mp3', 'wav', 'ogg']
  const imageFmt = ['png', 'bmp', 'gif', 'jpeg', 'webp', 'jpg']
  let fmt = 'file'
  if (videoFmt.includes(postfix)) {
    fmt = 'video'
  } else if (audioFmt.includes(postfix)) {
    fmt = 'audio'
  } else if (imageFmt.includes(postfix)) {
    fmt = 'image'
  }
  return fmt
}

export function formatTime(datetime) {
  datetime = +datetime * 1000
  const d = new Date(datetime)
  const now = Date.now()

  const diff = (now - d) / 1000

  if (diff < 30) {
    return '刚刚'
  } else if (diff < 3600) { // less 1 hour
    return Math.ceil(diff / 60) + '分钟前'
  } else if (diff < 3600 * 24) {
    return Math.ceil(diff / 3600) + '小时前'
  } else if (diff < 3600 * 24 * 2) {
    return '1天前'
  } else {
    return d.getMonth() + 1 + '月' + d.getDate() + '日' + d.getHours() + '时' + d.getMinutes() + '分'
  }
}

/**
 * 将对象转成query string
 * @param param
 * @returns {string}
 */
export function getQS(param) {
  if (!param) return ''

  const qs = []
  for (const key in param) {
    qs.push(`${key}=${param[key]}`)
  }
  return qs.join('&')
}

export function exportExcel(param) {
  const url = param.url
  delete param.url
  location.href = process.env.BASE_URL + url + '?' + getQS(param)
}
