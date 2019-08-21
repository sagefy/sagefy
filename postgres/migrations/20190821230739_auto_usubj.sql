-- migrate:up

create or replace function sg_private.subject_auto_user_subject()
returns trigger as $$
begin
  insert into sg_public.user_subject (subject_id)
  values (new.entity_id)
  on conflict do nothing;
  return new;
end;
$$ language plpgsql;
comment on function sg_private.subject_auto_user_subject()
  is 'Whenever I make a new subject version, add me as a learner.';
create trigger insert_subject_version_auto_user_subject
  after insert on sg_public.subject_version
  for each row execute procedure sg_private.subject_auto_user_subject();
comment on trigger insert_subject_version_auto_user_subject
  on sg_public.subject_version
  is 'Whenever I make a new subject version, add me as a learner.';

-- migrate:down

