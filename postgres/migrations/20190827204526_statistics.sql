-- migrate:up

-- user subject 7/28/364
create or replace function sg_public.recent_user_subject_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.user_subject
  where created > current_date - days;
  -- This function should count all usubjs, not just the current users.
$$ language sql stable strict security definer;
comment on function sg_public.recent_user_subject_count(int)
  is 'Count the number of new user subjects in the last X days.';
grant execute on function sg_public.recent_user_subject_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- response all 7/28/364
-- response filter 99, 90 7/28/364
create or replace function sg_public.recent_response_count(days int, min real default 0)
returns bigint as $$
  select count(*)
  from sg_public.response
  where created > current_date - days
  and learned >= min;
  -- This function should count all usubjs, not just the current users.
$$ language sql stable strict security definer;
comment on function sg_public.recent_response_count(int, real)
  is 'Count the number of new user subjects in the last X days.';
grant execute on function sg_public.recent_response_count(int, real)
  to sg_anonymous, sg_user, sg_admin;

-- new subject
create or replace function sg_public.recent_subject_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.subject_version
  where created > current_date - days
  and previous_version_id is null
  and status = 'accepted';
$$ language sql stable;
comment on function sg_public.recent_subject_count(int)
  is 'Count the number of new subjects in the last X days.';
grant execute on function sg_public.recent_subject_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- edit subject
create or replace function sg_public.recent_subject_update_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.subject_version
  where created > current_date - days
  and previous_version_id is not null
  and status = 'accepted';
$$ language sql stable;
comment on function sg_public.recent_subject_update_count(int)
  is 'Count the number of subject updates in the last X days.';
grant execute on function sg_public.recent_subject_update_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- new card
create or replace function sg_public.recent_card_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.card_version
  where created > current_date - days
  and previous_id is null
  and status = 'accepted';
$$ language sql stable;
comment on function sg_public.recent_card_count(int)
  is 'Count the number of new cards in the last X days.';
grant execute on function sg_public.recent_card_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- edit card
create or replace function sg_public.recent_card_update_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.card_version
  where created > current_date - days
  and previous_id is not null
  and status = 'accepted';
$$ language sql stable;
comment on function sg_public.recent_card_update_count(int)
  is 'Count the number of card updates in the last X days.';
grant execute on function sg_public.recent_card_update_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- new post
create or replace function sg_public.recent_post_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.post
  where created > current_date - days;
$$ language sql stable;
comment on function sg_public.recent_post_count(int)
  is 'Count the number of new posts in the last X days.';
grant execute on function sg_public.recent_post_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- new topic
create or replace function sg_public.recent_topic_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.topic
  where created > current_date - days;
$$ language sql stable;
comment on function sg_public.recent_topic_count(int)
  is 'Count the number of new topics in the last X days.';
grant execute on function sg_public.recent_topic_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- new user
create or replace function sg_public.recent_user_count(days int)
returns bigint as $$
  select count(*)
  from sg_public.user
  where created > current_date - days;
$$ language sql stable;
comment on function sg_public.recent_user_count(int)
  is 'Count the number of new users in the last X days.';
grant execute on function sg_public.recent_user_count(int)
  to sg_anonymous, sg_user, sg_admin;

-- Most frequent subjects last 7 days
create or replace function sg_public.recent_popular_subjects(days int)
returns setof sg_public.subject as $$
  with counts as (
    select subject_id, count(*)
    from sg_public.user_subject us
    group by subject_id
  )
  select s.*
  from sg_public.subject s, counts
  where s.entity_id = counts.subject_id
  order by count desc;
  -- This function should count all usubjs, not just the current users.
$$ language sql stable strict security definer;
comment on function sg_public.recent_popular_subjects(int)
  is '';
grant execute on function sg_public.recent_popular_subjects(int)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

