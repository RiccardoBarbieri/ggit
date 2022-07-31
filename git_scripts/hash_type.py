import os
import subprocess
from pprint import pprint
from enum import Enum
from typing import List
from process_exception import ProcessException

class HashType(Enum):

    BLOB = 0
    TREE = 1
    COMMIT = 2

class HashIdentifier:

    files: List[str] = []
    hashes_types: List[List[str]] = []
    
    def __init__(self, repository = '/home/riccardoob/thesys/git_test'):
        self.repository = repository
        try:
            os.chdir(repository)
        except FileNotFoundError:
            print('Directory not found')
            raise FileNotFoundError(f'{repository} is not a valid directory.')


    def get_all_objects(self) -> List[str]:
        find1_process = subprocess.run(['find', '.git/objects', '-type', 'f'], stdout=subprocess.PIPE)
        if find1_process.stderr:
            raise ProcessException(find1_process.stderr.strip().decode('utf-8'))
        self.files = find1_process.stdout.strip().decode('utf-8').split('\n')
        
        return self.files
    
    def get_all_hashes(self) -> List[str]:
        self.get_all_objects()
        
        for file in self.files:
            temp = []
            temp.append(file)

            temp.append(''.join(i.split('/')[2:]))

            hash_type_process = subprocess.run(['git', 'cat-file', '-t', temp[1]], stdout=subprocess.PIPE)
            if hash_type_process.stderr:
                raise ProcessException(hash_type_process.stderr.strip().decode('utf-8'))
            temp.append(hash_type_process.stdout.strip().decode('utf-8'))


    # def get_all_hashes(self):
    #     self.get_all_objects()
        
    #     for i in self.files:
    #         temp = []
    #         temp.append(i)
    #         temp.append(''.join(i.split('/')[2:]))
    #         hash_type = subprocess.run(['git', 'cat-file', '-t', temp[1]], stdout=subprocess.PIPE)
    #         if hash_type.stderr:
    #             print('Error:')
    #             print(hash_type.stderr.decode('utf-8'))
    #             continue
    #         temp.append(hash_type.stdout.decode('utf-8').strip())
    #         hash_files.append(temp)

hash_identifier = HashIdentifier()

print(hash_identifier.get_all_objects())

