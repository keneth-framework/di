from keneth.di_contracts import ContainerContextInterface


class ContainerContext(ContainerContextInterface):
    def __init__(self):
        self.bindings = {}
        self.targets = []

    def add_binding(self, key, value):
        self.bindings[key] = value
        return self

    def get_binding(self, key):
        return self.bindings.get(key, None)

    def add_target(self, target):
        self.targets.append(target)
        return self

    def get_targets(self):
        return self.targets
