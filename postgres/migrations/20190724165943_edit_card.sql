-- migrate:up

create or replace function sg_public.update_card(
  entity_id uuid,
  name text,
  tags text[],
  subject_id uuid,
  kind sg_public.card_kind,
  data jsonb
)
returns sg_public.card_version as $$
  declare
    xprevious sg_public.card;
    xversion_id uuid;
    xcard_version sg_public.card_version;
  begin
    select * into xprevious
    from sg_public.card_by_entity_id(entity_id);
    if (xprevious is null) then
      raise exception 'No previous version found.' using errcode = 'CF018471';
    end if;
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'card');
    insert into sg_public.card_version
    (version_id, entity_id, language, previous_id, name, tags, subject_id, kind, data)
    values (xversion_id, entity_id, 'en', xprevious.version_id, name, tags, subject_id, kind, data)
    returning * into xcard_version;
    return xcard_version;
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.update_card(
  uuid,
  text,
  text[],
  uuid,
  sg_public.card_kind,
  jsonb
) is 'Update an existing card.';
grant execute on function sg_public.update_card(
  uuid,
  text,
  text[],
  uuid,
  sg_public.card_kind,
  jsonb
) to sg_anonymous, sg_user, sg_admin;

-- migrate:down

