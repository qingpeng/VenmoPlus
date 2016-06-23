var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services"]);

var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Search', function($resource) {
    return $resource('http://52.40.84.152:5000/api/v1/search', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('User', function($resource) {
    return $resource('http://52.40.84.152:5000/api/v1/user', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Friend', function($resource) {
    return $resource('http://52.40.84.152:5000/api/v1/friend', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Message', function($resource) {
    return $resource('http://52.40.84.152:5000/api/v1/message', {q: '@q', m: '@m'}, {
        query: { method: 'GET', isArray: true}
    });
});





myApp.config(function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'pages/main.html',
        controller: 'mainController'
    })
    .when('/user', {
        templateUrl: 'pages/user.html',
        controller: 'userController'
    })
    .when('/friend', {
        templateUrl: 'pages/friend.html',
        controller: 'friendController'
    })
    .when('/message', {
        templateUrl: 'pages/message.html',
        controller: 'messageController'
    })
}
);


myApp.controller(
    'mainController',
    function ($scope, Search) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 1) {
                $scope.results = Search.query({q: q});    
            }
        };
    }
);

myApp.controller(
    'userController',
    function ($scope, User) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 1) {
                $scope.results = User.query({q: q});    
            }
        };
    }
);

myApp.controller(
    'friendController',
    function ($scope, Friend) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 4) {
                $scope.results = Friend.query({q: q});    
            }
        };
    }
);

myApp.controller(
    'messageController',
    function ($scope, Message) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 4) {
                $scope.results = Message.query({q: q});    
            }
        };
    }
);


