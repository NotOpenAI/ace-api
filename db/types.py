from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column
import datetime
from sqlalchemy import func, String, Numeric, Text
from decimal import Decimal

intpk = Annotated[int, mapped_column(primary_key=True)]
int_def_0 = Annotated[int, mapped_column(default=0)]
currency = Annotated[Decimal, mapped_column(Numeric(15, 2))]
str_20 = Annotated[str, mapped_column(String(20))]
str_50 = Annotated[str, mapped_column(String(50))]
str_100 = Annotated[str, mapped_column(String(100))]
str_255 = Annotated[str, mapped_column(String(255))]
str_text = Annotated[str, mapped_column(Text())]
create_date = Annotated[
    datetime.datetime,
    mapped_column(server_default=func.current_timestamp()),
]
update_date = Annotated[
    datetime.datetime, mapped_column(onupdate=func.current_timestamp(), nullable=True)
]
dt = Annotated[datetime.datetime, mapped_column()]
