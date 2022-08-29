import sys
from pathlib import Path

from rich.console import Console

sys.path.append(Path(__file__).parent.parent.parent.__str__())

from ggit.converter.git_connector import GitConnectorSubprocess
from ggit.entities.blob import Blob
from ggit.utils import walk_folder_flat

console = Console()
git_connector = GitConnectorSubprocess()
for i in walk_folder_flat(Path(__file__).parent.joinpath("assets")):
    with open(i, 'rb') as f:
        blob = Blob(f.read())
        real_hash = git_connector.hash_object(i)
        
        console.print(f"[blue]{i.name}[/blue]")
        if blob.hash == real_hash:
            console.print(f"[green]{real_hash} -> {blob.hash}[/green]")
        else:
            console.print(f"[red]{real_hash} -> {blob.hash}[/red]")
        assert blob.hash == real_hash

