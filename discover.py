from dataclasses import dataclass
from zeroconf import ServiceBrowser, ServiceInfo, ServiceListener, Zeroconf
import pyfzf
import time


WLED_TYPE = '_wled._tcp.local.'
WLED_NAME_SUFFIX = '.' + WLED_TYPE


def wled_service_name(full_name: str) -> str:
    assert full_name.endswith(WLED_NAME_SUFFIX), full_name
    return full_name.removesuffix(WLED_NAME_SUFFIX)


@dataclass(frozen=True)
class Service:
    name: str
    address: str

    @classmethod
    def from_zeroconf_info(cls, info: ServiceInfo) -> 'Service':
        name = wled_service_name(info.name)
        assert info.server == f'{name}.local.', info
        address = '.'.join(map(str, info.addresses[0]))
        return cls(name=name, address=address)


class ServiceCollectionListener(ServiceListener):
    def __init__(self, callback=None):
        super().__init__()
        self.services = set()
        self.callback = callback

    def _add(self, zc: Zeroconf, type_: str, name: str):
        service = Service.from_zeroconf_info(zc.get_service_info(type_, name))
        self.services.add(service)
        if self.callback is not None:
            self.callback(service)

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self._add(zc, type_, name)

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        return

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self._add(zc, type_, name)


def discover_wleds_until(until_returns, callback=None):
    zeroconf = Zeroconf()
    listener = ServiceCollectionListener(callback=callback)
    _browser = ServiceBrowser(zeroconf, WLED_TYPE, listener)
    try:
        until_returns()
    finally:
        zeroconf.close()
    return listener.services


def discover_wleds_for(seconds, callback=None):
    return discover_wleds_until(lambda: time.sleep(seconds), callback=callback)


def choose_wled_with_fzf(seconds):
    def format(service: Service):
        return f'{service.name} (http://{service.address}/)'

    services = list(discover_wleds_for(seconds))
    if not services:
        raise ValueError(
            f'Couldn\'t find a single WLED controller in the local network in {seconds} seconds;'
            f' consider increasing the discovery duration')
    elif len(services) == 1:
        service = services[0]
        print(f'Discovered only one WLED controller in the local network: {format(service)}.'
              f' Choosing it automatically.')
        return service
    else:
        print('Choose the WLED controller to operate on:')
        formatted_services = [f'{i}. {format(service)}' for i, service in enumerate(services, start=1)]
        choice = pyfzf.FzfPrompt().prompt(formatted_services, fzf_options='--height=~50% +m')[0]
        service_index = int(choice.split('.')[0]) - 1
        return services[service_index]


def main():
    services = discover_wleds_until(lambda: input("Press enter to exit...\n"), callback=print)
    print(services)


if __name__ == '__main__':
    main()
