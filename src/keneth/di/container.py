from keneth.di_contracts import ContainerInterface, ServiceInterface

from .container_context import ContainerContext

type ServiceType = type[ServiceInterface]


class Container(ContainerInterface):
    """Concrete implementation of the dependency injection container."""

    def __init__(self) -> None:
        """Initialize the container with empty contexts and instances."""
        super().__init__()
        self.__instances: dict[ServiceType, ServiceInterface] = {}
        self.__context = ContainerContext()
        self.__permanent_context = ContainerContext()
        self.__permanent_context.add_instance(self)

    def get_context(self) -> ContainerContext:
        return self.__context

    def get_permanent_context(self) -> ContainerContext:
        return self.__permanent_context

    def clear_context(self) -> None:
        self.__context = ContainerContext()

    def call(self, func: callable) -> any:
        args = []
        for name, param_type in func.__annotations__.items():
            if isinstance(param_type, type) and issubclass(
                param_type, ServiceInterface
            ):
                args.append(self.provide(param_type))
            else:
                args.append(self.bind_param(name, param_type))
        return func(*args)

    def provide(self, service_type: ServiceType) -> ServiceInterface:
        if service_type in self.__instances:
            return self.__instances[service_type]
        if service_type in self.__context.get_targets():
            message = (
                f"Circular dependency detected for service: {service_type.__name__}"
            )
            raise RuntimeError(message)
        self.__context.add_target(service_type)
        instance = service_type.__new__(service_type)
        self.__context.add_binding("self", instance)
        self.call(instance.__init__, self.__context)
        self.__instances[service_type] = instance
        return instance

    def bind_param(self, name: str, param_type: type) -> object | None:
        val = self.get_instance_from_type(param_type)
        if val is not None:
            return val
        val = self.get_binding(name)
        if val is not None:
            return val
        message = f"No binding found for parameter: {name}"
        raise RuntimeError(message)
