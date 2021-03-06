# -*- coding: utf-8 -*-

#########################################################################
# Copyright (C) 2008 by Alex Brandt <alunduil@alunduil.com>             #
#                                                                       #
# This program is free software; you can redistribute it and#or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 2 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, write to the                         #
# Free Software Foundation, Inc.,                                       #
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
#########################################################################

import sys
import optparse
import textwrap
import os

import output
from package import Package

class PClean:
    def __init__(self, argv):
        self._debug = False
        self._verbose = False
        self._quiet = False

        usage = "usage: %prog [options]"
        parser = optparse.OptionParser(usage=usage)
        variables, arguments = self._parseOptions(argv, parser)

        self._quiet = variables.quiet
        self._debug = variables.debug
        # If we have debugging turned on we should also have verbose.
        if self._debug: self._verbose = True
        else: self._verbose = variables.verbose
        # If we have verbose we shouldn't be quiet.
        if self._verbose: self._quiet = False

        # Other option handling ...
        self._destructive = variables.destructive
        self._reorganize = variables.reorganize
        self._sort = variables.sort
        self._pretend = variables.pretend

    def Run(self):
        """Run the application ...

        We first need to read in all of our package.* files.
        Then we simply write them out with the correct method.
        We pass a flag to check for installed packages.

        """
        files_list = [
            "/etc/portage/package.use",
            "/etc/portage/package.unmask",
            "/etc/portage/package.mask",
            "/etc/portage/package.keywords",
            "/etc/portage/package.license"
            ]
        for name in files_list:
            if not os.access(name, os.F_OK): continue
            file = Package(name, self._destructive, self._sort, self._debug)
            file.open()
            if self._pretend: 
                output.verbose("%s:", name)
                output.verbose(file.__unicode__())
            else: file.write(self._reorganize)
            file.close()

    def _parseOptions(self, argv, parser):
        verbose_help_list = [
            "Sets verbose output."
            ]
        parser.add_option('--verbose', '-v', action='store_true',
            default=False, help=''.join(verbose_help_list))

        debug_help_list = [
            "Sets debugging output (implies verbose output)."
            ]
        parser.add_option('--debug', '-D', action='store_true',
            default=False, help=''.join(debug_help_list))

        quiet_help_list = [
            "Sets output to be a bit quieter.  If either debug or ",
            "verbose are set this option has no effect."
            ]
        parser.add_option('--quiet', '-q', action='store_true',
            default=False, help=''.join(quiet_help_list))

        reorganize_help_list = [
            "Reorganizes the files into a directory structure."
            ]
        parser.add_option('--reorganize', '-r', action='store_true',
            default=False, help=''.join(reorganize_help_list))

        destructive_help_list = [
            "Removes packages that aren't installed on the system anymore."
            ]
        parser.add_option('--destructive', '-d', action='store_true',
            default=False, help=''.join(destructive_help_list))

        sort_help_list = [
            "Sort the packages in alphabetical order."
            ]
        parser.add_option('--sort', '-s', action='store_true',
            default=False, help=''.join(sort_help_list))

        pretend_help_list = [
            "Pretend but don't actually write anything."
            ]
        parser.add_option('--pretend', '-p', action='store_true',
            default=False, help=''.join(pretend_help_list))

        return parser.parse_args()

class PCleanException(Exception):
    def __init__(self, message, *args):
        super(PCleanException, self).__init__(args)
        self._message = message

    def GetMessage(self):
        return self._message

