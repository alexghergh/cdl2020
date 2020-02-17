from cdl import index


def main():
    prompt = 'File to add to index (or simply press enter for query): '
    while (file := input(prompt)) != "":
        try:
            msg = index.add_file(file)
        except (
                FileNotFoundError,
                IsADirectoryError,
                PermissionError,
                Exception
                ) as e:
            print(e)
        else:
            print(msg)
    query = input("Query: ")
    print('Files that matched the query:', *index.get_result_for_query(query))


if __name__ == '__main__':
    main()
