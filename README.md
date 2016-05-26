# uzicai deploy tools
a small deploy tools for quick deployment

## Author
Joseph Xu

## Run it

### What do you need to run it
- Python 3.5.1 (Maybe it work for other versions.)
- paramiko
- configparser (3.5.0)
- DateTime (4.1.1)


### How to run it
1. Download the code
1. Modify config.ini
1. Export few file from SVN to local_path for diff_deploy
1. synchronous all porject file with SVN and rebuild it for full_deploy
1. Use ```python diff_deploy.py``` to do diff_deploy
1. Use ```python full_deploy.py``` to do full_deploy

## Warning
- this tools only copy the file to server, all command still need to input


## TO DO
- introduce ssh command into tools

## License
The MIT license.
