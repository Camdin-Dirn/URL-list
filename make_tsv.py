import os
import hashlib
import base64

PREFIX = 'https://raw.githubusercontent.com/cd-public/books/main/' # DONT scrape Gutenberg
BK_DIR = 'c:/Users/camdi/OneDrive/Desktop/Data 599 cloud/books/'

def compute_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    md5_base64 = base64.b64encode(hash_md5.digest()).decode('utf-8')
    return md5_base64

def create_tsv(directory, prefix, output_file):
    with open(output_file, 'w') as tsv_file:
        tsv_file.write("TsvHttpData-1.0\n")
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                md5_checksum = compute_md5(file_path)
                
                # Construct the URL
                relative_path = os.path.relpath(file_path, directory)
                url = os.path.join(prefix, relative_path).replace("\\", "/")
                
                # Write to the TSV file
                tsv_file.write(f"{url}\t{file_size}\t{md5_checksum}\n")

create_tsv(BK_DIR, PREFIX, 'books.tsv')
