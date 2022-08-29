# import hashlib

# #first tree
# mode1_sub = b'100644'
# name1_sub = b'test.txt'
# sha1_sub = '83baae61804e65cc73a7201a7252750c76066a30'

# sub_tree_body = mode1_sub + b' ' + name1_sub + b'\0' + bytes.fromhex(sha1_sub)

# sub_tree_mode = b'40000'
# sub_tree_name = b'bak'
# sub_tree_hash = b'tree ' + str(len(sub_tree_body)).encode() + b'\0' + sub_tree_body

# print('sub tree hash ' + hashlib.sha1(sub_tree_hash).hexdigest())

# mode1 = b"100644"
# name1 = b"new.txt"
# sha1_1 = "fa49b077972391ad58037050f2a75f74e3671e92"
# mode2 = b"100644"
# name2 = b"test.txt"
# sha1_2 = "1f7a7a472abf3dd9643fd615f6da379c4acb3e3a"

# # body = f'{mode1} {name1}\0{sha1_1}{mode2} {name2}\0{sha1_2}'.encode()
# body = b""
# body += sub_tree_mode
# body += b" "
# body += sub_tree_name
# body += b"\0"
# body += bytes.fromhex(hashlib.sha1(sub_tree_hash).hexdigest())

# body += mode1
# body += b" "
# body += name1
# body += b"\0"
# body += bytes.fromhex(sha1_1)

# body += mode2
# body += b" "
# body += name2
# body += b"\0"
# body += bytes.fromhex(sha1_2)
# # print(body)

# hashlib.sha1(b"tree " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest()
# print(hashlib.sha1(b"tree " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest())


# # hashlib.sha1(f"blob {self.__length}\0{self.__content}".encode()).hexdigest()

