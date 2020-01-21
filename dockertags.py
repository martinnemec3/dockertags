import requests
import sys
import argparse

OS_NAME = "linux"
DEFAULT_TAG = "latest"
OFFICIAL_IMAGE_PATH = "library/"

class Image:
    def __init__(self, name, digest):
        self.digest = digest
        self.name = name
    def __eq__(self, other): 
        if not isinstance(other, Image):
            return False
        return self.digest == other.digest and self.name == other.name
    def compareDigests(self, other):
        if not isinstance(other, Image):
            return False
        return self.digest == other.digest

def parseArguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('image', metavar="image[:tag]", help="name of the image to query (if tag is included, it will be used for querying)")
    parser.add_argument('-c', '--browse-count', metavar='COUNT', type=int, default=100, help="count of tags to browse in the target repository (default is 100)")
    return parser.parse_args()

def buildBaseUrl(image):
    return f"https://registry.hub.docker.com/v2/repositories/{image if '/' in image else f'{OFFICIAL_IMAGE_PATH}{image}'}/"

def checkImageExistance(image, baseUrl):
    print(f'Checking existance of image: \'{image}\'...')
    response = requests.get(baseUrl)
    if (response.status_code >= 400):
        print(f'No image \'{image}\' exists, exitting.')
        sys.exit()

def determineRequiredImage(image, tagname, baseUrl):
    print(f'Determining digest for image: \'{image}:{tagname}\'...')
    response = requests.get(f"{baseUrl}tags/{tagname}")
    data = response.json()
    if (response.status_code >= 400 or not 'images' in data):
        print(f'No tag \'{tagname}\' found for image \'{image}\', exitting.')
        sys.exit()
    for i in data['images']:
            if (i['os'] == OS_NAME):
                return Image(data['name'], i['digest'])
    print(f'Tag \'{tagname}\' not found in latest 100 tags, exitting.')
    sys.exit()

def listTags(image, baseUrl, required):
    print(f'Searching tags for image \'{required.digest[7:15]}\':')
    response = requests.get(f"{baseUrl}tags/?page_size=100&page=1")
    data = response.json()
    count = 0
    for r in data['results']:
        for i in r['images']:
            if (i['os'] == OS_NAME):
                current = Image(r['name'], i['digest'])
                if (current.compareDigests(required)):
                    count += 1
                    print(f' + {image}:{current.name}')
    print(f'Listed {count} tag(s).')

def main():
    args = parseArguments()
    image = args.image.split(':')[0]
    tagname = DEFAULT_TAG if not ':' in args.image else args.image.split(':')[1]
    baseUrl = buildBaseUrl(image)

    checkImageExistance(image, baseUrl)
    required = determineRequiredImage(image, tagname, baseUrl)
    listTags(image, baseUrl, required)

main()