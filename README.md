# dockertags
A tool that allows you to show all tags that a specific image identified by one of those tags has.

A typical scenario for this is to find out what version tags has the 'latest' container.

Example output:
```bash
$ python dockertags.py gitlab/gitlab-ce:latest
Checking existance of image: 'gitlab/gitlab-ce'...
Determining digest for image: 'gitlab/gitlab-ce:latest'...
Searching tags for image '2c7d26f5':
 + gitlab/gitlab-ce:latest
 + gitlab/gitlab-ce:rc
 + gitlab/gitlab-ce:12.6.4-ce.0
Listed 3 tag(s).
```
