-- migrate:up

create or replace function sg_public.subject_user_count(sg_public.subject)
returns bigint as $$
  select count(*)
  from sg_public.user_subject us
  where us.subject_id = $1.entity_id
  and us.user_id is not null;
  -- This function should count all usubjs, not just the current users.
$$ language sql stable strict security definer;
comment on function sg_public.subject_user_count(sg_public.subject)
  is 'Count the number of logged in users learning the subject.';
grant execute on function sg_public.subject_user_count(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.select_popular_subjects()
returns setof sg_public.subject as $$
  with most_popular as (
    select s.*
    from sg_public.subject s
    order by sg_public.subject_user_count(s) desc
    limit 20
  )
  select *
  from most_popular
  where name not ilike '%what is sagefy?%'
  order by random()
  limit 4;
$$ language sql stable;

create or replace function sg_public.what_is_sagefy()
returns sg_public.subject as $$
  select *
  from sg_public.subject
  where name ilike '%what is sagefy?%'
  limit 1;
$$ language sql stable;
comment on function sg_public.what_is_sagefy()
  is 'Grab just the single "What is Sagefy?" subject, if it exists.';
grant execute on function sg_public.what_is_sagefy()
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

