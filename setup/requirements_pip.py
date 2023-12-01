import subprocess
import sys

packages_to_install = [ 'antlr4-tools', 'antlr4-python-runtime' ]
install_all         = False

if len(sys.argv) >= 2:
  if 'install_all' in sys.argv:
    install_all = True    
    
print("Installing " + str(len(packages_to_install)) + " packages")

for idx, val in enumerate(packages_to_install):
  print()
  print()

  do_install = install_all

  while not do_install:
    print(str(idx+1) + "/" + str(len(packages_to_install)) + " pip install " + val)
    print("[Y/n] > ", end='')
  
    choice = input().lower()
    if choice in [ 'n' ]:
      break
    if choice in [ '', 'y' ]:
      do_install = True
      break
  
  if do_install:
    subprocess.check_call([sys.executable, "-m", "pip", "install", val])
  
print()
print()
print("Done")
input()