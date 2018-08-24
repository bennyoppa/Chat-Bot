from db.retrieve_info import *
import re


if __name__ == '__main__':
    while True:
        print("---instruction---")
        print("c - Create database")
        print("d - Delete database")
        print("s - Search")
        print("q - Quit\n")
        action = input("Select an action: ")
        if action == 's':
            table_name = input("Enter a table name: ")
            match_keyword = input("Enter a search keyword: ")
            output = input("Enter desired search result: ")
            if len(output) == 0:
                output = []
            else:
                output = re.split(' ', output)
            print(get_course_info(table_name, match_keyword, output))
            print()
        elif action == 'q':
            break
        elif action == 'c':
            create_course_db()
            print()
        elif action == 'd':
            delete_course_db()
            print()
        else:
            continue
