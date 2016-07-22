# -*- coding: utf8 -*-
'''
This script is used to test upload on the sellit server.
'''
import cStringIO
from requests import post, get, Response, codes
import sys
import cv2
from PIL import Image


if __name__ == '__main__' :
    import argparse
    # Define command line arguments
    parser = argparse.ArgumentParser(description='Send a POST request for image classification.')
    parser.add_argument('--image', '-i', type=str,
                       help='path to the image')
    parser.add_argument('--url', type=str, default="http://localhost",
                       help='Url of the server')
    parser.add_argument('--port', type=str, default="53117",
                       help='Port on the server')

    args = parser.parse_args()

    url_availability = args.url + ":" + args.port + "/available"
    url_suggest = args.url + ":" + args.port + "/predict"

    r = get(url_availability)
    if r.status_code != codes.ok:
        print "Service is not available on this url"
        sys.exit()

    im = Image.open(args.image)
    buffer = cStringIO.StringIO()
    im.save(buffer, format='JPEG')
    buffer.seek(0)
    files = {'file': buffer}
    #files = {'file': open(args.image, 'rb')}
    r = post(url_suggest, files=files)


    print 'Response from the server: \n{text}'.format(text=r.text)