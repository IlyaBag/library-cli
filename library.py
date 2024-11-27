import argparse

from operations import Library, Status


def main():
    actions_map = {
        'add': create_book,
        'delete': remove_book,
        'find': search,
        'all': show_all_books,
        'status': change_status,
    }
    actions = tuple(actions_map.keys())

    parser = argparse.ArgumentParser(
        prog='python3 library.py',
        description='Приложение для управления хранилищем книг библиотеки'
    )
    parser.add_argument('action', choices=actions,
                        help='Указывает желаемое действие')
    parser.add_argument('-f', '--file', default='library.json',
                        help='Путь до файла хранилища книг')
    args = parser.parse_args()

    library = Library(storage_path=args.file)
    actions_map[args.action](library)

def create_book(lib: Library) -> None:
    title = input('Название книги: ')
    author = input('Автор книги: ')
    year = int(input('Год выхода книги: '))
    print()
    print(lib.add_book(title=title, author=author, year=year))

def remove_book(lib: Library) -> None:
    id = int(input('ID книги, которую нужно удалить: '))
    print()
    print(lib.delete_book(id=id))

def search(lib: Library) -> None:
    title = input('Название книги: ') or None
    author = input('Автор книги: ') or None
    year = int(input('Год выхода книги: ') or 0) or None
    books = lib.find_book(title=title, author=author, year=year)
    print()
    if not books:
        print('Ни одной книги не найдено')
    else:
        for book in books:
            print(book)

def show_all_books(lib: Library) -> None:
    for book in lib.get_all_books():
        print(book)

def change_status(lib: Library) -> None:
    id = int(input('ID книги: '))
    status = input(f'Доступные статусы: {', '.join(Status)}\nПрисвоить статус: ')
    print()
    print(lib.set_book_status(id=id, status=status))


if __name__ == '__main__':
    main()
