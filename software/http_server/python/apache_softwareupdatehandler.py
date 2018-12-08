from mod_python import apache

from urlparse import parse_qs
import time
import platform
import os.path
import python3_github_pull

def handler(req):
  dictArgs = parse_qs(req.args)

  def getArg(strTag):
    listArg = dictArgs.get(strTag, None)
    if listArg == None:
      req.content_type = "text/html"
      req.write("<p>args: '%s'</p>" % req.args)
      req.write("<p>ERROR: Required argument missing='%s'!</p>" % strTag)
      # raise(apache.SERVER_RETURN(apache.HTTP_BAD_REQUEST))
      raise(apache.SERVER_RETURN(apache.DONE))
    if len(listArg) == 0:
      req.content_type = "text/html"
      req.write("<p>args: '%s'</p>" % req.args)
      req.write("<p>ERROR: Parameter for argument '%s' missing!</p>" % strTag)
      raise(apache.SERVER_RETURN(apache.DONE))
    return listArg[0]

  # http://localhost/softwareupdate/?mac=3C:71:BF:0F:97:A4&version=none
  strMac = getArg('mac')
  strVersion = getArg('version')


  # req.write("<p>python version: '%s'</p>" % platform.python_version())
  # req.write("<p>method: '%s'<p>" % req.method)
  # req.write("<p>---</p>")

  p = python3_github_pull.GitHubPullLocal()
  strVersionGit = p.setMac(strMac)

  if req.uri.endswith('/versioncheck.download'):
    req.content_type = "text/html"
    req.write(strVersionGit)
    # if strVersion == strVersionGit:
    #   # No update required
    #   return apache.HTTP_NO_CONTENT
    return apache.OK

  req.content_type = "application/octet-stream"
  
  strFilenameFull = p.getTar()
  if strFilenameFull == None:
    # Unknown Mac/Node
    return apache.HTTP_NO_CONTENT

  req.sendfile(strFilenameFull)

  return apache.OK

