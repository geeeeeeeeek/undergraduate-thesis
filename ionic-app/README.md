# IonicKit from eKreative

[![JavaScript Style Guide](https://img.shields.io/badge/code_style-standard-brightgreen.svg)](https://standardjs.com)

## Get started

Setup (required Node 4.x)

    cp www/js/main/config.<dev or release>.js.dist www/js/main/config.js

    yarn

Run a dev server

    yarn serve

Run on a device

    ionic run <platform>

Create a build

    ionic build <platform>

Emulating in real time

    ionic emulate <platform> -l -c -s

Tests

    yarn test

## This ionicKit includes:

1. Added and installed [ngCordova](http://ngcordova.com/) - a collection of AngularJS extensions on top of the Cordova API;

2. API service for different requests (<access origin="*"/> <allow-intent href="*"/> in config.xml and <meta http-equiv="Content-Security-Policy" ...> in index.html) - more info here [cordova-plugin-whitelist](https://github.com/apache/cordova-plugin-whitelist);

3. Gulp tasks with ionic’s commands: serve, build, run:

  * sourcemaps for scss and js files;

  * js-files manipulations: sourcemaps, babel, ngAnnotate, concat, uglify -> so now we have only 1 js-file in index.html.
