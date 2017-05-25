window.angular.module('starter')
  .factory('Chats', () => {
    'ngInject'
    // Might use a resource here that returns a JSON array
    // Some fake testing data
    let chats = [{
      id: 0,
      name: 'Max Lynx',
      lastText: 'Hey, it\'s me',
      face: 'https://avatars3.githubusercontent.com/u/11214?v=3&s=460'
    }, {
      id: 1,
      name: 'Adam Bradleyson',
      lastText: 'I should buy a boat',
      face: 'https://pbs.twimg.com/profile_images/479090794058379264/84TKj_qa.jpeg'
    }, {
      id: 2,
      name: 'Perry Governor',
      lastText: 'Look at my mukluks!',
      face: 'https://pbs.twimg.com/profile_images/598205061232103424/3j5HUXMY.png'
    }]

    return {
      all: () => {
        return chats
      },
      remove: (chat) => {
        chats.splice(chats.indexOf(chat), 1)
      },
      get: (chatId) => {
        for (let i = 0; i < chats.length; i++) {
          if (chats[i].id === parseInt(chatId)) {
            return chats[i]
          }
        }
        return null
      }
    }
  })
