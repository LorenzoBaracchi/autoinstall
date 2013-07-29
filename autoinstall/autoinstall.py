import argparse
import subprocess as sub
import sys
import jsonpickle
from termcolor import colored

quietmode = ""


def createarguments():
  """
  Function to create arguments that can be passed to the main function
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', help="File with the list of programs to install", required=True)
  parser.add_argument('-q', '--quiet', help='Quiet output', action="store_true")
  return parser

def install_aptfast():
  """
  Installing apt-fast to speed-up installation process
  """
  global quietmode
  retcode = sub.call("add-apt-repository" + " -y ppa:apt-fast/stable" + quietmode, shell=True)
  if retcode==0:
    retcode = sub.call("apt-get" + " update" + quietmode, shell=True)
  if retcode==0:
    retcode = sub.call("apt-get" + " install -y apt-fast" + quietmode, shell=True)
  return True if retcode==0 else False

def read_json(filename):
  """
  Read the file json with the list of packaes to install
  """
  f = open(filename, 'r')
  s = f.read()
  return jsonpickle.decode(s)

def divide_packages(packages):
  """
  Divide packages in standards and repositories packages
  """
  stds = []
  repos = []
  for p in packages:
    if (not 'repository' in p):
      stds = stds + [p]
    elif (p['repository']==None or p['repository']==''):
      stds = stds + [p]
    else:
      repos = repos +[p]
  return stds, repos

def install_standards(stds):
  """
  Install standard packages
  """
  global quietmode
  packs = ""
  for s in stds:
    packs = packs + " " + s['name']
  retcode = sub.call("apt-fast" + " install -y" + packs + quietmode, shell=True)
  return True if retcode==0 else False

def add_repositories(repos):
  """
  Add external repositories
  """
  global quietmode
  for r in repos:
    retcode = sub.call("add-apt-repository" + " -y " + r['repository'] + quietmode, shell=True)
    if retcode==0:
      r['added'] = True
    else:
      print colored("ERROR: not possible to add repository for: " + r['name'], "red")
  sub.call("apt-get" + " update" + quietmode, shell=True)
  return repos

def install_nonstandards(repos):
  """
  Install non-standard packages
  """
  global quietmode
  packs = ""
  for r in repos:
    if 'added' in r:
      packs = packs + " " + r['name']
      sub.call("apt-fast" + " install -y" + packs + quietmode, shell=True)

def main():
  global quietmode
  parser = createarguments()
  args = vars(parser.parse_args())
  if args['quiet']:
    quietmode = " > /dev/null"
  #install apt-fast
  print colored("Installing apt-fast", 'blue')
  r = install_aptfast()
  if r:
    print("apt-fast installed")
    #read file
    packages = read_json(args['input'])
    #install packages
    standards, repos = divide_packages(packages)
    print colored("Installing packages...", 'blue')
    install_standards(standards)
    print colored("standard packages installed.", 'blue')
    print colored("Adding repositories...", 'blue')
    repos = add_repositories(repos)
    print colored("repositories added.", 'blue')
    print colored("Installing packages from repositories...", 'blue')
    install_nonstandards(repos)
    print colored("Finished installing.", 'blue')
  else:
    print colored("ERROR: not possible to install apt-fast", 'red')
    sys.exit(1)


if __name__ == "__main__":
  main()
