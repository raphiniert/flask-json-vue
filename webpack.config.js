const miniCssExtractPlugin = require('mini-css-extract-plugin')
const path = require('path')
const { VueLoaderPlugin } = require('vue-loader')
const webpack = require('webpack');

module.exports = {
  mode: "development",
  entry: {
    'main': './flaskjsonvue/static/js/main.js',
    'list': './flaskjsonvue/static/vue/list.js',
  },
  output: {
    path: path.resolve(__dirname, 'flaskjsonvue/static/dist'),
    filename: (pathData) => {
        // console.log(pathData)
        return '[name].js'
      },
  },
  plugins: [
    new miniCssExtractPlugin({
      // filename: isProductionMode ? "[name].[contenthash].css" : "[name].css",
      filename: "[name].css",
    }),
    new VueLoaderPlugin(),
    new webpack.DefinePlugin({
        "__VUE_OPTIONS_API__": false,
        "__VUE_PROD_DEVTOOLS__": false,
      }),
  ],
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js"
    }
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.(scss)$/,
        use: [
          {
            // Extracts CSS for each JS file that includes CSS
            loader: miniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader'
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: () => [
                  require('autoprefixer')
                ]
              }
            }
          },
          {
            loader: 'sass-loader'
          }
        ]
      }
    ]
  }
}
