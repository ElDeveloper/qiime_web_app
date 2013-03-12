#!/usr/bin/env python
# File created on 13 Feb 2013
from __future__ import division

__author__ = "Yoshiki Vazquez-Baeaa"
__copyright__ = "Copyright 2009-2010, QIIME Web Analysis"
__credits__ = ["Yoshiki Vazquez-Baeza"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Yoshiki Vazquez-Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from qiime.util import (parse_command_line_parameters, make_option,
    qiime_system_call)

script_info = {}
script_info['brief_description'] = "Toggle the state of a study between " +\
    "private and public."
script_info['script_description'] = "Move the files and entries in the system"+\
    " from a private to a public state and vice-versa."
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-s','--study_id',help='Unique study identifier'),
    make_option('--study_status', type="choice", action='append', choices=[
        'public', 'private'], help='current status of the study [default: '
        '%default]', default=['public', 'private']),
]
script_info['optional_options'] = []
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    study_id = int(opts.study_id)
    study_status = opts.study_status

    # use ssh to move the files from one location to the other
    if study_status == 'public':
        remote_command = ('mv /qiimedb_studies/private/'+\
            'study_%d_split_library_seqs_and_mapping.tgz /qiimedb_studies/'+\
            'public/') % study_id
    elif study_status == 'private':
        remote_command = ('mv /qiimedb_studies/public/'+\
        'study_%d_split_library_seqs_and_mapping.tgz /qiimedb_studies/'+\
        'private/') % study_id

    # if the command call returns something to stderr cmd_e will catch that
    cmd = 'ssh wwwuser@thebeast.colorado.edu "%s"' % remote_command
    cmd_o, cmd_e, cmd_r = qiime_system_call(cmd)

    if cmd_e:
        opts.error('Could not move the files from location %s' % study_status)

    # things to change the status of the entries in the database should go here

if __name__ == "__main__":
    main()
