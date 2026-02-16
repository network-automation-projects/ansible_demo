"""
Drill 16: Write a Pydantic Model with Nested Validation — Reference solution.
"""

from pydantic import BaseModel, field_validator


class Job(BaseModel):
    id: str
    retries: int
    metadata: dict

    @field_validator("id")
    @classmethod
    def id_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("id must be non-empty")
        return v

    @field_validator("retries")
    @classmethod
    def retries_range(cls, v: int) -> int:
        if not 0 <= v <= 5:
            raise ValueError("retries must be 0-5")
        return v

    @field_validator("metadata")
    @classmethod
    def metadata_keys_str(cls, v: dict) -> dict:
        for k in v:
            if not isinstance(k, str):
                raise ValueError("metadata keys must be strings")
        return v


def main() -> None:
    j = Job(id="j1", retries=2, metadata={"env": "prod"})
    print(j)


if __name__ == "__main__":
    main()
