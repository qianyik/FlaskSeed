(function() {
    'use strict';

    angular
        .module('fas')
        .controller('add_project_controller', add_project_controller);

        add_project_controller.$inject = ['$location', 'Project'];

        function add_project_controller($location, Project) {
            var vm = this;
            angular.element(document).find('body').addClass('index');
            vm.project_data = {};
            // TODO: fix date UTC issue.
            vm.title = '';
            vm.short_syn= '';
            vm.long_syn = '';
            vm.website = '';
            vm.organization = '';
            vm.loc = '';
            vm.create_project = create_project;

            function create_project() {
                vm.project_data = {
                    title: vm.title,
                    short_synopsis: vm.short_syn,
                    long_synopsis: vm.long_syn,
                    website: vm.website,
                    organization: vm.organization,
                    location: vm.loc
                }

                Project.save(vm.project_data, function(data) {
                    $location.path('/details/'+data.data.id);
                });
            }

        }
})();
