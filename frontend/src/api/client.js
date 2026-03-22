import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export const discoverApis = (payload) => api.post('/api/discover', payload)
export const getResults = () => api.get('/api/results')
export const getAlerts = () => api.get('/api/alerts')
export const runFix = () => api.post('/api/fix')
export const getReport = () => api.get('/api/report')
