create or replace procedure ag_delete_participant
(
    ag_login_id_ varchar2,
    participant_name_ varchar2
)
as
begin

    -- Remove the backup log
    delete  ag_survey_answer
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
            
    -- Remove the multiple answers
    delete  ag_survey_multiples
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
            
    -- Remove the participant/survey/consent
    delete  ag_human_survey
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
            
    -- Remove the participant/survey/consent if they are an animal
    delete  ag_animal_survey
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
            
    commit;

end;
