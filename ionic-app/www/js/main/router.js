window.angular.module('starter')
  .config(($stateProvider, $urlRouterProvider) => {
    'ngInject'

    // Ionic uses AngularUI Router which uses the concept of states
    // Learn more here: https://github.com/angular-ui/ui-router
    // Set up the various states which the app can be in.
    // Each state's controller can be found in controllers.js
    $stateProvider

    // setup an abstract state for the tabs directive
      .state('tab', {
        url: '/tab',
        abstract: true,
        templateUrl: 'templates/tabs/tabs.html'
      })

      // Each tab has its own nav history stack:

      .state('tab.dash', {
        url: '/dash',
        views: {
          'tab-dash': {
            templateUrl: 'templates/tabs/tab-dash.html',
            controller: 'DashCtrl as Dash'
          }
        }
      })

      .state('tab.chats', {
        url: '/chats',
        views: {
          'tab-chats': {
            templateUrl: 'templates/tabs/tab-chats.html',
            controller: 'ChatsCtrl as Chats'
          }
        }
      })
      .state('tab.chat-detail', {
        url: '/chats/:chatId',
        views: {
          'tab-chats': {
            templateUrl: 'templates/tabs/chat-detail.html',
            controller: 'ChatDetailCtrl as ChatDetail'
          }
        }
      })

      .state('tab.account', {
        url: '/account',
        views: {
          'tab-account': {
            templateUrl: 'templates/tabs/tab-account.html',
            controller: 'AccountCtrl as Account'
          }
        }
      })

    // if none of the above states are matched, use this as the fallback
    $urlRouterProvider.otherwise('/tab/dash')
    // $urlRouterProvider.otherwise(function ($injector) {
    //  return $injector.get('serviceName').methodOrVariable() ? '/tab/dash' : '/tab/account';
    // this will not work right now, this is an example
    // });
  })
