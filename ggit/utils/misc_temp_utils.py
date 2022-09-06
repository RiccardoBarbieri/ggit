

def load_trees():
    main_tree = Tree()
    for i in os.listdir(Path(__file__).parent.parent /  'test' / 'assets' / 'tree_tester'):
        path = Path(__file__).parent.parent /  'test' / 'assets' / 'tree_tester' / i
        if path.is_file():
            with open(path, 'rb') as f:
                main_tree.append_item(Blob(f.read()), i, '100644' if path.name != 'bin' else '100755')
        if path.is_dir():
            sub_tree = Tree()
            for j in os.listdir(path):
                sub_path = path / j
                if sub_path.is_file():
                    with open(sub_path, 'rb') as f:
                        sub_tree.append_item(Blob(f.read()), j, '100644')
    main_tree.append_item(sub_tree, 'sub', '040000')
    return main_tree