-- migrate:up

-- We create a new array_to_text. This function is normally stable,
-- because it may involve dates or times. By limiting it to text, we can
-- mark it immutable, which makes it indexable.
create or replace function text_array_to_text(arr text[])
returns text as $$
  select array_to_string(arr, ' ');
$$ language sql immutable;
comment on function text_array_to_text(text[])
  is 'Convert an array of text to a single text.';
grant execute on function text_array_to_text(text[])
  to sg_anonymous, sg_user, sg_admin;

-- Similarly again, concat_ws can take date or times which are
-- stable but not immutable, so we create a sister than only takes text
-- we can mark as immutable and indexable.
create or replace function text_concat_ws(text, variadic text[])
returns text as 'text_concat_ws' language internal immutable;
comment on function text_concat_ws(text, variadic text[])
  is 'Concat a list of plain text to a single text.';
grant execute on function text_concat_ws(text, variadic text[])
  to sg_anonymous, sg_user, sg_admin;

-- `unaccent` is also stable and not immutable,
-- for the same date/time formatting reasons, so we create a new
-- search dictionary that adds in unaccent to the regular English
-- dictionary so its indexable.
create text search configuration english_unaccent (copy = english);
alter text search configuration english_unaccent
  alter mapping for hword, hword_part, word
  with unaccent, english_stem;

create or replace function sg_public.search_subjects(query text)
returns setof sg_public.subject as $$
  with documents as (
    select
      entity_id,
      to_tsvector('english_unaccent', text_concat_ws(' ',
        name, text_array_to_text(tags), body
      )) as document
    from sg_public.subject
  ),
  ranking as (
    select
      s.entity_id as entity_id,
      ts_rank(d.document, websearch_to_tsquery('english_unaccent', query)) as rank
    from sg_public.subject s, documents d
    where
      d.document @@ websearch_to_tsquery('english_unaccent', query)
      and s.entity_id = d.entity_id
    order by rank desc
  )
  select s.*
  from ranking r, sg_public.subject s
  where s.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;

create index search_subject_idx
  on sg_public.subject_version
  using gin (
    to_tsvector('english_unaccent', text_concat_ws(' ',
      name, text_array_to_text(tags), body
    ))
  );

create or replace function sg_public.search_cards(query text)
returns setof sg_public.card as $$
  with documents as (
    select
      entity_id,
      to_tsvector('english_unaccent', text_concat_ws(' ',
        name, text_array_to_text(tags), data::text
      )) as document
    from sg_public.card
  ),
  ranking as (
    select
      c.entity_id as entity_id,
      ts_rank(d.document, websearch_to_tsquery('english_unaccent', query)) as rank
    from sg_public.card c, documents d
    where
      d.document @@ websearch_to_tsquery('english_unaccent', query)
      and c.entity_id = d.entity_id
    order by rank desc
  )
  select c.*
  from ranking r, sg_public.card c
  where c.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;

create index search_card_idx
  on sg_public.card_version
  using gin (
    to_tsvector('english_unaccent', text_concat_ws(' ',
      name, text_array_to_text(tags), data::text
    ))
  );

-- migrate:down

