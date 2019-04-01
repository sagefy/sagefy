-- migrate:up

-- Nota bene that this is intended to be _temporary_.
create or replace function sg_private.insert_subject_version_status()
returns trigger as $$
begin
  new.status = 'accepted'::sg_public.entity_status;
  return new;
end;
$$ language plpgsql strict security definer;
comment on function sg_private.insert_subject_version_status()
  is 'When inserting a new subject, '
     'automatically set the status to accepted.';

create trigger insert_subject_version_status
  before insert on sg_public.subject_version
  for each row execute procedure sg_private.insert_subject_version_status();
comment on trigger insert_subject_version_status
  on sg_public.subject_version
  is 'When inserting a new subject, '
     'automatically set the status to accepted.';

-- migrate:down

