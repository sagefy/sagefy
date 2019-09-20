-- migrate:up

create or replace function sg_public.recent_popular_subjects(days int)
returns setof sg_public.subject as $$
  with counts as (
    select subject_id, count(*)
    from sg_public.user_subject us
    where us.created > current_date - days
    group by subject_id
  )
  select s.*
  from sg_public.subject s
  left join counts
  on s.entity_id = counts.subject_id
  order by count desc nulls last;
  -- This function should count all usubjs, not just the current users.
$$ language sql stable strict security definer;

drop function if exists sg_public.popular_subjects;

create or replace function sg_public.trending_subjects()
returns setof sg_public.subject as $$
  with first as (
    select *
    from sg_public.what_is_sagefy()
    where entity_id is not null
  ), rps as (
    select ps.*
    from sg_public.recent_popular_subjects(7) ps, first
    where ps.entity_id != first.entity_id
    limit 20
  ), trending as (
    select *
    from rps
    order by random()
  )
  select * from first
  union all
  select * from trending;
$$ language sql stable;
comment on function sg_public.trending_subjects()
  is 'Select trending subjects over the last 7 days. Always starts with "What is Sagefy?" if it exists.';
grant execute on function sg_public.trending_subjects()
  to sg_anonymous, sg_user, sg_admin;


-- migrate:down

