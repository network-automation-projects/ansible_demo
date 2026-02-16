"""
Drill 16: Write a Pydantic Model with Nested Validation
Fill in the TODOs. See README.md for the problem description.
Requires: pip install pydantic
"""

# TODO: from pydantic import BaseModel, field_validator


# TODO: class Job(BaseModel):
#     id: str
#     retries: int
#     metadata: dict
#
#     @field_validator("id")
#     def id_non_empty(cls, v): ...
#
#     @field_validator("retries")
#     def retries_range(cls, v): ...
#
#     @field_validator("metadata")
#     def metadata_keys_str(cls, v): ...


def main() -> None:
    # After implementing Job model:
    # j = Job(id="j1", retries=2, metadata={"env": "prod"})
    # print(j)
    print("Implement Job model first, then uncomment main()")


if __name__ == "__main__":
    main()
