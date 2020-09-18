"""
Download PubMed abstract files from ftp server
PubMed Abstract 1: ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/
PubMed Abstract 2: ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/
"""
import os
import sys
import enum
import re
import time
import argparse
import ftplib
from ftplib import FTP
from datetime import datetime
from logger_utils import get_logger


# Enum for size units
class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes, unit):
    """ Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


def get_file_size(file_name, size_type=SIZE_UNIT.BYTES):
    """ Get file in size in given unit like KB, MB or GB"""
    size = os.path.getsize(file_name)
    return convert_unit(size, size_type)


parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True, help="FTP link")
parser.add_argument("--timeout", type=float, default=60, help="Time out (seconds)")
parser.add_argument("--skip_existing", action="store_true", help="Whether to skip existing files")
parser.add_argument("--output_dir", type=str, default="./data", help="Path to output directory")
args = parser.parse_args()



interval = 0.05
MIN_SIZE = 10

# Get the host name
m = re.match(r'ftp://([^/]+?)/(pubmed/[^/]+)', args.url)
host = None
domain = None
if m:
    host = m.group(1)
    path = m.group(2)
else:
    raise ValueError("Invalid URL")

destination = os.path.join(args.output_dir, path)
os.makedirs(destination, exist_ok=True)

LOG_FILE = os.path.join(destination, "log.txt")
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

logger = get_logger(LOG_FILE, __name__)

logger.info(args)
logger.info(f"Download files from: {args.url}")
logger.info(f"Host: {host}")
logger.info(f"Directory: {path}")

start = datetime.now()
ftp = FTP(host, timeout=args.timeout)
ftp.login()

try:
    ftp.cwd(path)
    logger.info("FPT loggin and change path sucessully!")
except ftplib.error_perm as e:
    logger.error("Could not change to " + path)
    logger.error(e)
    sys.exit("Ending Application")

files = ftp.nlst()

n_files = len(files)
logger.info(f"Number of files: {n_files}")
gz_files = [f for f in files if re.search(r'\.gz$', f)]
n_gz_files = len(gz_files)
logger.info(f"Number of tgz files: {n_gz_files}")

i = 0
for file in files:
    time.sleep(interval)
    try:
        target_file = os.path.join(destination, file)
        if args.skip_existing and re.search(r'\.gz$', file) and os.path.isfile(target_file) and \
                get_file_size(target_file, SIZE_UNIT.MB) > MIN_SIZE:
            logger.info(f"Skipped file...{file}")
        else:
            if re.search(r'\.gz$', file):
                i += 1
                logger.info(f"Downloading...{file} ({i}/{n_gz_files} (.gz files))")
            else:
                logger.info("Downloading..." + file)
            ftp.retrbinary("RETR " + file, open(target_file, "wb").write)
    except ftplib.error_perm as e:
        logger.error("File could not be downloaded " + file)
        logger.info(e)

ftp.close()

end = datetime.now()
diff = end - start
logger.info(f"All files downloaded for {diff.seconds}s")

