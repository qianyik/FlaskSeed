(function() {
    'use strict';

    angular
        .module('fas')
        .controller('project_details_controller', project_details_controller);

        project_details_controller.$inject = [
            'Project',
            '$routeParams',
            '$location'
        ];

        function project_details_controller(
            Project,$routeParams,$location) {

            var vm = this;
            angular.element(document).find('body').addClass('index');
            vm.project_id = $routeParams.project_id;
            vm.project = {};
            vm.delete_project = delete_project;

            load_project_data();

            function load_project_data() {
                Project.get({project_id: vm.project_id}, function(data) {
                    vm.project = data.data;
                }, function(data) {
                    // TODO: add in error page.
                    //$location.path('/error');
                });
            }

            function delete_project() {
                Project.delete({project_id: vm.project_id}, function(data) {
                    $location.path('/');
                }, function(data) {
                    // TODO: add in error page.
                    //$location.path('/error');
                });
            }

        }

})();
