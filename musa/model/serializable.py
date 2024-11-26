from dataclasses import dataclass, field
from typing import Any, Dict, Type, TypeVar
from uuid import UUID, uuid4

T = TypeVar("T", bound="Serializable")


@dataclass
class Serializable:
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        # Convert string UUID back to UUID object
        if "id" in data:
            data["id"] = UUID(data["id"])
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, UUID):
                result[key] = str(value)
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, Serializable) else item
                    for item in value
                ]
            elif isinstance(value, Serializable):
                result[key] = value.to_dict()
            else:
                result[key] = value

        return result
