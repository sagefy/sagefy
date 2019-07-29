-- migrate:up

create or replace function sg_public.search_cards(query text)
returns setof sg_public.card as $$
  with documents as (
    select
      entity_id,
      to_tsvector('english', unaccent(name)) ||
      to_tsvector('english', unaccent(array_to_string(tags, ' '))) ||
      to_tsvector('english', unaccent(data::text)) as document
    from sg_public.card
  ),
  ranking as (
    select
      c.entity_id as entity_id,
      ts_rank(d.document, websearch_to_tsquery('english', unaccent(query))) as rank
    from
      sg_public.card c,
      documents d
    where
      d.document @@ websearch_to_tsquery('english', unaccent(query))
      and c.entity_id = d.entity_id
    order by rank desc
  )
  select c.*
  from
    ranking r,
    sg_public.card c
  where
    c.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;
comment on function sg_public.search_cards(text)
  is 'Search cards.';
grant execute on function sg_public.search_cards(text)
  to sg_anonymous, sg_user, sg_admin;

create type sg_public.search_result as (
  entity_id uuid,
  kind text,
  subkind text,
  name text,
  body jsonb
);
comment on type sg_public.search_result
  is 'The format of a search result entry.';

create or replace function sg_public.search_entities(query text)
returns setof sg_public.search_result as $$
  select
    s.entity_id as entity_id,
    'subject' as kind,
    'subject' as subkind,
    s.name as name,
    to_jsonb(s.body) as body
  from sg_public.search_subjects(query) s
  union all
  select
    c.entity_id as entity_id,
    'card' as kind,
    c.kind::text as subkind,
    c.name as name,
    c.data as body
  from sg_public.search_cards(query) c;
$$ language sql stable;
comment on function sg_public.search_entities(text)
  is 'Search subjects and cards.';
grant execute on function sg_public.search_entities(text)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

