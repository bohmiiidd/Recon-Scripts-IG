import os
import gzip
import shutil
import argparse

def decompress_gz_files(directory):
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a directory.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.gz'):
                gz_file_path = os.path.join(root, file)
                decompressed_file_path = os.path.splitext(gz_file_path)[0]

                with gzip.open(gz_file_path, 'rb') as gz_file:
                    with open(decompressed_file_path, 'wb') as decompressed_file:
                        shutil.copyfileobj(gz_file, decompressed_file)

                print(f'Decompressed: {gz_file_path} to {decompressed_file_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decompress .gz files in a directory.')
    parser.add_argument('directory', type=str, help='The directory to search for .gz files.')

    args = parser.parse_args()
    decompress_gz_files(args.directory)
