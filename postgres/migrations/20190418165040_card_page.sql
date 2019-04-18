-- migrate:up

create or replace function sg_public.card_subject(card sg_public.card)
returns sg_public.subject as $$
  select s.*
  from sg_public.subject s
  where s.entity_id = $1.subject_id;
$$ language sql stable;
comment on function sg_public.card_subject(sg_public.card)
  is 'Get the card''s subject.';
grant execute on function sg_public.card_subject(sg_public.card)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.user_md5_email(sg_public.user)
returns text as $$
  select md5(lower(trim(email)))
  from sg_private.user
  where user_id = $1.id
  limit 1;
$$ language sql stable strict security definer;
comment on function sg_public.user_md5_email(sg_public.user)
  is 'The user''s email address as an MD5 hash, for Gravatars. '
     'See https://bit.ly/2F6cR0M';
grant execute on function sg_public.user_md5_email(sg_public.user)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

