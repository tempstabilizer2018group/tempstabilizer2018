# -*- coding: utf-8 -*-
import socket

strInfluxDbDatabase = 'tempstabilizer2018'
strInfluxDbHost = 'www.tempstabilizer2018.org'
strInfluxDbPort = 8086
strInfluxDbTagOrigin = 'tempstabilizer2018'
strInfluxDbNameOrigin = 'origin'

strInfluxDbSummaryPrefix = 'sy_'

# After changing this file you might need to restart apache!
# sudo systemctl restart apache2

# True: Don't connect to www.github.com and get the files locally
# False: Get files from www.github.com
bGithubPullLocal = False
if socket.gethostname() == 'raspberrypi':
  # On the raspberry pi, we usually want to update the local files
  bGithubPullLocal = True

# True: If a update-tar-file is already in the cache: Use it
#   Use this option on a productive system or not at all...
# False: Create a update-tar-file even and override a file which is already in the cache.
#   Use this option when developing locally on the software.
bCacheTarFiles = True

if bGithubPullLocal:
  # If we pull local, we also want the locally changed files be in the next download.
  # Therfore: No cache!
  bCacheTarFiles = False

def factoryGitHubPull():
  '''
    There are different implementation of GitHubPull.
    Specially pulling from the local filesystem or from github.
    This will return an puller and assign the mac-addresse.
  '''
  import python3_github_pull

  if bGithubPullLocal:
    return python3_github_pull.GitHubPullLocal()

  # return python3_github_pull.GitHubApiPull()
  return python3_github_pull.GitHubPublicPull()
