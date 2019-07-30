-- migrate:up

create or replace function sg_public.cards_by_current_user()
returns setof sg_public.card as $$
  select *
  from sg_public.card
  where entity_id in (
    select entity_id
    from sg_public.card_version
    where user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
  );
$$ language sql stable;
comment on function sg_public.cards_by_current_user()
  is 'Select cards I created or worked on.';
grant execute on function sg_public.cards_by_current_user()
  to sg_user, sg_admin;

create or replace function sg_public.subjects_by_current_user()
returns setof sg_public.subject as $$
  select *
  from sg_public.subject
  where entity_id in (
    select entity_id
    from sg_public.subject_version
    where user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
  );
$$ language sql stable;
comment on function sg_public.subjects_by_current_user()
  is 'Select subjects I created or worked on.';
grant execute on function sg_public.subjects_by_current_user()
  to sg_user, sg_admin;

-- migrate:down

