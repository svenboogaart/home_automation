from dataclasses import dataclass


@dataclass
class HueConnectionSettings:
    id: str
    internal_ipaddress: str
    port: str
