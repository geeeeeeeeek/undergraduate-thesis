#!/usr/bin/env node

/**
 * After prepare, files are copied to the platforms/ios and platforms/android folders.
 * Lets clean up some of those files that arent needed with this hook.
 */
var fs = require('fs')
var path = require('path')

var deleteFolderRecursive = function (removePath) {
  if (fs.existsSync(removePath)) {
    fs.readdirSync(removePath).forEach(function (file, index) {
      var curPath = path.join(removePath, file)
      if (fs.lstatSync(curPath).isDirectory()) { // recurse
        deleteFolderRecursive(curPath)
      } else { // delete file
        fs.unlinkSync(curPath)
      }
    })
    fs.rmdirSync(removePath)
  }
}

try {
  var packageJSON = require('../../package.json');
  (packageJSON.cleanFromPlatforms || [])
      .forEach(function (toRemove) {
        var iosPlatformsDir = path.resolve(__dirname, '../../platforms/ios/www/' + toRemove)
        var androidPlatformsDir = path.resolve(__dirname, '../../platforms/android/assets/www/' + toRemove)

        deleteFolderRecursive(iosPlatformsDir)
        deleteFolderRecursive(androidPlatformsDir)
      })
} catch (ex) {
  console.log('\nThere was an error fetching your package.json file.')
  console.log('\nPlease ensure a valid package.json is in the root of this project\n')
}
