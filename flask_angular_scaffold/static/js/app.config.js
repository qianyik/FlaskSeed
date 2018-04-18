(function() {
    'use strict';

    angular
        .module('fas')
        .config(function($resourceProvider) {
            $resourceProvider.defaults.stripTrailingSlashes = false;
        })

        .config(function($routeProvider, $locationProvider) {
            $routeProvider

                .when('/', {
                    templateUrl: base_url + '/static/html/list_projects.html',
                    controller: 'list_projects_controller',
                    controllerAs: 'list'
                })
                .when('/add_project', {
                    templateUrl: base_url + '/static/html/add_project.html',
                    controller: 'add_project_controller',
                    controllerAs: 'add'
                })
                .when('/edit/:project_id', {
                    templateUrl: base_url + '/static/html/edit_project.html',
                    controller: 'edit_project_controller',
                    controllerAs: 'edit'
                })
                .when('/details/:project_id', {
                    templateUrl: base_url + '/static/html/project_details.html',
                    controller: 'project_details_controller',
                    controllerAs: 'details'
                })

            // use the HTML5 History API
            $locationProvider.html5Mode(true);
        });
})();
