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
                 storage: str = 'library.json',
                 id: int | None = None,
                 status: Status | str | None = None,
                 status_changed: str | None = None,
                 created_at: str | None = None) -> None:
        self.__storage = storage

        self.title = title
        self.author = author
        self.year = year
        if not id:
            self.id = self.__set_id()
        else:
            self.id = id
        if not status:
            self.status = Status.available
        else:
            self.status = Status(status)
        if not created_at:
            self.created_at = datetime.now(timezone.utc)
        else:
            self.created_at = datetime.fromisoformat(created_at)
        if not status_changed:
            self.status_changed = self.created_at
        else:
            self.status_changed = datetime.fromisoformat(status_changed)

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

    def delete_book(self, id: int) -> str:
        """Delete book from storage by given id."""
        if id < 1:
            raise ValueError(
                'Parameter "id" must be greater than or equal to 1, got', id
            )
        library = self._open_storage(self.storage_path)
        index = self._find_index_by_id(id, library['books'])
        if index is None:
            return f'Книга с id = {id} не найдена.'
        deleted = library['books'].pop(index)
        deleted_book = Book(**deleted)
        self._save_to_storage(library)
        return f'{deleted_book}\nКнига удалена'

    def find_book(self, title: str | None = None, author: str | None = None,
                  year: int | None = None) -> ...:
        ...

    def get_all_books(self) -> list[Book]:
        library = self._open_storage(self.storage_path)
        all_books = [Book(**book) for book in library['books']]
        return all_books

    def set_book_status(self, id: int, status: Status) -> ...:  # Как удобнее вводить статус?
        ...

    def _open_storage(self, path: str) -> dict[str, int | BooksBunch]:
        with open(path, 'r') as f:
            content = json.load(f)
        return content

    def _save_to_storage(self, data: dict[str, int | BooksBunch]) -> None:
        with open(self.storage_path, 'w') as f:
            f.write(json.dumps(data))

    def _find_index_by_id(self, id: int, data: BooksBunch) -> int | None:
        """Find the book index in the list of all saved books by given id."""
        if len(data) == 0:
            return None
        i_start = 0
        i_end = len(data) - 1
        while i_start <= i_end:
            i_mid = (i_start + i_end) // 2
            if id == (mid_val := data[i_mid]['id']):
                return i_mid
            elif id > mid_val:
                i_start = i_mid + 1
            else:
                i_end = i_mid - 1
        return None


if __name__ == '__main__':
    library = Library()
    # print(library.add_book('Война и Мир', 'Толстой Л.Н.', 1873))  # PRINT_DEL
    print(library.delete_book(id=18))
    # print(library._open_storage('library.json'))  # PRINT_DEL
    for book in library.get_all_books():
        print(book)
