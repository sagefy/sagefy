-- migrate:up


drop function if exists sg_public.create_card(language character varying, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb);

CREATE or replace FUNCTION sg_public.create_card(language character varying, name text, subject_id uuid, kind sg_public.card_kind, data jsonb) RETURNS sg_public.card_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
  declare
    xentity_id uuid;
    xversion_id uuid;
    xcard_version sg_public.card_version;
  begin
    xentity_id := uuid_generate_v4();
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity
    (entity_id, entity_kind) values (xentity_id, 'card');
    insert into sg_public.card_entity
    (entity_id) values (xentity_id);
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'card');
    insert into sg_public.card_version
    (version_id, entity_id, language, name, subject_id, kind, data)
    values (xversion_id, xentity_id, language, name, subject_id, kind, data)
    returning * into xcard_version;
    return xcard_version;
  end;
$$;

COMMENT ON FUNCTION sg_public.create_card(language character varying, name text, subject_id uuid, kind sg_public.card_kind, data jsonb) IS 'Create a new card.';

grant execute on function sg_public.create_card(language character varying, name text, subject_id uuid, kind sg_public.card_kind, data jsonb)
  to sg_anonymous, sg_user, sg_admin;




drop function if exists sg_public.create_subject(language character varying, name text, tags text[], body text, parent uuid[], before uuid[]);

CREATE FUNCTION sg_public.create_subject(language character varying, name text, body text, parent uuid[], before uuid[]) RETURNS sg_public.subject_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
  declare
    xentity_id uuid;
    xversion_id uuid;
    xsubject_version sg_public.subject_version;
  begin
    xentity_id := uuid_generate_v4();
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity
    (entity_id, entity_kind) values (xentity_id, 'subject');
    insert into sg_public.subject_entity
    (entity_id) values (xentity_id);
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'subject');
    insert into sg_public.subject_version
    (version_id, entity_id, language, name, body)
    values (xversion_id, xentity_id, language, name, body)
    returning * into xsubject_version;
    insert into sg_public.subject_version_parent_child
    (child_version_id, parent_entity_id)
    select xversion_id, unnest(parent);
    insert into sg_public.subject_version_before_after
    (after_version_id, before_entity_id)
    select xversion_id, unnest(before);
    return xsubject_version;
  end;
$$;

COMMENT ON FUNCTION sg_public.create_subject(language character varying, name text, body text, parent uuid[], before uuid[]) IS 'Create a new subject.';

grant execute on function sg_public.create_subject(language character varying, name text, body text, parent uuid[], before uuid[])
  to sg_anonymous, sg_user, sg_admin;




drop function if exists sg_public.update_card(entity_id uuid, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb);

CREATE FUNCTION sg_public.update_card(entity_id uuid, name text, subject_id uuid, kind sg_public.card_kind, data jsonb) RETURNS sg_public.card_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
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
    (version_id, entity_id, language, previous_id, name, subject_id, kind, data)
    values (xversion_id, entity_id, 'en', xprevious.version_id, name, subject_id, kind, data)
    returning * into xcard_version;
    return xcard_version;
  end;
$$;

COMMENT ON FUNCTION sg_public.update_card(entity_id uuid, name text, subject_id uuid, kind sg_public.card_kind, data jsonb) IS 'Update an existing card.';

grant execute on function sg_public.update_card(entity_id uuid, name text, subject_id uuid, kind sg_public.card_kind, data jsonb)
  to sg_anonymous, sg_user, sg_admin;





drop function if exists sg_public.update_subject(entity_id uuid, name text, tags text[], body text, parent uuid[], before uuid[]);

CREATE FUNCTION sg_public.update_subject(entity_id uuid, name text, body text, parent uuid[], before uuid[]) RETURNS sg_public.subject_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
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
    (version_id, previous_version_id, entity_id, language, name, body)
    values (xversion_id, xprevious.version_id, entity_id, xprevious.language, name, body)
    returning * into xsubject_version;
    insert into sg_public.subject_version_parent_child
    (child_version_id, parent_entity_id)
    select xversion_id, unnest(parent);
    insert into sg_public.subject_version_before_after
    (after_version_id, before_entity_id)
    select xversion_id, unnest(before);
    return xsubject_version;
  end;
$$;


COMMENT ON FUNCTION sg_public.update_subject(entity_id uuid, name text, body text, parent uuid[], before uuid[]) IS 'Update an existing subject.';

grant execute on function sg_public.update_subject(entity_id uuid, name text, body text, parent uuid[], before uuid[])
  to sg_anonymous, sg_user, sg_admin;











CREATE or replace FUNCTION sg_public.search_cards(query text) RETURNS SETOF sg_public.card
    LANGUAGE sql STABLE
    AS $$
  -- If you see this in the future... NB the `to_tsvector` calls are indexed.
  -- if this part changes, you need to replace the index too.
  with r as (
    select
      distinct on (entity_id) entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ', name, data::text)),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.card_version
    where to_tsvector('english_unaccent', text_concat_ws(' ', name, data::text))
      @@ websearch_to_tsquery('english_unaccent', query)
    order by entity_id, rank
  )
  select c.*
  from sg_public.card c, r
  where c.entity_id = r.entity_id
  order by r.rank desc;
$$;


CREATE or replace FUNCTION sg_public.search_subjects(query text) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  -- If you see this in the future... NB the `to_tsvector` calls are indexed.
  -- if this part changes, you need to replace the index too.
  with r as (
    select
      distinct on (entity_id) entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ', name, body)),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.subject_version
    where to_tsvector('english_unaccent', text_concat_ws(' ', name, body))
      @@ websearch_to_tsquery('english_unaccent', query)
    order by entity_id, rank
  )
  select s.*
  from sg_public.subject s, r
  where s.entity_id = r.entity_id
  order by r.rank desc;
$$;

drop INDEX sg_public.search_card_idx;

CREATE INDEX search_card_idx ON sg_public.card_version USING gin (to_tsvector('public.english_unaccent'::regconfig, public.text_concat_ws(' '::text, VARIADIC ARRAY[name, (data)::text])));

drop INDEX sg_public.search_subject_idx;

CREATE INDEX search_subject_idx ON sg_public.subject_version USING gin (to_tsvector('public.english_unaccent'::regconfig, public.text_concat_ws(' '::text, VARIADIC ARRAY[name, body])));




-- migrate:down

