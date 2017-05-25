window.angular.module('starter')
  .controller('DashCtrl', function () {
    'ngInject'
  })
  .controller('ChatsCtrl', function (Chats) {
    'ngInject'
    let vm = this // view model

    vm.chats = Chats.all()
    vm.remove = (chat) => {
      Chats.remove(chat)
    }
  })

  .controller('ChatDetailCtrl', function ($stateParams, Chats) {
    'ngInject'
    let vm = this

    vm.chat = Chats.get($stateParams.chatId)
  })

  .controller('AccountCtrl', function () {
    'ngInject'
    let vm = this

    vm.settings = {
      enableFriends: true
    }
  })
