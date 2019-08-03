-- migrate:up

-- If you see this in the future... NB the `to_tsvector` calls are indexed.
-- if this part changes, you need to replace the index too.

create or replace function sg_public.search_subjects(query text)
returns setof sg_public.subject as $$
  select s.*
  from sg_public.subject s, (
    select
      entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ',
          name, text_array_to_text(tags), body
        )),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.subject
  ) r
  where r.rank > 0 and s.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;

create or replace function sg_public.search_cards(query text)
returns setof sg_public.card as $$
  select c.*
  from sg_public.card c, (
    select
      entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ',
          name, text_array_to_text(tags), data::text
        )),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.card
  ) r
  where r.rank > 0 and c.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;

-- migrate:down

