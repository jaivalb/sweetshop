'use strict'

const path = require('path')
const express = require('express')
const { createProxyMiddleware } = require('http-proxy-middleware')

const app = express()

const PORT = process.env.PORT || 5173
const API_TARGET = process.env.API_TARGET || 'https://sweetshop-api.herokuapp.com'

// Proxy API to backend
app.use('/api', createProxyMiddleware({
  target: API_TARGET,
  changeOrigin: true,
  xfwd: true,
}))

// Serve static files from dist
const distDir = path.join(__dirname, 'dist')
app.use(express.static(distDir))

// Fallback to index.html for SPA routes
app.get('*', (req, res) => {
  res.sendFile(path.join(distDir, 'index.html'))
})

app.listen(PORT, () => {
  console.log(`Web listening on http://0.0.0.0:${PORT} (proxy -> ${API_TARGET})`)
})


