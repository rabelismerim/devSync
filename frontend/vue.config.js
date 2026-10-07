const path = require('path')
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({

  lintOnSave: false,

  configureWebpack: {
    devtool: 'source-map'
  },

  devServer: {
    allowedHosts: "all",
    hot: true,
    port: 8080,
    historyApiFallback: true
  },

  publicPath: '/devsync/static/frontend/',
  outputDir: path.resolve(__dirname, '../backend/static/frontend/'),
  filenameHashing: false,
  runtimeCompiler: true,

  transpileDependencies: [
    'vuetify'
  ]

})
