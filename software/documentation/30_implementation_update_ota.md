# Implementation SW-Update

## States of the filesystem
listFiles = uos.listdir()

- isFilesystemEmpty()
  - len(listFiles) == 0
- isUpdateFinished()
  - 'update_finished' in listFiles

## States of the button

- isButtonPressed():

- isPowerOnBoot():

## Bootup logic

if isButtonPressed() and isPowerOnBoot():
  print 'Button presed. Format'
  formatAndReboot()

if not isUpdateFinished():
  print 'Update was not finished. Format'
  formatAndReboot()

if isFilesystemEmpty:
  print 'Filesystem is empty: Update'
  updateAndReboot()

startApplication()

## Bootup logic for testing

remote: format
copy script
update