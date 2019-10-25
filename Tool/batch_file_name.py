import click 
from pathlib import Path



@click.command()
@click.option('--dir', '-d', prompt='direction',help='你想替换哪个目录下的文件')
@click.option('--old-extention', '-o', prompt='old extention')
@click.option('--new-extention', '-n', prompt='new extention')
@click.option('--recursive', '-r', prompt='recursive [y/n]')
def main(dir, old_extention, new_extention, recursive):
    batch_name(dir, old_extention, new_extention, recursive)


def batch_name(dir, old_extention, new_extention, recursive):
    p = Path(dir)
    for file in p.iterdir():
        if file.is_dir() and recursive == 'y':
            batch_name(file, old_extention, new_extention, recursive)
        if file.is_file() and file.suffix == '.' + old_extention:
            file.rename(file.with_suffix('.' + new_extention))

if __name__ == "__main__":
    main()