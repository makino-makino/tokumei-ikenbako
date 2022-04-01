module.exports = {
  configureWebpack: {
    module: {
      rules: [
        {
          type: 'javascript/auto',
          test: /\.wasm$/,
          loaders: ["wasm-loader"]
        }
      ]
    }
  },

  css: {
    loaderOptions: {
      scss: {
        prependData: '@import "./src/assets/main.scss";',
      },
    },
  },

  pluginOptions: {
    autoRouting: {
      chunkNamePrefix: 'page-'
    }
  },

  devServer: {
    disableHostCheck: true,
    watchOptions: {
      poll: true
    }
  }
}
