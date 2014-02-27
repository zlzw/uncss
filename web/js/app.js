


function TodoCtrl($scope, $http) {
    // default config. should be overwritten in the next ajax request.
    $scope.config = {
        "api_url": "http://localhost"
    };

    $.getJSON( "js/config.json", function( data ) {
        $scope.config = data;
    });

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

        $http(
            {
                method: 'POST',
                url: $scope.config.api_url + '/process_html',
                headers: {"Content-Type": "text/plain"},
                data: $.param({'url': url})
            }
        ).success(function(data, status, headers, config) {
                $scope.is_processing_html = false;
                if(data.links.length == 0) {
                    $('#global_messages').append("<div class='alert alert-warning results'><a href='#' class='close' data-dismiss='alert'>&times;</a>No CSS links found in " + url + "</div>");
                }
                $scope.html_key = data.html_key;
                $scope.links = [];
                data.links.forEach(function(source) {
                    $scope.links.push({'source': source, 'status': 'processing'});
                });

                $scope.links.forEach(function(link){
                    $http(
                        {
                            method: 'POST',
                            url: $scope.config.api_url + '/clean_css',
                            headers: {"Content-Type": "text/plain"},
                            data: $.param({'html_key': $scope.html_key, 'css_source_url': link.source})
                        }
                    ).success(function(data, status, headers, config) {
                            link.status = 'success';
                            link.css_key = data;
                    }).error(function(data, status, headers, config) {
                            link.status = 'error';
                    });
                });
          }).error(function(data, status, headers, config) {
                $scope.is_processing_html = false;
                $('#global_messages').append("<div class='alert alert-danger results'><a href='#' class='close' data-dismiss='alert'>&times;</a>Error processing " + url + "</div>");
          });
    };
}
