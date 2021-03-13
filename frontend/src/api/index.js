import fetch from '@/common/axios'
// import fetch from '@/common/bmob'

export const login = data => fetch('/login', data, 'POST')
export const logout = () => fetch('/logout')

// 照片墙上传的时候
export const form = (url, formData) => fetch(url, formData, 'POST','multipart/form-data')

export const save = data => fetch(data.url, data, 'POST')
export const approve = data => fetch(data.url + '/approve', data, 'POST')
export const remove = data => fetch(data.url, data, 'DELETE')
export const removeById = (url, id) => fetch(url, {id: id}, 'DELETE')
export const getList = data => fetch(data.url, data)

export const search = (url, value) => fetch(url, {qs: value})
export const download = fileName => {
  location.href = process.env.BASE_URL + "sys/download/" + fileName
}
