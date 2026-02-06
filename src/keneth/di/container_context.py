from keneth.di_contracts import ContainerContextInterface, ServiceInterface


class ContainerContext(ContainerContextInterface):
    """Concrete implementation of the container context."""

    def __init__(self) -> None:
        """Initialize the container context."""
        self.bindings = {}
        self.targets: list[ServiceInterface] = []
        self.instances: list[object] = []

    def add_binding(self, key: str, value: object) -> ContainerContextInterface:
        self.bindings[key] = value
        return self

    def get_binding(self, key: str) -> object | None:
        return self.bindings.get(key)

    def add_target(self, target: type[ServiceInterface]) -> ContainerContextInterface:
        self.targets.append(target)
        return self

    def get_targets(self) -> list[type[ServiceInterface]]:
        return self.targets

    def add_instance(self, target: object) -> ContainerContextInterface:
        self.instances.append(target)
        return self

    def get_instance_from_type(self, target_type: type) -> object | None:
        for instance in self.instances:
            if isinstance(instance, target_type):
                return instance
        return None

    def clear_instances(self) -> None:
        self.instances.clear()
