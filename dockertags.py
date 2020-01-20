import requests
import sys

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

OS_NAME = "linux"

image = sys.argv[1]
tagname = 'latest' if len(sys.argv) < 3 else sys.argv[2]

print(f'Checking existance of image: \'{image}\'...')
response = requests.get(f"https://registry.hub.docker.com/v2/repositories/{image}/")
if (response.status_code >= 400):
    print(f'No image \'{image}\' exists, exitting.')
    sys.exit()

print(f'Determining digest for image: \'{image}:{tagname}\'...')
response = requests.get(f"https://registry.hub.docker.com/v2/repositories/{image}/tags/{tagname}")
data = response.json()
if (response.status_code >= 400 or not 'images' in data):
    print(f'No tag \'{tagname}\' found for image \'{image}\', exitting.')
    sys.exit()
required = None
for i in data['images']:
        if (i['os'] == OS_NAME):
            required = Image(data['name'], i['digest'])

if (required == None):
    print(f'Tag \'{tagname}\' not found in first 100 tags, exitting.')
    sys.exit()

print(f'Searching tags for image \'{required.digest[7:15]}\':')
response = requests.get(f"https://registry.hub.docker.com/v2/repositories/{image}/tags/?page_size=100&page=1")
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