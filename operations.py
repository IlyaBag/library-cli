import enum
import json
from datetime import datetime, timezone
from typing import TypeAlias

from exceptions import BookNotFoundError


BooksBunch: TypeAlias = list[dict[str, str | int]]


class Status(enum.StrEnum):
    available = 'в наличии'
    out = 'выдана'


class Book:
    """Represent a book in a library."""

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
        """Retrieve id counter from storage, increment it and save new value of
        counter. Return id for creating new Book instance.
        """

        with open(self.__storage, 'r') as f:
            lib_content = json.load(f)
        new_id = lib_content['id_count'] + 1
        lib_content['id_count'] = new_id
        with open(self.__storage, 'w') as f:
            f.write(json.dumps(lib_content))
        return new_id

    def chage_status(self, status: Status) -> None:
        """Update status-bounded atributes of Book instance."""
        self.status = status
        self.status_changed = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, str | int]:
        """Convert the instanse of the class to a dict which keys are names of
        class atributes and values are atribute values. Return the resulting
        dict.
        """

        book_as_dict = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
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
    """Provide methods for managing a library's storage of books represented
    by a json file.
    """

    def __init__(self, storage_path: str = 'library.json') -> None:
        self.storage_path = storage_path

    def add_book(self, title: str, author: str, year: int) -> str:
        """Create new book and save it to storage."""
        new_book = Book(title, author, year)
        library = self._open_storage(self.storage_path)
        library['books'].append(new_book.to_dict())
        self._save_to_storage(library)
        return f'{new_book!s}\nКнига добавлена в библиотеку.'

    def delete_book(self, id: int) -> str:
        """Delete book from storage by given id."""
        library = self._open_storage(self.storage_path)
        index, book = self._get_book_by_id(id, library['books'])
        library['books'].pop(index)
        self._save_to_storage(library)
        return f'{book}\nКнига удалена'

    def find_book(self, title: str | None = None, author: str | None = None,
                  year: int | None = None) -> list[Book] | str:
        """Strict search of book in a storage. Attributes 'title', 'author' and
        'year' can be combined in any way and refine the search.
        """

        library = self._open_storage(self.storage_path)
        kwargs = {'title': title, 'author': author, 'year': year}
        search_criterias = {k: v for k, v in kwargs.items() if v is not None}
        finded_books = []
        for book in library['books']:
            fields_to_compare = {k: book.get(k) for k in search_criterias}
            if search_criterias == fields_to_compare:
                finded_books.append(Book(**book))
        if not finded_books:
            return 'Ни одной книги не найдено'
        return finded_books

    def get_all_books(self) -> list[Book]:
        """Retrieve all books from storage and return list of all books."""
        library = self._open_storage(self.storage_path)
        all_books = [Book(**book) for book in library['books']]
        return all_books

    def set_book_status(self, id: int, status: str) -> str:
        """Change status of book finded by given id."""
        new_enum_status = Status(status)
        library = self._open_storage(self.storage_path)
        index, book = self._get_book_by_id(id, library['books'])
        book.chage_status(new_enum_status)
        library['books'][index] = book.to_dict()
        self._save_to_storage(library)
        return f'{book}\nСтатус книги изменён'

    def _open_storage(self, path: str) -> dict[str, int | BooksBunch]:
        """Open json file and return deserialized object."""
        with open(path, 'r') as f:
            content = json.load(f)
        return content

    def _save_to_storage(self, data: dict[str, int | BooksBunch]) -> None:
        """Save given data to json file."""
        with open(self.storage_path, 'w') as f:
            f.write(json.dumps(data))

    def _get_book_by_id(self, id: int, data: BooksBunch) -> tuple[int, Book]:
        """Return book object with given id if id was found in storage."""
        if id < 1:
            raise ValueError('Parameter \'id\' must be greater than or equal '
                             f'to 1, got {id}')
        index = self._find_index_by_id(id, data)
        if index is None:
            raise BookNotFoundError(f'Книга с id={id} не найдена.')
        return index, Book(**data[index])

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
    print(library.delete_book(id=23))
    # print(library._open_storage('library.json'))  # PRINT_DEL
    for book in library.get_all_books():
        print(book)
    # print(library.find_book(author='Толстой Л.Н.', title='Война и Мир'))
    print(library.set_book_status(24, 'выдана'))
