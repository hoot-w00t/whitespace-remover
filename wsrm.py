#!/usr/bin/python3

"""
    Whitespace Remover
    Copyright (C) 2019  akrocynova

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from argparse import ArgumentParser
from os.path import join, isdir, isfile, splitext
from os import listdir

safe_exts = [".c", ".h", ".cpp", ".py", ".cs", ".class", ".java", ".sh",
              ".swift", ".vb", ".asp", ".aspx", ".css", ".html", ".htm",
              ".php", ".js", ".jsp", ".rss", ".xml", ".json", ".rst", ".md",
              ".txt"
              ]

def backup_file(filepath):
    try:
        with open(filepath, 'rb') as origin:
            with open(f"{filepath}.backup", 'wb') as backup:
                backup.write(origin.read())
        return True

    except Exception as e:
        print(f"'{filepath}': Skipping file because it could not be backed up: {e}")
        return False

def remove_ws_from_file(filepath, display_ws_lines=True, dry_run=False):
    try:
        with open(filepath, 'r') as file_input:
            file_content = []
            line_nb = 1
            whitespace_count = 0

            for line in file_input.readlines():
                file_content.append(line.rstrip())
                if len(file_content[line_nb - 1]) < len(line.replace('\n', '')):
                    whitespace_count += 1
                    if display_ws_lines:
                        print(f"{filepath}: line {line_nb}: {file_content[line_nb - 1]}")
                line_nb += 1

            print(f"{filepath}: removed {whitespace_count} whitespaces")

        if whitespace_count > 0 and not dry_run:
            with open(filepath, 'w') as file_output:
                file_output.write('\n'.join(file_content))

        file_content.clear()
        return True

    except Exception as e:
        print(f"Error while processing '{filepath}': {e}")
        return False

def is_file_safe(filepath):
    file_name, file_ext = splitext(filepath)
    if file_ext.lower() in safe_exts:
        return True

    return False

if __name__ == "__main__":
    arg_parser = ArgumentParser(description="Whitespace Remover")
    arg_parser.add_argument("-d", "--dry-run", dest="dry_run", action="store_true", help="Execute the program but don't write anything to the files.")
    arg_parser.add_argument("-l", "--lines", dest="display_lines", action="store_true", help="Display lines that contain a whitespace.")
    arg_parser.add_argument("-b", "--backup", dest="backup", action="store_true", help="Backup each file before processing it.")
    arg_parser.add_argument("-f", "--force", dest="force_process", action="store_true", help="Process unsafe files (not recommended).")
    arg_parser.add_argument("--safe-extensions", dest="display_extensions", action="store_true", help="Display extensions that the program considers safe.")
    arg_parser.add_argument(dest="files", nargs='*', default=[], help="Files to process.")
    args = arg_parser.parse_args()

    if (args.display_extensions):
        print(f"Safe extensions: {', '.join(safe_exts)}")
        exit(0)

    if len(args.files) == 0:
        arg_parser.print_help()
        exit(1)

    if args.force_process and not args.dry_run:
        if (input("Warning: Every file will be processed no matter if it is safe or not. Continue? (y/N) ").lower() != 'y'):
            exit(0)

        if not args.backup:
            make_backup = input("Do you want to make a backup just in case? (Y/n) ").lower()
            if (len(make_backup) == 0 or make_backup == 'y'):
                args.backup = True

    if args.backup:
        print("The files will be backed up.")

    for _file in args.files:
        if is_file_safe(_file) or args.force_process:
            if args.backup and not args.dry_run:
                if not backup_file(_file):
                    continue

            remove_ws_from_file(
                _file,
                display_ws_lines=args.display_lines,
                dry_run=args.dry_run
                )

        else:
            print(f"Skipping unsafe file '{_file}'")