from db.retrieve_info import *
import re


if __name__ == '__main__':
    while True:
        print("---instruction---")
        print("c - Create database")
        print("s - Search")
        print("q - Quit\n")
        action = input("Select an action: ")
        if action == 's':
            table_name = input("Enter a table name: ")
            match_keyword = input("Enter a search keyword: ")
            if len(match_keyword) == 0:
                match_keyword = []
            else:
                match_keyword = re.split(' ', match_keyword)
            output = input("Enter query: ")
            if len(output) == 0:
                output = []
            else:
                output = re.split(' ', output)
            print(get_info(table_name, match_keyword, output))
            print()
        elif action == 'q':
            break
        elif action == 'c':
            db_name = input("Enter a database name: ")
            if db_name == 'course':
                create_course_db()
            elif db_name == 'stream':
                create_stream_db()
            else:
                print('Wrong database name.')
            print()
        else:
            continue
