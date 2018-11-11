var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $http) {
    $scope.message = 'No message';
    $scope.x = 2;
    $scope.startS =  function( ) {
        
        $http({
            method : "GET",
            url : "http://127.0.0.1:5000/startconsumer"
        }).then(function mySuccess(response) {
            $scope.message = response.data.result;
            
        }, function myError(response) {
            this.message = response.statusText;

        });
    };
    $scope.stopS =  function() {
        $http({
            method : "GET",
            url : "http://127.0.0.1:5000/stopconsumer"
        }).then(function mySuccess(response) {
            $scope.message = response.data.result;
        }, function myError(response) {
            $scope.message = response.statusText;
        });
    };
    $scope.aveg =  function() {
        $http({
            method : "GET",
            url : "http://127.0.0.1:5000/data/"+ $scope.x
        }).then(function mySuccess(response) {
            $scope.message = 'The average of last ' + $scope.x + ' prices is: '+ response.data.result;
        }, function myError(response) {
            $scope.message = response.statusText;
        });
    };

});
