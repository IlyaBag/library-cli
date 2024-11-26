import enum
import json
from datetime import datetime, timezone
from typing import TypeAlias


BooksBunch: TypeAlias = list[dict[str, str | int]]


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
            'status_changed': str(self.status_changed),
            'created_at': str(self.created_at)
        }
        return book_as_dict

    def __str__(self) -> str:
        return (f'[{str(self.id)+"]":<4}"{self.title}", {self.author}, '
                f'{self.year} (с {self.status_changed.date()} {self.status})')

    def __repr__(self) -> str:
        return (f'<Book({self.id}) Created_at="{self.created_at}"; '
                f'Name="{self.title}"; Author="{self.author}"; '
                f'Year="{self.year}"; Status="{self.status.name}"; '
                f'Status_changed="{self.status_changed}">')


class Library:
    def __init__(self, storage_path: str = 'library.json') -> None:
        self.storage_path = storage_path

    def add_book(self, title: str, author: str, year: int) -> str:
        new_book = Book(title, author, year)
        library = self._open_storage(self.storage_path)
        library['books'].append(new_book.to_dict())
        self._save_to_storage(library)
        return f'{new_book!s}\nКнига добавлена в библиотеку.'

    def delete_book(self, id: int) -> ...:
        ...

    def find_book(self, title: str | None = None, author: str | None = None,
                  year: int | None = None) -> ...:
        ...

    def get_all_books(self) -> ...:
        ...

    def set_book_status(self, id: int, status: Status) -> ...:  # Как удобнее вводить статус?
        ...

    def _open_storage(self, path: str) -> dict[str, int | BooksBunch]:
        with open(path, 'r') as f:
            content = json.load(f)
        return content

    def _save_to_storage(self, data) -> None:
        with open(self.storage_path, 'w') as f:
            f.write(json.dumps(data))


if __name__ == '__main__':
    library = Library()
    print(library.add_book('Война и Мир', 'Толстой Л.Н.', 1873))  # PRINT_DEL
    print(library._open_storage('library.json'))  # PRINT_DEL
