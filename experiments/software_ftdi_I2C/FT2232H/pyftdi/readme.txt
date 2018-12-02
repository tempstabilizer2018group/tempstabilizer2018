Installation
------------

==> Versuch vermutlich OHNE ERFOLG!


ACHTUNG:
http://eblot.github.io/pyftdi/
As adminstrator
$ cd "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts"
$ pip install libusb

Collecting libusb
  Downloading https://files.pythonhosted.org/packages/bb/3a/d72fca150c04149440fe4f8c62255483f756d984e265ee152772466001fd/libusb-1.0.22b1.zip (252kB)
    100% || 256kB 2.3MB/s
Requirement already satisfied: setuptools>=39.0.1 in c:\program files (x86)\microsoft visual studio\shared\python36_64\lib\site-packages (from libusb) (39.0.1)
Collecting cffi>=1.11.5 (from libusb)
  Downloading https://files.pythonhosted.org/packages/2f/85/a9184548ad4261916d08a50d9e272bf6f93c54f3735878fbfc9335efd94b/cffi-1.11.5-cp36-cp36m-win_amd64.whl (166kB)
    100% || 174kB 2.3MB/s
Collecting pycparser (from cffi>=1.11.5->libusb)
  Downloading https://files.pythonhosted.org/packages/8c/2d/aad7f16146f4197a11f8e91fb81df177adcc2073d36a17b1491fd09df6ed/pycparser-2.18.tar.gz (245kB)
    100% || 256kB 3.4MB/s
Installing collected packages: pycparser, cffi, libusb
  Running setup.py install for pycparser ... done
  Running setup.py install for libusb ... done
Successfully installed cffi-1.11.5 libusb-1.0.22b1 pycparser-2.18

$ pip install pyftdi

Collecting pyftdi
  Downloading https://files.pythonhosted.org/packages/83/cb/e80219e9ba796630e135268be7ee0bd64d3065ad1b0bcb18b4227a5886a4/pyftdi-0.29.0.tar.gz (52kB)
    100% || 61kB 1.2MB/s
Collecting pyusb>=1.0.0 (from pyftdi)
  Downloading https://files.pythonhosted.org/packages/5f/34/2095e821c01225377dda4ebdbd53d8316d6abb243c9bee43d3888fa91dd6/pyusb-1.0.2.tar.gz (54kB)
    100% || 61kB 1.7MB/s
Collecting pyserial>=3.0 (from pyftdi)
  Downloading https://files.pythonhosted.org/packages/0d/e4/2a744dd9e3be04a0c0907414e2a01a7c88bb3915cbe3c8cc06e209f59c30/pyserial-3.4-py2.py3-none-any.whl (193kB)
    100% || 194kB 2.9MB/s
Installing collected packages: pyusb, pyserial, pyftdi
  Running setup.py install for pyusb ... done
  Running setup.py install for pyftdi ... done
Successfully installed pyftdi-0.29.0 pyserial-3.4 pyusb-1.0.2

