import json

from pydantic import BaseModel, Field


class RoleMetadata(BaseModel):
    description: str = Field(description="Basic description of the role and its purpose.")
    model: str | None = Field(description="Model to be used for executing this role.")


def main(argv=None):
    url = "TBD"
    name = "aergia-role-metadata"
    version = "0.1.0"
    id = f"https://{url}/{name}-{version}.json"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": id,
    }
    schema.update(RoleMetadata.model_json_schema())
    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
