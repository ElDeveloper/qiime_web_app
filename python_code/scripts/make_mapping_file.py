#!/usr/bin/env python
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from os import makedirs
from qiime.util import load_qiime_config
from generate_mapping import write_mapping
from submit_job_to_qiime import submitQiimeJob

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Run write_mapping in QIIME-DB python_code"
script_info['script_description'] = """\
This script takes input from the DB, then associates the appropriate files and
parameters to the write_mapping_file function from the QIIME-DB"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -f /files/on/server/ -w http://www.microbio.me/files/ -o /files/on/server/otu_table.biom -q /files/on/server/query.txt -p meta_analysis -u 0 -m 0 -b /files/on/server/params.txt -r 0 -j 0 -s 1  -t /files/on/server/taxonomy.txt -g /files/on/server/tree.tre -d 1/1/2012")]
script_info['output_description']= "The output is generated and can be downloaded from the QIIME-DB website"
script_info['required_options'] = [\
    make_option('-f','--fs_fp',help='this is the location of the actual files on the linux box'),\
    make_option('-w','--web_fp',help='this is the location that the webserver can find the files'),\
    make_option('-q','--query',help='this is the path to the users query'),\
    make_option('-p','--fname_prefix',help='this is the prefix to append to the users files'),\
    make_option('-u','--user_id',help='this is the user id'),\
    make_option('-m','--meta_id',help='this is the meta analysis id'),\
    make_option('-b','--params_path',help='this is the parameters file used'),\
    make_option('-r','--bdiv_rarefied_at',help='this is the rarefaction number'),\
    make_option('-j','--otutable_rarefied_at',help='this is the rarefaction number for the OTU table'),\
    make_option('-s','--jobs_to_start',help='these are the jobs that should be started'),\
    make_option('-t','--taxonomy',help='this is the taxonomy to use'),\
    make_option('-g','--tree_fp',help='this is the gg tree to use'),\
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
       
    # get database connection
    try:
        from data_access_connections import data_access_factory
        from enums import ServerConfig
        import cx_Oracle
        data_access = data_access_factory(ServerConfig.data_access_type)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
    
    # get the query from the website
    query_dict=eval(open(opts.query).read())
    table_col_value={}
    for i in query_dict:
        if i not in ['otu_table','mapping_file','pcoa_plot']:
            table_col_value[i]=query_dict[i]
            
    fs_fp=opts.fs_fp
    web_fp=opts.web_fp
    file_name_prefix=opts.fname_prefix
    user_id=int(opts.user_id)
    meta_id=int(opts.meta_id)
    params_path=opts.params_path
    bdiv_rarefied_at=int(opts.bdiv_rarefied_at)
    otutable_rarefied_at=int(opts.otutable_rarefied_at)
    jobs_to_start=opts.jobs_to_start
    taxonomy=opts.taxonomy
    tree_fp=opts.tree_fp
    write_mapping(data_access, table_col_value, fs_fp, web_fp, 
                                file_name_prefix,user_id,meta_id,params_path,
                                bdiv_rarefied_at,otutable_rarefied_at,
                                jobs_to_start,taxonomy,tree_fp)

if __name__ == "__main__":
    main()
