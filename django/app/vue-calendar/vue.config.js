if (process.env.NODE_ENV === 'production') {
    module.exports = {
        outputDir: '../static',
        assetsDir: '../static/app',
        indexPath: '../templates/app/index.html',
        publicPath: '/',
    }
}
