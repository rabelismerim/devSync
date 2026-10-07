import axios from 'axios'

const axiosInstance = axios.create({
    baseURL: '/devsync/api',
    withCredentials: true,
    xsrfHeaderName: 'X-CSRFToken',
    xsrfCookieName: 'csrftoken',
    timeout: 10000
})

export default axiosInstance
