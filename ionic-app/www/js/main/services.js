window.angular.module('starter')
  .factory('API', ($http, $q, config) => {
    'ngInject'

    return {
      get: (url, headers) => {
        let deferred = $q.defer()
        let configObj = {
          headers: headers
        }

        $http.get(config.apiServer + url, configObj).then((data) => {
          deferred.resolve(data)
        }, (err) => {
          deferred.reject(err)
        })

        return deferred.promise
      },

      post: (url, data, headers) => {
        let deferred = $q.defer()
        let configObj = {
          headers: headers
        }

        $http.post(config.apiServer + url, data, configObj).then((result) => {
          deferred.resolve(result)
        }, (err) => {
          deferred.reject(err)
        })

        return deferred.promise
      },

      put: (url, data, headers) => {
        let deferred = $q.defer()
        let configObj = {
          headers: headers
        }

        $http.put(config.apiServer + url, data, configObj).then((result) => {
          deferred.resolve(result)
        }, (err) => {
          deferred.reject(err)
        })

        return deferred.promise
      },

      delete: (url, headers) => {
        let deferred = $q.defer()
        let configObj = {
          headers: headers
        }

        $http.delete(config.apiServer + url, configObj).then((result) => {
          deferred.resolve(result)
        }, (err) => {
          deferred.reject(err)
        })

        return deferred.promise
      }

    }
  })
