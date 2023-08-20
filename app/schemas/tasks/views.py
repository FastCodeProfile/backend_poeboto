from .base_task import BaseScheme, BaseSchemeAdd


class ViewsScheme(BaseScheme):
    limit: int = 1


class ViewsSchemeAdd(BaseSchemeAdd):
    limit: int = 1
