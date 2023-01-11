import enum
from strenum import StrEnum
from rs.core import pipe as p


class Type(StrEnum):
    aiueo = enum.auto()
    aiueo2 = enum.auto()
    open = enum.auto()


TYPE_LIST = p.pipe(
    Type,
    p.map(lambda x: x.value),
    list,
)

if __name__ == '__main__':
    print(TYPE_LIST)
