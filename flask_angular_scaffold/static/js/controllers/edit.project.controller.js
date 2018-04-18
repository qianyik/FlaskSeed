(function() {
    'use strict';

    angular
        .module('fas')
        .controller('edit_project_controller', edit_project_controller);

        edit_project_controller.$inject = [
            'Project',
            '$routeParams',
            '$location',
        ];

        function edit_project_controller(
            Project,$routeParams,$location) {

            var vm = this;
            angular.element(document).find('body').addClass('index');
            vm.project_id = $routeParams.project_id;
            vm.save_project = save_project;

            load_project_data();
            function load_project_data() {
                Project.get({project_id: vm.project_id}, function(data) {
                    vm.project = data.data;
                }, function(data) {
                    // TODO: add in error page.
                    //$location.path('/error');
                });
            }

            function save_project() {
                Project.update({project_id: vm.project_id}, vm.project, function(data) {
                    $location.path('/details/' + vm.project_id);
                });
            }

        }
})();
