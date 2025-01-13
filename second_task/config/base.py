from sqlalchemy import BigInteger
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base(type_annotation_map={int: BigInteger})
