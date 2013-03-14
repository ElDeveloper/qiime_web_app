create or replace procedure ag_get_participant_samples
(
    ag_login_id_ raw,
    participant_name_ varchar2,
    results_ in out types.ref_cursor
)
as
begin

    open results_ for
        select  akb.barcode, akb.site_sampled, akb.sample_date, akb.hour, akb.minute, akb.meridian
        from    ag_kit_barcodes akb 
                inner join ag_kit ak 
                on akb.ag_kit_id = ak.ag_kit_id 
        where   akb.site_sampled is not null
                and ak.ag_login_id = ag_login_id_
                and akb.participant_name = participant_name_;
                
end;
