from typing import Dict, List, Type
from keneth.di_contracts import ContainerInterface, ServiceInterface, ContainerContextInterface

from .container_context import ContainerContext

type ServiceType = Type[ServiceInterface]


class Container(ContainerInterface):
    def __init__(self):
        super().__init__()
        self.instances: Dict[ServiceType, ServiceInterface] = {}

    def call(self, func: callable, targets: List[ServiceType] = None) -> any:
        args = []
        for name, param_type in func.__annotations__.items():
            if isinstance(param_type, type) and issubclass(
                param_type, ServiceInterface
            ):
                args.append(self.provide(param_type, targets))
            else:
                args.append(self.bind_param(name, param_type, targets))
        return func(*args)

    def provide(
        self,
        service_type: ServiceType,
        context: ContainerContextInterface = None,
    ) -> ServiceInterface:
        if service_type in self.instances:
            return self.instances[service_type]
        context = context or ContainerContext()
        if service_type in context.get_targets():
            raise RuntimeError(
                f"Circular dependency detected for service: {service_type.__name__}"
            )
        context.add_target(service_type)
        instance = service_type.__new__(service_type)
        context.add_binding('self', instance)
        self.call(instance.__init__, context)
        self.instances[service_type] = instance
        return instance

    def bind_param(
        self, name: str, type: Type, targets: List[ServiceType] = None
    ) -> any:
        if name in self.bindings:
            return self.bindings[name]
        for target in reversed(targets or []):
            if hasattr(target, "bind_param") and callable(
                getattr(target, "bind_param")
            ):
                return target.bind_param(name, type, targets)
        raise RuntimeError(f"No binding found for parameter: {name}")
