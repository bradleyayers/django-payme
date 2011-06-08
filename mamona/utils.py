from . import settings


def import_backend_modules(submodule=''):
    modules = {}
    for backend_name in settings.ACTIVE_BACKENDS:
        fqmn = 'mamona.backends.%s' % backend_name
        if submodule:
            fqmn = '%s.%s' % (fqmn, submodule)
        mamona = __import__(fqmn)
        if submodule:
            module = getattr(getattr(mamona.backends, backend_name), submodule)
        else:
            module = getattr(mamona.backends, backend_name)
        modules[backend_name] = module
    return modules


def get_backend_choices():
    choices = []
    backends = import_backend_modules()
    for name, module in backends.items():
        choices.append((name, module.BACKEND_NAME))
    return choices


def get_backend_settings(backend):
    return settings.BACKENDS_SETTINGS.get(backend, {})
