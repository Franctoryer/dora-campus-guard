// src/utils/axios.ts
import axios from 'axios'
import type { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8080/rest',
  timeout: 10000, // 10 秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 例如：从本地获取 token 并附加到请求头
    // const token = localStorage.getItem('token')
    // if (token && config.headers) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data
    // 这里可以根据实际业务自定义返回值判断
    return res
  },
  (error) => {
    // 网络或服务器错误
    console.error(error?.response?.data?.message || '网络错误')
    return Promise.reject(error)
  },
)

export default service
