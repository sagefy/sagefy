-- migrate:up

grant select on table sg_public.subject_version
  to sg_anonymous, sg_user, sg_admin;

create table sg_public.user_subject (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id) on delete cascade,
  session_id uuid null,
  subject_id uuid not null references sg_public.subject_entity (entity_id),
  unique (user_id, subject_id),
  unique (session_id, subject_id),
  constraint user_or_session check (user_id is not null or session_id is not null)
);

comment on table sg_public.user_subject
  is 'The association between a user and a subject. '
     'This is a subject the learner is learning.';
comment on column sg_public.user_subject.id
  is 'The ID of the user subject.';
comment on column sg_public.user_subject.created
  is 'When the user created the association.';
comment on column sg_public.user_subject.modified
  is 'When the association last changed.';
comment on column sg_public.user_subject.user_id
  is 'Which user the association belongs to.';
comment on column sg_public.user_subject.session_id
  is 'If not user, the session the association belongs to.';
comment on column sg_public.user_subject.subject_id
  is 'Which subject the association belongs to.';
comment on constraint user_or_session on sg_public.user_subject
  is 'Ensure only the user or session has data.';

create trigger insert_user_subject_user_or_session
  before insert on sg_public.user_subject
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_user_subject_user_or_session
  on sg_public.user_subject
  is 'Whenever I make a new user subject, auto fill the `user_id` column';

create trigger update_user_subject_modified
  before update on sg_public.user_subject
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_user_subject_modified on sg_public.user_subject
  is 'Whenever a user subject changes, update the `modified` column.';

alter table sg_public.user_subject enable row level security;

-- Select usubj: user or admin self or with setting.
grant select on table sg_public.user_subject to sg_user, sg_admin;
create policy select_user_subject on sg_public.user_subject
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy select_user_subject on sg_public.user_subject
  is 'A user or admin may select their own subject relationships.';

-- Insert usubj: user or admin.
grant insert (subject_id) on table sg_public.user_subject to sg_user, sg_admin;
create policy insert_user_subject on sg_public.user_subject
  for insert to sg_user, sg_admin;
comment on policy insert_user_subject on sg_public.user_subject
  is 'A user or admin may insert a user subject relationship.';

-- Update usubj: none.

-- Delete usubj: user or admin self.
grant delete on table sg_public.user_subject to sg_user, sg_admin;
create policy delete_user_subject on sg_public.user_subject
  for delete to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy delete_user_subject on sg_public.user_subject
  is 'A user or admin can delete their own user subject.';

create view sg_public.subject as
  select distinct on (entity_id) *
  from sg_public.subject_version
  where status = 'accepted'
  order by entity_id, created desc;
comment on view sg_public.subject
  is 'The latest accepted version of each subject.';

create function sg_public.select_popular_subjects()
returns setof sg_public.subject as $$
  select *
  from sg_public.subject
  order by (
    select count(*)
    from sg_public.user_subject
    where subject_id = entity_id
  )
  limit 5;
$$ language sql stable;
comment on function sg_public.select_popular_subjects()
  is 'Select the 5 most popular subjects.';
grant execute on function sg_public.select_popular_subjects()
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.search_subjects(query text)
returns setof sg_public.subject as $$
  with documents as (
    select
      entity_id,
      to_tsvector('english', unaccent(name)) ||
      to_tsvector('english', unaccent(array_to_string(tags, ' '))) ||
      to_tsvector('english', unaccent(body)) as document
    from sg_public.subject
  ),
  ranking as (
    select
      s.entity_id as entity_id,
      ts_rank(d.document, websearch_to_tsquery('english', unaccent(query))) as rank
    from
      sg_public.subject s,
      documents d
    where
      d.document @@ websearch_to_tsquery('english', unaccent(query))
      and s.entity_id = d.entity_id
    order by rank desc
  )
  select s.*
  from
    ranking r,
    sg_public.subject s
  where
    s.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;
comment on function sg_public.search_subjects(text)
  is 'Search subjects.';
grant execute on function sg_public.search_subjects(text)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

