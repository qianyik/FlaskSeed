(function() {
    'use strict';

    angular
        .module('fas')
        .controller('list_projects_controller', list_projects_controller);

        list_projects_controller.$inject = [
            '$location',
            '$filter',
            'Project',
            'NgTableParams'
        ];

        function list_projects_controller(
            $location, $filter, Project, NgTableParams) {

            var vm = this;
            angular.element(document).find('body').addClass('index');
            vm.search_term;
            vm.project_data = {};
            vm.projects = Project.query({embed: 'incident'}, load_data);
            vm.data_filter = data_filter;

            function data_filter() {
                vm.table_params.filter({$: vm.search_term});
            }

            function load_data() {
                var initial_params = {
                    count: 10,
                    sorting: {id: "asc"}
                };

                var initial_settings = {
                    dataset: vm.projects.data
                };
                
                vm.table_params =  new NgTableParams(initial_params, initial_settings);
            }
        }
})();
