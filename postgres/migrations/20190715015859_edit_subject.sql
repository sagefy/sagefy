-- migrate:up

create or replace function sg_public.update_subject(
  entity_id uuid,
  name text,
  tags text[],
  body text,
  parent uuid[],
  before uuid[]
)
returns sg_public.subject_version as $$
  declare
    xprevious sg_public.subject;
    xversion_id uuid;
    xsubject_version sg_public.subject_version;
  begin
    select * into xprevious
    from sg_public.subject_by_entity_id(entity_id);
    if (xprevious is null) then
      raise exception 'No previous version found.' using errcode = 'B7615F09';
    end if;
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'subject');
    insert into sg_public.subject_version
    (version_id, previous_version_id, entity_id, language, name, tags, body)
    values (xversion_id, xprevious.version_id, entity_id, xprevious.language, name, tags, body)
    returning * into xsubject_version;
    insert into sg_public.subject_version_parent_child
    (child_version_id, parent_entity_id)
    select xversion_id, unnest(parent);
    insert into sg_public.subject_version_before_after
    (after_version_id, before_entity_id)
    select xversion_id, unnest(before);
    return xsubject_version;
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.update_subject(
  uuid,
  text,
  text[],
  text,
  uuid[],
  uuid[]
) is 'Update an existing subject.';
grant execute on function sg_public.update_subject(
  uuid,
  text,
  text[],
  text,
  uuid[],
  uuid[]
) to sg_anonymous, sg_user, sg_admin;


-- migrate:down

