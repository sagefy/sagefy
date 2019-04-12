-- migrate:up

create or replace function sg_public.subject_cards(subject sg_public.subject)
returns setof sg_public.card as $$
  select c.*
  from sg_public.card c
  where c.subject_id = $1.entity_id;
$$ language sql stable;
comment on function sg_public.subject_cards(sg_public.subject)
  is 'List the number of cards directly on the subject.';
grant execute on function sg_public.subject_cards(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_card_count(subject sg_public.subject)
returns bigint as $$
  select count(c.*) from sg_public.subject_cards($1) c;
$$ language sql stable;

alter table sg_public.subject_version
add column details text null;
comment on column sg_public.subject_version.details
  is 'The details of the subject.';

-- Have to redo the view so it picks up on the column
create or replace view sg_public.subject as
  select distinct on (entity_id) *
  from sg_public.subject_version
  where status = 'accepted'
  order by entity_id, created desc;

create or replace function sg_public.subject_parent_subjects(subject sg_public.subject)
returns setof sg_public.subject as $$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_parent_child svpc
  where
    svpc.child_version_id = $1.version_id
    and s.entity_id = svpc.parent_entity_id;
$$ language sql stable;
comment on function sg_public.subject_parent_subjects(sg_public.subject)
  is 'Collects the direct parents of the child subject.';
grant execute on function sg_public.subject_parent_subjects(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

