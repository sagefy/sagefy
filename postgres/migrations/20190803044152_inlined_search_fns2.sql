-- migrate:up

create or replace function sg_public.search_subjects(query text)
returns setof sg_public.subject as $$
  -- If you see this in the future... NB the `to_tsvector` calls are indexed.
  -- if this part changes, you need to replace the index too.
  with r as (
    select
      distinct on (entity_id) entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ',
          name, text_array_to_text(tags), body
        )),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.subject_version
    where to_tsvector('english_unaccent', text_concat_ws(' ',
      name, text_array_to_text(tags), body
    )) @@ websearch_to_tsquery('english_unaccent', query)
    order by entity_id, rank
  )
  select s.*
  from sg_public.subject s, r
  where s.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;

create or replace function sg_public.search_cards(query text)
returns setof sg_public.card as $$
  -- If you see this in the future... NB the `to_tsvector` calls are indexed.
  -- if this part changes, you need to replace the index too.
  with r as (
    select
      distinct on (entity_id) entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ',
          name, text_array_to_text(tags), data::text
        )),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.card_version
    where to_tsvector('english_unaccent', text_concat_ws(' ',
      name, text_array_to_text(tags), data::text
    )) @@ websearch_to_tsquery('english_unaccent', query)
    order by entity_id, rank
  )
  select c.*
  from sg_public.card c, r
  where c.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;

-- migrate:down

