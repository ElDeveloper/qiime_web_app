#!/usr/bin/env python
# File created on 28 Feb 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2009-2010, QIIME Web Analysis"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from enums import ServerConfig
from data_access_connections import data_access_factory

def submit_toggle_study_status_job(user_id, study_id, study_status):
    """Togglee a study status from public to private and viceversa"""

    # Instantiate one copy of data access for this process
    data_access = data_access_factory(ServerConfig.data_access_type)

    # Set up the parameters
    params = []
    params.append('StudyID=%s' % str(study_id))
    params.append('StudyStatus=%s' % str(study_status))
    job_input = '!!'.join(params)

    # Submit the job
    job_id = data_access.createTorqueJob('ToggleStudyStatusHandler', job_input,
        user_id, study_id)
    # Make sure a legit job_id was created, ese inform that there was a problem
    if job_id < 0:
        raise Exception('There was an error creating the job. Please contact '
            'the system administrator.')
