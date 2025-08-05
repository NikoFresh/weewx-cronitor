#
#    Copyright (c) 2020-2023 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
""" Installer for MTTQSubscribe driver and service. """

from io import StringIO

import configobj

from weecfg.extension import ExtensionInstaller

VERSION = '0.2.0'

CRONITOR_CONFIG = """
[StdReport]
    [[Cronitor]]
        # Turn the service on and off.
        # Default is: true
        # Only used by the service.
        enable = false
        
        skin = cronitor
        
        # The host to 'ping'
        # Default is cronitor.link/p
        # host = cronitor.link/p 

        # The name for the tracker
        # Default is Weewx
        # device_name = Weewx
        
        # The http request timeout
        # The default is 10
        # timeout = 10
        
        # The Cronitor api_key
        api_key = REPLACE_ME
"""


def loader():
    """ Load and return the extension installer. """
    return CronitorInstaller()

class CronitorInstaller(ExtensionInstaller):
    """ The extension installer. """
    def __init__(self):
        install_dict = {
            'version': VERSION,
            'name': 'Cronitor',
            'description': 'Monitor WeeWX using Cronitor.io',
            'author': "Rich Bell",
            'author_email': "bellrichm@gmail.com",
            'files': [
                ('bin/user', ['bin/user/cronitor.py']),
                ('skins/cronitor',['skins/cronitor/skin.conf']),             
            ]
        }

        cronitor_dict = configobj.ConfigObj(CRONITOR_CONFIG)
        install_dict['config'] = cronitor_dict
        install_dict['prep_services'] = 'user.cronitor.Cronitor'

        super().__init__(install_dict)
