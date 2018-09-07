# Chat-Bot
Example for Stream retrieval

get_info(table_name, keywords, query)
get_info('stream', ['COMPAS', 'COMPSS], ['COMP9444', 'COMP9318', 'COMP9417'])


Result is as below (a list of 2 sub-lists)

[ [ {'number': 1, 'electives': ['COMP9414', 'COMP9814']} ], 
[ {'number': 1, 'electives': ['COMP9313', 'COMP9315', 'COMP9319']}, {'number': 2, 'electives': ['COMP4141', 'COMP6741', 'MATH5845', 'MATH5855', 'MATH5905', 'MATH5960']} ]]
