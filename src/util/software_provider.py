class SoftwareProvider:
    def __init__(self, global_state):
        self.global_state = global_state

    ### public methods ###

    def get_suggestions(self):
        suggestions = []
        software = self.global_state.get_config('additional_software')
        if software:
            for package in software:
                print(package)
                package_ok = ('package' in package and
                              'default' in package and
                              'name' in package and
                              'description' in package and
                              'icon_path' in package)
                if package_ok:
                    suggestions.append((package['package'],
                                        package['default'],
                                        package['name'],
                                        package['description'],
                                        package['icon_path']))
                else:
                    print('Package {} not correctly configured!'.format(package))
        return suggestions
