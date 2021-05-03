'''
This is the file to delete the files
older than the specified days in the
given file location
'''

import os
import time


def delete_files():
    filePath = input('Enter the file path to delete the files from: ')
    no_of_days = int(input('How many days old file to be deleted?'))
    count = 0

    currentTime = time.time()
    no_of_days_time = currentTime - no_of_days * 86400
    for file in os.listdir(filePath):
        absolute_file_path = os.path.join(filePath, file)
        if os.stat(absolute_file_path).st_mtime < no_of_days_time:
            if os.path.isfile(absolute_file_path):
                os.remove(absolute_file_path)
                count += 1

    if count > 0:
        print(count, ' number of files have been deleted')
    else:
        print('No files where deleted from the given location')


if __name__ == '__main__':
    delete_files()
