const path = require('path')
const defaultSettings = require('./src/settings.js')
const name = defaultSettings.title + defaultSettings.version

function resolve(dir) {
  return path.join(__dirname, dir)
}

// https://cli.vuejs.org/zh/config/#vue-config-js
// 被 @vue/cli-service 自动加载
module.exports = {
  publicPath: "/",
  outputDir: 'dist',

  // 放置生成的静态资源 (js、css、img、fonts)  (相对于outputDir)
  assetsDir: 'static',

  // eslint on save
  lintOnSave: process.env.NODE_ENV === 'development',

  // 加速生产环境构建
  productionSourceMap: false,

  devServer: { // webpack-dev-server
    host: '0.0.0.0',
    port: process.env.port || 8888,
    proxy: { // 将任何未知请求 (没有匹配到静态文件的请求) 代理到http://localhost:8080
      [process.env.VUE_APP_BASE_API]: {
        target: process.env.BASE_URL,
        changeOrigin: true,
        pathRewrite: {
          ['^' + process.env.VUE_APP_BASE_API]: ''
        }
      }
    },
    disableHostCheck: true,
    open: false // open the browser
  },

  configureWebpack: {
    name: name,
    resolve: {
      alias: {
        '@': resolve('src'),
        // 'vue$': resolve('src/page/vue.esm.js'),
        '@css': resolve('src/assets/css')
      }
    },
  },

  chainWebpack(config) {
    config.plugins.delete('preload') // TODO: need test
    config.plugins.delete('prefetch') // TODO: need test

    // set svg-sprite-loader
    config.module
      .rule('svg')
      .exclude.add(resolve('src/assets/icon'))
      .end()
    config.module
      .rule('icon')
      .test(/\.svg$/)
      .include.add(resolve('src/assets/icon'))
      .end()
      .use('svg-sprite-loader')
      .loader('svg-sprite-loader')
      .options({
        symbolId: 'icon-[name]'
      })
      .end()

    // set preserveWhitespace
    config.module
      .rule('vue')
      .use('vue-loader')
      .loader('vue-loader')
      .tap(options => {
        options.compilerOptions.preserveWhitespace = true
        return options
      })
      .end()

    config
      .when(process.env.NODE_ENV !== 'development',
        config => {
          config
            .plugin('ScriptExtHtmlWebpackPlugin')
            .after('html')
            .use('script-ext-html-webpack-plugin', [{
            // `runtime` must same as runtimeChunk name. default is `runtime`
              inline: /runtime\..*\.js$/
            }])
            .end()
          config
            .optimization.splitChunks({
              chunks: 'all',
              cacheGroups: {
                libs: {
                  name: 'chunk-libs',
                  test: /[\\/]node_modules[\\/]/,
                  priority: 10,
                  chunks: 'initial' // only package third parties that are initially dependent
                },
                elementUI: {
                  name: 'chunk-elementUI', // split elementUI into a single package
                  priority: 20, // the weight needs to be larger than libs and app or it will be packaged into libs or app
                  test: /[\\/]node_modules[\\/]_?element-ui(.*)/ // in order to adapt to cnpm
                },
                commons: {
                  name: 'chunk-commons',
                  test: resolve('src/components'), // can customize your rules
                  minChunks: 3, //  minimum common number
                  priority: 5,
                  reuseExistingChunk: true
                }
              }
            })
          config.optimization.runtimeChunk('single'),
          {
             from: path.resolve(__dirname, './public/robots.txt'),// 防爬虫文件
             to: './',// 到根目录下
          }
        }
      )
  },

  pluginOptions: {
    'style-resources-loader': {
      preProcessor: 'less',
      patterns: [ // 填写公共文件路径
        resolve('src/assets/less/global.less'),
        resolve('src/assets/less/common.less'),

      ]
    }
  }
}
