# -*- coding: utf-8 -*-

strInfluxDbDatabase = 'tempstabilizer2018'
strInfluxDbHost = 'www.tempstabilizer2018.org'
strInfluxDbPort = 8086

# After changing this file you might need to restart apache!
# sudo systemctl restart apache2

# if set to True, instead of getting the files from github, the will be lookedup locally
bGithubPullLocal = True

# Cache tar-files (the software-updates) to make downloads faster
bCacheTarFiles = False

if bGithubPullLocal:
  # If we pull local, we also want the locally changed files be in the next download.
  # Therfore: No cache!
  bCacheTarFiles = False

strMacUnderTest = '840D8E1BC40C'

def factoryGitHubPull(strMac):
  '''
    There are different implementation of GitHubPull.
    Specially pulling from the local filesystem or from github.
    This will return an puller and assign the mac-addresse.
  '''
  def factory():
    import python3_github_pull
    if bGithubPullLocal:
      return python3_github_pull.GitHubPullLocal()

    if strMac == strMacUnderTest:
      return python3_github_pull.GitHubPullLocal()

    # return python3_github_pull.GitHubApiPull()
    return python3_github_pull.GitHubPublicPull()

  p = factory()
  p.setMac(strMac)

  return p
