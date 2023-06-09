# ruff: noqa: B008
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK

from app.domain.accounts.guards import requires_active_user
from app.domain.accounts.models import User
from app.domain.backlogs.dependencies import provides_service
from app.domain.backlogs.models import Backlog as Model
from app.domain.backlogs.models import ReadDTO, Service, WriteDTO

if TYPE_CHECKING:
    from uuid import UUID

    from litestar.contrib.repository.abc import FilterTypes


__all__ = [
    "ApiController",
]


validation_skip: Any = Dependency(skip_validation=True)


class ApiController(Controller):
    dto = WriteDTO
    return_dto = ReadDTO
    path = "/api/backlogs"
    dependencies = {"service": Provide(provides_service, sync_to_thread=False)}
    tags = ["Backlogs"]
    detail_route = "/detail/{row_id:uuid}"
    project_route = "/project/{project_type:str}"
    slug_route = "/slug/{slug:str}"
    guards = [requires_active_user]

    @get()
    async def filter(self, service: "Service", filters: list["FilterTypes"] = validation_skip) -> Sequence[Model]:
        return await service.list(*filters)

    @post()
    async def create(self, data: Model, current_user: User, service: "Service") -> Model:
        if not data.owner_id:
            data.owner_id = current_user.id
        if not data.assignee_id:
            data.assignee_id = current_user.id
        return await service.create(data)

    @get(detail_route)
    async def retrieve(self, service: "Service", row_id: "UUID") -> Model:
        return await service.get(row_id)

    @put(detail_route)
    async def update(self, data: Model, service: "Service", row_id: "UUID") -> Model:
        return await service.update(row_id, data)

    @delete(detail_route, status_code=HTTP_200_OK)
    async def delete(self, service: "Service", row_id: "UUID") -> Model:
        return await service.delete(row_id)

    @get(project_route)
    async def retrieve_by_project_type(self, service: "Service", project_type: str) -> list[Model]:
        return await service.filter_by_project_type(project_type)
