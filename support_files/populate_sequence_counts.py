from data_access_connections import data_access_factory
from enums import ServerConfig

data_access = data_access_factory(ServerConfig.data_access_type)
con = data_access.getMetadataDatabaseConnection()
study_ids = []

query_string = """
select  distinct s.study_id 
from    study s 
        inner join sample sa 
        on s.study_id = sa.study_id 
        inner join sequence_prep sp 
        on sa.sample_id = sp.sample_id 
where   exists
        (
            select  1
            from    sequence_prep sp2
            where   sp2.num_sequences is null
                    and sp2.sequence_prep_id = sp.sequence_prep_id
        )
order by study_id
"""

results = data_access.dynamicMetadataSelect(query_string)
print '---------------------- Studies List ----------------------'
for row in results:
    study_id = row[0]
    print 'study_id: {0}'.format(str(study_id))
    study_ids.append(row[0])

query_string = """
select  substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) as sequence_prep_id, 
        count(substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1)) as cnt 
from    sff.split_library_read_map slrm 
        inner join sff.analysis a 
        on slrm.split_library_run_id = a.split_library_run_id 
        inner join qiime_metadata.sequence_prep sp 
        on sp.sequence_prep_id = substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) 
where   a.study_id = {0} 
        and sp.num_sequences is null
group by substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) 
"""

print '---------------------- Seqs per Prep ID ----------------------'
for study_id in study_ids:
    seq_prep_counts = []
    run_string = query_string.format(study_id)
    #print run_string
    results = data_access.dynamicMetadataSelect(query_string.format(study_id))
    for sequence_prep_id, seq_count in results:
        seq_prep_counts.append((sequence_prep_id, seq_count))
        
        print '{0}: {1}'.format(sequence_prep_id, seq_count)
        
        query_string_2 = """
        update  sequence_prep 
        set     num_sequences = {0} 
        where   sequence_prep_id = {1} 
        """

        for sequence_prep_id, seq_count in seq_prep_counts:
            run_string = query_string_2.format(seq_count, sequence_prep_id)
            #print run_string
            con.cursor().execute(run_string)
            con.cursor().execute('commit')

# end
