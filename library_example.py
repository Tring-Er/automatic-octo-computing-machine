from dataclasses import dataclass
from core.data import create_new_entity, register_service, run_services


@dataclass(slots=True)
class Health:
    max_value: int
    current_value: int | None = None

    def __post_init__(self) -> None:
        if self.current_value is None:
            self.current_value = self.max_value

@dataclass(slots=True)
class Velocity:
    speed: int
    value: int = 0

def generic_service(velocity_component: Velocity) -> None:
    velocity_component.value += velocity_component.speed
    if velocity_component.value >= 10:
        velocity_component.value = 10

def another_generic_service(health_component: Health) -> None:
    if health_component.current_value is not None:
        health_component.current_value -= 1


create_new_entity([Health(10)])
create_new_entity([Health(5), Velocity(2)])
create_new_entity([Health(3), Velocity(5)])
register_service(generic_service, required=[Velocity])
register_service(another_generic_service, required=[Health], forbidden=[Velocity])
run_services()