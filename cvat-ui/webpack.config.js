// Copyright (C) 2019-2020 Intel Corporation
//
// SPDX-License-Identifier: MIT


/* eslint-disable */
const path = require('path');
const HtmlWebpackPlugin = require("html-webpack-plugin");
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin');
const Dotenv = require('dotenv-webpack');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
    target: 'web',
    mode: 'production',
    devtool: 'source-map',
    entry: './src/index.tsx',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'cvat-ui.min.js',
    },
    devServer: {
        contentBase: path.join(__dirname, 'dist'),
        compress: false,
        inline: true,
        port: 3000,
        historyApiFallback: true,
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.jsx', '.js', '.json'],
        plugins: [new TsconfigPathsPlugin({ configFile: "./tsconfig.json" })]
    },
    module: {
        rules: [{
            test: /\.(ts|tsx)$/,
            use: {
                loader: 'babel-loader',
                options: {
                    plugins: ['@babel/plugin-proposal-class-properties', ['import', {
                        'libraryName': 'antd',
                    }]],
                    presets: [
                        ['@babel/preset-env', {
                            targets: '> 2.5%', // https://github.com/browserslist/browserslist
                        }],
                        ['@babel/preset-react'],
                        ['@babel/typescript'],
                    ],
                    sourceType: 'unambiguous',
                },
            },
        }, {
            test: /\.(css|scss)$/,
            use: ['style-loader', {
                loader: 'css-loader',
                options: {
                    importLoaders: 2,
                },
            }, 'postcss-loader', 'sass-loader']
        }, {
            test: /\.svg$/,
            exclude: /node_modules/,
            use: ['babel-loader',
                {
                    loader: 'react-svg-loader',
                    query: {
                        svgo: {
                            plugins: [
                                { pretty: true, },
                                { cleanupIDs: false, }
                            ],
                        },
                    },
                }
            ]
        }, {
            test: /3rdparty\/.*\.worker\.js$/,
            use: {
                loader: 'worker-loader',
                options: {
                    publicPath: '/',
                    name: '3rdparty/[name].js',
                },
            },
        }, {
            test: /\.worker\.js$/,
            exclude: /3rdparty/,
            use: {
                loader: 'worker-loader',
                options: {
                    publicPath: '/',
                    name: '[name].js',
                },
            },
        },],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./src/index.html",
            inject: false,
        }),
        new Dotenv({
            systemvars: true,
        }),
        new CopyPlugin([
            {
                from: '../cvat-data/src/js/3rdparty/avc.wasm',
                to: '3rdparty/',
            },
        ]),
    ],
    node: { fs: 'empty' },
};
