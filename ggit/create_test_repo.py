import subprocess
import os

def remove_repo(repo_dir = '/home/riccardoob/thesys/git_test'):
    process = subprocess.run(['rm', '-rf', repo_dir])
    if process.returncode != 0:
        return False
    return True
    
if not remove_repo():
    print('Error removing repo')
    exit(1)

try:
    os.mkdir('/home/riccardoob/thesys/git_test')
except FileExistsError:
    pass
os.chdir('/home/riccardoob/thesys/git_test')

subprocess.run(['git', 'init'])

find1_process = subprocess.run(['find', '.git/objects'], stdout=subprocess.PIPE)
print('Current objects:')
print(find1_process.stdout.decode('utf-8'))

echo_process = subprocess.Popen(['echo', 'test content'], stdout=subprocess.PIPE)
hash1_process = subprocess.run(['git', 'hash-object', '-w', '--stdin'], stdin=echo_process.stdout, stdout=subprocess.PIPE)
print('Created new object, hash:')
print(hash1_process.stdout.decode('utf-8'))

find2_process = subprocess.run(['find', '.git/objects', '-type', 'f'], stdout=subprocess.PIPE)
print('Hash is now saved in the objects directory:')
print(find2_process.stdout.decode('utf-8'))

with open('test.txt', 'w+') as f:
    f.write('version 1\n')
hash2_process = subprocess.run(['git', 'hash-object', '-w', 'test.txt'], stdout=subprocess.PIPE)
print('Created new object from file test.txt, version 1, hash:')
print(hash2_process.stdout.decode('utf-8'))

with open('test.txt', 'w+') as f:
    f.write('version 2\n')
hash3_process = subprocess.run(['git', 'hash-object', '-w', 'test.txt'], stdout=subprocess.PIPE)
print('Created new object from file test.txt, version 2, hash:')
print(hash3_process.stdout.decode('utf-8'))

find3_process = subprocess.run(['find', '.git/objects', '-type', 'f'], stdout=subprocess.PIPE)
print('Both files are now saved in the objects directory:')
print(find3_process.stdout.decode('utf-8'))



update_index1_process = subprocess.run(['git', 'update-index', '--add', '--cacheinfo', '100644', '83baae61804e65cc73a7201a7252750c76066a30', 'test.txt'], stdout=subprocess.PIPE)
print('Added test.txt to the index:')
print(update_index1_process.stdout.decode('utf-8'))

write_tree1_process = subprocess.run(['git', 'write-tree'], stdout=subprocess.PIPE)
print('Tree created, hash:')
print(write_tree1_process.stdout.decode('utf-8'))

cat_file1_process = subprocess.run(['git', 'cat-file', '-p', write_tree1_process.stdout.strip().decode('utf-8')], stdout=subprocess.PIPE)
print('Tree content:')
print(cat_file1_process.stdout.decode('utf-8'))

with open('new.txt', 'w+') as f:
    f.write('new file\n')
subprocess.run(['git', 'update-index', 'test.txt'], stdout=subprocess.PIPE)
subprocess.run(['git', 'update-index', '--add', 'new.txt'], stdout=subprocess.PIPE)
write_tree2_process = subprocess.run(['git', 'write-tree'], stdout=subprocess.PIPE)
print('Second tree created, hash:')
print(write_tree2_process.stdout.decode('utf-8'))

cat_file2_process = subprocess.run(['git', 'cat-file', '-p', write_tree2_process.stdout.strip().decode('utf-8')], stdout=subprocess.PIPE)
print('Second tree content:')
print(cat_file2_process.stdout.decode('utf-8'))

print(f'Pulling tree from {write_tree1_process.stdout.strip().decode("utf-8")}...')
subprocess.run(['git', 'read-tree', '--prefix=bak', write_tree1_process.stdout.strip().decode('utf-8')], stdout=subprocess.PIPE)

write_tree3_process = subprocess.run(['git', 'write-tree'], stdout=subprocess.PIPE)
print('Third tree created, hash:')
print(write_tree3_process.stdout.decode('utf-8'))

cat_file3_process = subprocess.run(['git', 'cat-file', '-p', write_tree3_process.stdout.strip().decode('utf-8')], stdout=subprocess.PIPE)
print('Third tree content:')
print(cat_file3_process.stdout.decode('utf-8'))

echo_process = subprocess.Popen(['echo', 'first commit'], stdout=subprocess.PIPE)
commit1_process = subprocess.run(['git', 'commit-tree', f'{write_tree1_process.stdout.strip().decode("utf-8")[:6]}'], stdin=echo_process.stdout, stdout=subprocess.PIPE)
print('First commit created, hash:')
print(commit1_process.stdout.decode('utf-8'))

print('First commit content:')
cat_file4_process = subprocess.run(['git', 'cat-file', '-p', commit1_process.stdout.strip().decode('utf-8')], stdout=subprocess.PIPE)
print(cat_file4_process.stdout.decode('utf-8'))

echo_process = subprocess.Popen(['echo', 'second commit'], stdout=subprocess.PIPE)
commit2_process = subprocess.run(['git', 'commit-tree', write_tree2_process.stdout.strip().decode('utf-8')[:6], '-p', commit1_process.stdout.strip().decode('utf-8')], stdin=echo_process.stdout, stdout=subprocess.PIPE)
print('Second commit created, hash:')
print(commit2_process.stdout.decode('utf-8'))

echo_process = subprocess.Popen(['echo', 'third commit'], stdout=subprocess.PIPE)
commit3_process = subprocess.run(['git', 'commit-tree', write_tree3_process.stdout.strip().decode('utf-8')[:6], '-p', commit2_process.stdout.strip().decode('utf-8')], stdin=echo_process.stdout, stdout=subprocess.PIPE)
print('Third commit created, hash:')
print(commit3_process.stdout.decode('utf-8'))

print('Current objects:')
find4_process = subprocess.run(['find', '.git/objects', '-type', 'f'], stdout=subprocess.PIPE)
print(find4_process.stdout.decode('utf-8'))






# process = subprocess.run('ls -a', shell=True, stdout=subprocess.PIPE)
# print(process.stdout.decode('utf-8'))

