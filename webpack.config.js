var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractText = require('extract-text-webpack-plugin');

module.exports = {
  mode: 'development',
  entry:  path.join(__dirname, 'assets/src/js/index'),
  output: {
    path: path.join(__dirname, 'assets/dist'),
    filename: '[name]-[hash].js'
  },
  devtool: "#eval-source-map",
  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: 'webpack-stats.json'
    }),
    new ExtractText({
      filename: '[name]-[hash].css'
    }),
  ],
  module: {
      rules: [
        {
          test: /\.jsx?$/,
          loader: 'babel-loader',
          exclude: /node_modules/,
        },
          {
          test: /\.css$/,
          loader: ['style-loader', 'css-loader'],
        },
        {
          test: /\.scss$/,
          use: ExtractText.extract({
            fallback: 'style-loader',
            use: ['css-loader',{
              loader: 'postcss-loader',
            options: {
              sourceMap: true,
              ident: 'postcss',
              plugins: () => [
                /* eslint-disable global-require */
                require('postcss-pseudo-class-any-link'),
                require('postcss-initial')(),
                require('postcss-prepend-selector')({ selector: '#react-app ' }),
                /* eslint-enable global-require */
              ],
            },
          },
              'sass-loader']
          })
        },
      ],
    },
}
