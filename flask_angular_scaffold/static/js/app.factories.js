(function() {
    'use strict';

    angular
        .module('fas')
        .factory('Project', projects_factory);

    function resource_fact($resource, url) {
        return $resource(url, null,
            {
                'query': {method: "GET", isArray: false},
                'update': {method: "PUT"},
                'delete': {method: "DELETE"}
            }
        );
    }

    function projects_factory($resource) {
        return resource_fact($resource, base_url+'api/project/:project_id')
    }

})();
