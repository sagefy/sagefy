-- migrate:up

create or replace function sg_public.electronic_music()
returns sg_public.subject as $$
  select *
  from sg_public.subject
  where name = 'An Introduction to Electronic Music'
  limit 1;
$$ language sql stable;
comment on function sg_public.electronic_music()
  is 'Grab just the single "An Introduction to Electronic Music" subject, if it exists.';
grant execute on function sg_public.electronic_music()
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.trending_subjects()
returns setof sg_public.subject as $$
  with first as (
    select *
    from sg_public.what_is_sagefy()
    where entity_id is not null
  ), second as (
    select *
    from sg_public.electronic_music()
    where entity_id is not null
  ), rps as (
    select ps.*
    from sg_public.recent_popular_subjects(7) ps, first
    where ps.entity_id != first.entity_id
    limit 50
  ), trending as (
    select *
    from rps
    order by random()
  )
  select * from first
  union all
  select * from second
  union all
  select * from trending;
$$ language sql stable;
comment on function sg_public.trending_subjects()
  is 'Select trending subjects over the last 7 days. Always starts with "What is Sagefy?" and "An Introduction to Electronic Music" if they exist.';
grant execute on function sg_public.trending_subjects()
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

