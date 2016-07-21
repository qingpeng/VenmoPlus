var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services"]);
var url = 'http://52.26.150.191:8080'
var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Search', function($resource) {
    return $resource(url+'/api/v1/search', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('User', function($resource) {
    return $resource(url+'/api/v1/user', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Friend', function($resource) {
    return $resource(url+'/api/v1/friend', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Message', function($resource) {
    return $resource(url+'/api/v1/message', {q: '@q', m: '@m'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Name', function($resource) {
    return $resource(url+'/api/v1/name', {q: '@q'}, {
        query: { method: 'GET', isArray: false}
    });
})
.factory('List', function($resource) {
    return $resource(url+'/api/v1/list', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})

//.factory('UserDetail', function($resource) {
//    return $resource("





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
    .when('/user/:user_id', {
        templateUrl: 'pages/user.html',
        controller: 'userDetailsController'
    })
});


myApp.controller(
    'userController',
    function ($scope, Search) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 3) {
                $scope.results = Search.query({q: q});    
            }
        };
    }
);

myApp.controller(
    'mainController',
    function ($scope, User) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 3) {
                $scope.results = User.query({q: q});    
                if ($scope.results.length > 0){
                    $scope.list = ["1"]
                }
                else {
                    $scope.list = []
                }
            }
        };
        
    }
);

myApp.controller(
    'friendController',
    function ($scope, Friend) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 3) {
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

myApp.controller(
    'userDetailsController', ['$scope', 'Search', 'Friend','Message','Name','List','$routeParams',
    function ($scope, Search, Friend, Message,Name, List,$routeParams) {
            $scope.results = Search.query({q: $routeParams.user_id});    
            //$scope.user_id = $routeParams.user_id;
            $scope.friends = Friend.query({q: $routeParams.user_id});
            $scope.name = Name.query({q: $routeParams.user_id});
            $scope.friend_list = List.query({q: $routeParams.user_id});
            //var date = new Date(results['time'].concat(' UTC'));
            //results['time'] = date.toString();
            //$scope.results = results;
            $scope.search = function() {
                q = $scope.searchString;
                if (q.length > 1) {
                    $scope.search_results = Message.query({q: $routeParams.user_id,m:q});    
                }
        };
            
    }
]);


