#!/usr/bin/python
"""Set TVheadend Default Password for web gui
Option:
    --pass=     unless provided, will ask interactively
"""

import sys
import getopt
import bcrypt

from executil import system
from dialog_wrapper import Dialog

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "TVheadend Password",
            "Enter Web GUI Password.")
        
    """Set Package Configuration"""
    system('echo "tvheadend tvheadend/admin_username string admin" | debconf-set-selections')
    system('echo "tvheadend tvheadend/admin_password password %s" | debconf-set-selections' % password)
    """Change Default Listening Port"""
    system('sed', '-i', "s/TVH_HTTP_PORT=.*/TVH_HTTP_PORT=\"9980\"/g", '/etc/default/tvheadend')
    """Configure Package"""
    system('DEBIAN_FRONTEND=noninteractive', 'dpkg-reconfigure', 'tvheadend')
    """Clear Package Configuration"""
    system('echo purge | debconf-communicate tvheadend')
    """Restart nginx"""
    system('service', 'nginx', 'restart')

if __name__ == "__main__":
    main()
