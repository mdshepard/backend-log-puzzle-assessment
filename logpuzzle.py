#!/usr/bin/env python2
"""
Logpuzzle exercise
Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    puz_url_lst = []
    # open filename as an object that we can read
    with open(filename) as file:
        if 'place' in filename:
            return sorted(set(puz_url_lst), key=lambda x: x[(x.rfind('-')+1):])
        for line in file:
            match = re.search('puzzle', line)
            if match:
                url = re.search(r'\S+puzzle+\S+', line)
                puz_url_lst.append(url.group())
    # eliminate duplicate img urls
    puz_lst_set = set(puz_url_lst)
    # using sorted and lambda function
    sorted_list = sorted(list(puz_lst_set), key=lambda x: x[-8:-4])
    return sorted_list


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # setting up HTML template
    html_head = "<html><head><body>"
    new_html = ""
    html_endhead = "</body></head></html>"
    # if dir doesn't exist
    if os.path.isdir(dest_dir):
        return
        os.mkdir(dest_dir)
        os.chdir(dest_dir)
    # using enumerate to name img files by number as mentioned in docstring
    for i, image_url in enumerate(img_urls):
        img_num = str(i)
        urllib.urlretrieve(
            "http://code.google.com/{0}{1}/img{2}.jpeg".format(
                image_url, dest_dir, img_num)
            )
        new_html += """<img src = './{0}/img{1}.jpeg' />""".format(
            dest_dir, img_num
            )
        result_html = html_head + new_html + html_endhead
    f = open('puzzle.html', 'w')
    f.write(result_html)
    f.close()


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir', help='destination dir for img urls')
    parser.add_argument('logfile', help='apache logfile to extract urls from')
    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    parsed_args = parser.parse_args(args)
    img_urls = read_urls(parsed_args.logfile)
    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
