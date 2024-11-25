import enum
import json
from datetime import datetime, timezone


class Status(enum.Enum):
    available = 'в наличии'
    out = 'выдана'


class Book:
    def __init__(self, title: str, author: str, year: int,
                 storage='library.json') -> None:
        self.__storage = storage

        self.id = self.__set_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = Status.available
        self.created_at = datetime.now(timezone.utc)
        self.status_changed = self.created_at

    def __set_id(self) -> int:
        with open(self.__storage, 'r') as f:
            lib_content = json.load(f)
        new_id = lib_content['id_count'] + 1
        lib_content['id_count'] = new_id
        with open(self.__storage, 'w') as f:
            f.write(json.dumps(lib_content))
        return new_id

    def to_dict(self) -> dict[str, str | int]:
        book_as_dict = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status.value,
            'status_changed': self.status_changed,
            'created_at': self.created_at,
        }
        return book_as_dict

    def __str__(self) -> str:
        return (f'"{self.title}", {self.author}, {self.year} '
                f'(с {self.status_changed.date()} {self.status.value})')

    def __repr__(self) -> str:
        return (f'<Book({self.id}) Created_at="{self.created_at}"; '
                f'Name="{self.title}"; Author="{self.author}"; '
                f'Year="{self.year}"; Status="{self.status.name}"; '
                f'Status_changed="{self.status_changed}">')


if __name__ == '__main__':
    book = Book('Война и Мир', 'Толстой Л.Н.', 1873)
    print(f'{book!s}')  # PRINT_DEL
    print(f'{book!r}')  # PRINT_DEL
