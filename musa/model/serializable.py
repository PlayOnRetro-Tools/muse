from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Serializable:
    id: str = field(default_factory=lambda: uuid4().hex)
    name: str = ""
