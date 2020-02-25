from model import Index


def add_file_to_index(file, index):
    try:
        msg = index.add_file(file)
    except (
            IndexError,
            FileNotFoundError,
            IsADirectoryError,
            PermissionError
            ) as e:
        print(e)
    else:
        print(msg)


def main():
    # create a new index
    try:
        index = Index()
    except ValueError as e:
        print(e)

    try:
        with open('files.txt') as file:
            for line in file:
                if not line.strip() or line.strip().startswith('#'):
                    continue
                add_file_to_index(line.split()[0], index)
    except FileNotFoundError:
        print('files.txt was not found, continuing with manual file addition.')
        prompt = 'File to add to index (or simply press enter for query): '
        while (file := input(prompt)) != "":
            add_file_to_index(file, index)

    query = input("Query: ")
    try:
        print('Files that matched the query:', *index.get_result_for_query(query))
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
