from .base_task import BaseScheme, BaseSchemeAdd


class ReactionsScheme(BaseScheme):
    reactions: list[str]


class ReactionsSchemeAdd(BaseSchemeAdd):
    reactions: list[str]
