from typing import Any, Dict, Iterator, List, Optional
from uuid import UUID

from iterator import CollectionIterator, I

from .animation import Animation
from .observable import CollectionSignals


class AnimationCollection:
    def __init__(self) -> None:
        self.animations: Dict[UUID, Animation] = {}
        self.signals = CollectionSignals()

    def to_dict(self) -> Dict[str, Any]:
        return {"animations": {str(k): v.to_dict() for k, v in self.animations.items()}}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnimationCollection":
        collection = cls()
        animations_data = data.get("animations", {})
        for (
            anim_id,
            anim_data,
        ) in animations_data.items():
            animation = Animation.from_dict(anim_data)
            collection.animations[UUID(anim_id)] = animation
        collection.signals.collectionLoaded.emit()
        return collection

    def create_animation(self, name: str) -> Animation:
        animation = Animation(name=name)
        self.animations[animation.id] = animation
        self.signals.animationAdded.emit(animation.id)
        return animation

    def get_animation(self, animation_id: UUID) -> Optional[Animation]:
        return self.animations.get(animation_id)

    def update_animation(self, animation_id: UUID, name: str) -> bool:
        if animation := self.animations.get(animation_id):
            animation.name = name
            self.signals.animationModified.emit(animation_id)
            return True
        return False

    def delete_animation(self, animation_id: UUID) -> Optional[Animation]:
        if animation := self.animations.pop(animation_id, None):
            self.signals.animationRemoved.emit(animation_id)
            return animation
        return None

    def commit_all_changes(self):
        for animation in self.list_animations():
            animation.commit_frame_changes()

    def list_animations(self) -> List[Animation]:
        return list(self.animations.values())

    def __iter__(self) -> Iterator[I]:
        return CollectionIterator(self.list_animations())
