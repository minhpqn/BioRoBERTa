"""
Extract PubMed abstract text from xml data
"""
import os
import re
from datetime import datetime
import argparse
import gzip
from lxml import etree


def preprocess(text):
    """Preprocess abstract text
    
    :param text: Abstract text
    :type str
    :return:
    """
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min_length", type=int, default=50, help="Minimum length")
    parser.add_argument("--print_every", type=int, default=50, help="Print status every time steps")
    parser.add_argument("--input_dir", type=str, help="Path to PubMed abstracts")
    parser.add_argument("--output_file", type=str, help="Path to data file")
    args = parser.parse_args()

    start = datetime.now()
    print(args)
    files = [f for f in os.listdir(args.input_dir) if re.search(r"\.xml\.gz$", f)]
    print(f"Number of files: {len(files)}")
    with open(args.output_file, "w") as fo:
        for i, filename in enumerate(files, start=1):
            if i % args.print_every == 0:
                print(f"Processing file...{i}/{len(files)}")
            filepath = os.path.join(args.input_dir, filename)
            try:
                root = etree.parse(filepath).getroot()
                for node in root.xpath("//AbstractText"):
                    if node.text is not None:
                        text = preprocess(node.text)
                        if len(text.split()) >= args.min_length:
                            print(text, file=fo)
            except Exception as e:
                print(e)
                with gzip.open(filepath,'rt') as fi:
                    for line in fi:
                        m = re.search(r'<AbstractText>(.+?)</AbstractText>', line)
                        if m:
                            text = m.group(1)
                            text = preprocess(text)
                            if len(text.split()) >= args.min_length:
                                print(text, file=fo)
                        
    end = datetime.now()
    diff = end - start
    print(f"All abstract texts are extracted for {diff.seconds}s")


if __name__ == "__main__":
    main()
