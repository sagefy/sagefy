-- migrate:up

create or replace function sg_public.select_popular_subjects()
returns setof sg_public.subject as $$
  select *
  from sg_public.subject s
  order by (
    select count(*)
    from sg_public.user_subject us
    where us.subject_id = s.entity_id
    and us.user_id is not null
  ) desc, random()
  limit 5;
  -- This function should count all usubjs, not just the current users.
$$ language sql stable strict security definer;

-- migrate:down

