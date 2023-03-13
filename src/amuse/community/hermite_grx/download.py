#!/usr/bin/env python

import subprocess
import os
import sys
import datetime
import urllib.request
import urllib.parse
import urllib.error
import glob
from optparse import OptionParser
import pathlib

class GetCodeFromHttp(object):
    url_template = "https://github.com/amusecode/Hermite_GRX/archive/refs/tags/{version}.zip"
    filename_template = "{version}.zip"
    version = ""

    def get_code_directory(self):
        return pathlib.Path(__file__).parent.absolute()

    def get_download_directory(self):
        return self.get_code_directory() / "downloads"
    
    def get_archive_directory(self):
        return self.get_code_directory() / "archive"

    def unpack_downloaded_file(self, filename):
        print(f"unpacking {filename}")
        arguments = ['unzip', "-o"]
        arguments.append(filename)
        subprocess.call(
            arguments,
            cwd=self.get_download_directory()
        )
        
        files_to_move = list((self.get_download_directory() / f"Hermite_GRX-{self.version.replace('v', '')}").glob("*"))
        # Move all the current files but this file to an archive
        for file_ in files_to_move:
            file_.rename(self.get_code_directory() / file_.name)
        print("done")
        
    def check_and_move_old_code(self):
        # Get all the files in the currenty directory.
        files = [pathlib.Path(p) for p in glob.glob(f"{self.get_code_directory()}/*")]
        print("before cleanup: ", files)
        for file_ in files:
            # Filter out any source directory
            if file_.stem.startswith("download") or file_.stem.startswith("archive"):
                files.remove(file_)
            # Filter out the download.py file
            elif file_.name == "download.py":
                files.remove(file_)
            else:
                continue            
        # Create a backup with the current time.
        if not self.get_archive_directory().exists():
            self.get_archive_directory().mkdir(exist_ok=True)
        backup_target = self.get_archive_directory() / f"backup_{datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S')}"
        backup_target.mkdir()
        for f in files:
            f.rename(backup_target / f.name)
        

    def start(self):
        self.check_and_move_old_code()
        self.get_download_directory().mkdir(exist_ok=True)
        url = self.url_template.format(version=self.version)
        filename = self.filename_template.format(version=self.version)
        filepath = self.get_download_directory() / filename
        if not filepath.exists():
            print(f"downloading version {self.version} from {url} to {filepath}")
            urllib.request.urlretrieve(url, filepath)
        else:
            print(f"The zip for {filename} is already present, not downloading")
        print("downloading finished")
        self.unpack_downloaded_file(filename)


def main(version=''):
    instance = GetCodeFromHttp()
    instance.version = version
    instance.start()


def new_option_parser():
    result = OptionParser()
    result.add_option(
        "--version",
        default='v0.1.0',
        dest="version",
        help="version number to download",
        type="string"
    )
    return result


if __name__ == "__main__":
    options, arguments = new_option_parser().parse_args()
    main(**options.__dict__)
