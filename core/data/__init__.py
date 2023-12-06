"""Contains data wrappers"""


from typing import Callable
import uuid


__DATA = object


__ENTITIES: dict[str, list[__DATA]] = {}
__SERVICES_MAPPINGS: dict[Callable[..., None], tuple[list[type[__DATA]], list[type[__DATA]], list[list[__DATA]]]] = {}


def create_new_entity(data_list: list[__DATA]) -> None:
    key = str(uuid.uuid4())
    __ENTITIES[key] = data_list

def register_service(function: Callable[..., None], required: list[type[__DATA]] = [], forbidden: list[type[__DATA]] = []) -> None:
    __SERVICES_MAPPINGS[function] = (required, forbidden, [])

def run_services() -> None:
    run_startup_services()
    for service in __SERVICES_MAPPINGS:
        for arguments in __SERVICES_MAPPINGS[service][2]:
            service(*arguments)

def run_startup_services() -> None:
    map_entities()

def map_entities() -> None:
    for entity in __ENTITIES:
        for service in __SERVICES_MAPPINGS:
            valid_data: list[__DATA] = []
            has_forbidden = False
            required, forbidden, _ = __SERVICES_MAPPINGS[service]
            for data in __ENTITIES[entity]:
                if type(data) in required:
                    valid_data.append(data)
                if type(data) in forbidden:
                    has_forbidden = True
            if len(valid_data) == len(__SERVICES_MAPPINGS[service][0]) and has_forbidden == False:
                __SERVICES_MAPPINGS[service][2].append(valid_data)
