#!/usr/bin/python
"""Set TVheadend Default Username and Password
  Use dpkg-reconfigure instead of arguments
"""

import sys, os, os.path, time, string, dialog

from executil import system         

def informuser(d):
        d.msgbox("Executing dpkg-reconfigure for tvheadend", title="Setup TVheadend", no_shadow=False)

def dpkgconfigure():
    d = dialog.Dialog(dialog="dialog")
    d.add_persistent_args(["--backtitle", "TurnKey Linux - First boot configuration"])
    informuser(d)
    system('dpkg-reconfigure tvheadend')
    
def main():
    try:
        dpkgconfigure()
    except dialog.error, exc_instance:
        sys.stderr.write("Error:\n\n%s\n" % exc_instance.complete_message())
        sys.exit(1)
        
    sys.exit(0)


if __name__ == "__main__": main()
