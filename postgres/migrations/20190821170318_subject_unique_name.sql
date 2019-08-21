-- migrate:up

create or replace function sg_private.subject_unique_name()
returns trigger as $$
declare
  xprev sg_public.subject_version;
begin
  select s.* into xprev
  from sg_public.subject s
  where slugify(s.name) = slugify(new.name)
  and s.entity_id <> new.entity_id;
  if (found) then
    raise exception 'Subject name in use.' using errcode = '5E310F2E';
  end if;
  return new;
end;
$$ language plpgsql;
comment on function sg_private.subject_unique_name()
  is 'Ensure new subject versions have a unique name.';
create trigger insert_subject_version_name
  before insert on sg_public.subject_version
  for each row execute procedure sg_private.subject_unique_name();
comment on trigger insert_subject_version_name on sg_public.subject_version
  is 'Ensure new subject versions have a unique name.';

-- migrate:down

