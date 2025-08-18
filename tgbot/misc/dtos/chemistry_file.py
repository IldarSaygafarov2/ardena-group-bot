from pydantic import BaseModel

class ChemistryFileDTO(BaseModel):
    name: str
    file_path: str
    file_type: str
    date: str
