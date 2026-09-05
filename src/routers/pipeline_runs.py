from datetime import datetime

from fastapi import APIRouter, Query
from pydantic import BaseModel

from src.load import try_create_connection
from src.repository.pipeline_runs import get_pipeline_runs


class PipelineRunResponse(BaseModel):
    id: int
    started_at: datetime
    finished_at: datetime | None
    status: str
    extracted: int | None
    transformed: int | None
    valid: int | None
    loaded: int | None
    error: str | None


router = APIRouter(prefix="/pipeline-runs", tags=["pipeline-runs"])


@router.get("/")
def get_pipeline_runs_endpoint(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[PipelineRunResponse]:
    connection = try_create_connection()

    try:
        rows = get_pipeline_runs(
            connection,
            limit=limit,
            offset=offset,
        )

        return [
            PipelineRunResponse(
                id=row[0],
                started_at=row[1],
                finished_at=row[2],
                status=row[3],
                extracted=row[4],
                transformed=row[5],
                valid=row[6],
                loaded=row[7],
                error=row[8],
            )
            for row in rows
        ]
    finally:
        connection.close()
