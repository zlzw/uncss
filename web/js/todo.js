function TodoCtrl($scope, $http) {
    $scope.links = [];
    $scope.html_key = null;
    $scope.is_processing_html = false;
    $scope.clean = function(url) {
        $scope.links = [];
        $scope.html_key = null;
        if(!url) {
             $('#global_messages').append("<div class='alert alert-danger results'><a href='#' class='close' data-dismiss='alert'>&times;</a>Please, enter an URL.</div>");
            return;
        }
        $scope.is_processing_html = true;
        url = encodeURIComponent(url);
        $http({method: 'GET', url: 'http://localhost:8097/process_html/' + url}).
          success(function(data, status, headers, config) {
                $scope.is_processing_html = false;
                if(data.links.length == 0) {
                    $('#global_messages').append("<div class='alert alert-warning results'><a href='#' class='close' data-dismiss='alert'>&times;</a>No CSS links found in " + url + "</div>");
                }
                $scope.html_key = data.html_key;
                $scope.links = [];
                data.links.forEach(function(source) {
                    $scope.links.push({'source': source, 'status': 'processing'});
                });

                var css_url;
                $scope.links.forEach(function(link){
                    css_url = encodeURIComponent(link.source);
                    $http({method: 'GET', url: 'http://localhost:8097/clean_css/' + $scope.html_key + '/' + css_url}).
                        success(function(data, status, headers, config) {
                            link.status = 'success';
                            link.css_key = data;
                        }).
                        error(function(data, status, headers, config) {
                            link.status = 'error';
                        });
                });
          }).
          error(function(data, status, headers, config) {
                $scope.is_processing_html = false;
                $('#global_messages').append("<div class='alert alert-danger results'><a href='#' class='close' data-dismiss='alert'>&times;</a>Error processing " + url + "</div>");
          });
    };
}