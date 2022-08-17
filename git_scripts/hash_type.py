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

class GitHash:

    __hash: str = ''
    __type: HashType = None

    __path: str = ''
    __repo: str = ''

    def __init__(self, hash: str, type: HashType, path: str, repo: str):
        self.__hash = hash
        self.__type = type
        self.__path = path
        self.__repo = repo

    @property
    def hash(self) -> str:
        return self.__hash

    @property
    def type(self) -> HashType:
        return self.__type

    @property
    def repo(self) -> str:
        return self.__repo
    
    @property
    def path(self) -> str:
        return self.__path



class HashIdentifier:

    __files: List[str] = []
    __hashes: List[GitHash] = []
    
    def __init__(self, repository = '/home/riccardoob/thesys/git_test'):
        self.repository = repository
        try:
            os.chdir(repository)
        except FileNotFoundError:
            print('Directory not found')
            raise FileNotFoundError(f'{repository} is not a valid directory.')

    def __get_all_objects(self) -> List[str]:
        find1_process = subprocess.run(['find', '.git/objects', '-type', 'f'], stdout=subprocess.PIPE)
        if find1_process.stderr:
            raise ProcessException(find1_process.stderr.strip().decode('utf-8'))
        self.__files = find1_process.stdout.strip().decode('utf-8').split('\n')
        
        return self.__files
    
    def get_all_hashes(self) -> List[str]:
        self.__get_all_objects()
        
        for file in self.__files:
            hash = ''.join(file.split('/')[2:])
            
            hash_type_process = subprocess.run(['git', 'cat-file', '-t', hash], stdout=subprocess.PIPE)
            if hash_type_process.stderr:
                raise ProcessException(hash_type_process.stderr.strip().decode('utf-8'))

            self.__hashes.append(
                GitHash(
                    hash,
                    HashType[hash_type_process.stdout.strip().decode('utf-8').upper()],
                    file,
                    self.repository
                )
            )

        


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

# hash_identifier = HashIdentifier()

# print(hash_identifier.get_all_objects())

print(HashType['TREE'])