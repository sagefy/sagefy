-- migrate:up

-- Learning endpoints:
-- - Choose subject
-- - Choose card
-- - Get card
-- - Create response

create view sg_public.card as
  select distinct on (entity_id) *
  from sg_public.card_version
  where status = 'accepted'
  order by entity_id, created desc;
comment on view sg_public.card
  is 'The latest accepted version of each card.';
grant select on sg_public.card to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.card_by_entity_id(entity_id uuid)
returns sg_public.card as $$
  select c.*
  from sg_public.card c
  where c.entity_id = $1
  limit 1;
$$ language sql stable;
comment on function sg_public.card_by_entity_id(uuid)
  is 'Get the latest version of the card.';
grant execute on function sg_public.card_by_entity_id(uuid)
  to sg_anonymous, sg_user, sg_admin;

grant select on table sg_public.subject_version_before_after
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.subject_version_parent_child
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.card_version
  to sg_anonymous, sg_user, sg_admin;

create table sg_public.response (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id),
  session_id uuid null,
  card_id uuid not null references sg_public.card_entity (entity_id),
  subject_id uuid not null references sg_public.subject_entity (entity_id),
  response text not null,
  score real not null check (score >= 0 and score <= 1),
  learned real not null check (score >= 0 and score <= 1),
  constraint user_or_session check (user_id is not null or session_id is not null)
);

comment on table sg_public.response
  is 'When a learner responds to a card, we record the result.';
comment on column sg_public.response.id
  is 'The ID of the response.';
comment on column sg_public.response.created
  is 'When the user created the response.';
comment on column sg_public.response.modified
  is 'When the system last modified the response.';
comment on column sg_public.response.user_id
  is 'The user the response belongs to.';
comment on column sg_public.response.session_id
  is 'If not user, the session_id the response belongs to.';
comment on column sg_public.response.card_id
  is 'The card (entity id) that the response belongs to.';
comment on column sg_public.response.subject_id
  is 'The subject (entity id) that the response belongs to... '
     'at the time of the response';
comment on column sg_public.response.response
  is 'How the user responded.';
comment on column sg_public.response.score
  is 'The score, 0->1, of the response.';
comment on column sg_public.response.learned
  is 'The estimated probability the learner has learned the subject, '
     'after this response.';
comment on constraint user_or_session on sg_public.response
  is 'Ensure only the user or session has data.';

create index on "sg_public"."response"("user_id");
create index on "sg_public"."response"("card_id");
create index on "sg_public"."response"("subject_id");

create trigger insert_response_user_or_session
  before insert on sg_public.response
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_response_user_or_session
  on sg_public.response
  is 'Whenever I make a new response, auto fill the `user_id` column';

create trigger update_response_modified
  before update on sg_public.response
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_response_modified on sg_public.response
  is 'Whenever a response changes, update the `modified` column.';

create or replace function sg_public.select_latest_response(subject_id uuid)
returns sg_public.response as $$
  select r.*
  from sg_public.response r
  where r.subject_id = $1 and (
    user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
    or session_id = nullif(current_setting('jwt.claims.session_id', true), '')::uuid
  )
  order by r.created desc
  limit 1;
$$ language sql stable;
comment on function sg_public.select_latest_response(uuid)
  is 'Get the latest response from the user on the given subject.';
grant execute on function sg_public.select_latest_response(uuid)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.select_subject_learned(subject_id uuid)
returns real as $$
  select case when learned is not null then learned else 0.4 end
  from sg_public.select_latest_response($1);
$$ language sql stable;
comment on function sg_public.select_subject_learned(uuid)
  is 'Get the latest learned value for the user on the given subject.';
grant execute on function sg_public.select_subject_learned(uuid)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_private.score_response()
returns trigger as $$
  declare
    card sg_public.card;
    prior sg_public.response;
    prior_learned real;
    option jsonb;
    score real;
    learned real;
    slip constant real := 0.1;
    guess constant real := 0.3;
    transit constant real := 0.05;
  begin
    -- Overall: Fill in (subject_id, score, learned)
    -- Validate if the response to the card is valid.
    select c.* into card
    from sg_public.card c
    where c.entity_id = new.card_id
    limit 1;
    if (card.kind is null) then
      raise exception 'No card found.' using errcode = 'EE05C989';
    end if;
    if (card.kind <> 'choice') then -- scored kinds only
      raise exception 'You may only respond to a scored card.'
        using errcode = '1306BF1C';
    end if;
    option := card.data->'options'->new.response;
    if (option is null) then
      raise exception 'You must submit an available response `id`.'
        using errcode = '681942FD';
    end if;
    -- Set default values
    new.subject_id := card.subject_id;
    -- Score the response
    new.score := (option->>'correct')::boolean::int::real;
    -- Calculate p(learned)
    prior_learned := (select sg_public.select_subject_learned(card.subject_id));
    learned := (
      new.score * (
        (prior_learned * (1 - slip)) /
        (prior_learned * (1 - slip) + (1 - prior_learned) * guess)
      ) +
      (1 - new.score) * (
        (prior_learned * slip) /
        (prior_learned * slip + (1 - prior_learned) * (1 - guess))
      )
    );
    new.learned := learned + (1 - learned) * transit;
    return new;
  end;
$$ language plpgsql strict security definer;
comment on function sg_private.score_response()
  is 'After I respond to a card, score the result and update model.';

create trigger insert_response_score
  before insert on sg_public.response
  for each row execute procedure sg_private.score_response();
comment on trigger insert_response_score on sg_public.response
  is 'After I respond to a card, score the result and update model.';

-- Enable RLS.

alter table sg_public.response enable row level security;

-- Select response: any self.
grant select on table sg_public.response to sg_anonymous, sg_user, sg_admin;
create policy select_response on sg_public.response
  for select to sg_anonymous, sg_user, sg_admin
  using (
    user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
    or session_id = nullif(current_setting('jwt.claims.session_id', true), '')::uuid
  );
comment on policy select_response on sg_public.response
  is 'Anyone may select their own responses.';

-- Insert response: any.
grant insert (card_id, response)
  on table sg_public.response to sg_anonymous, sg_user, sg_admin;
create policy insert_response on sg_public.response
  for insert to sg_anonymous, sg_user, sg_admin
  with check (true);
comment on policy insert_response on sg_public.response
  is 'Anyone may insert `card_id` and `response` into responses.';

-- Update & delete response: none.

create or replace function sg_public.select_card_to_learn(subject_id uuid)
returns sg_public.card as $$
  with prior as (select * from sg_public.select_latest_response($1)),
  k (kinds) as (
    select case
      when random() < (0.5 + 0.5 * sg_public.select_subject_learned($1))
      then array[
        'choice'
      ]::sg_public.card_kind[]
      else array[
        'video',
        'page',
        'unscored_embed'
      ]::sg_public.card_kind[]
    end
  )
  select c.*
  from sg_public.card c, prior, k
  where c.subject_id = $1
    and c.kind = any(k.kinds)
    and (prior.card_id is null or c.entity_id <> prior.card_id)
  order by random()
  limit 1;
  -- Future version: When estimating parameters and the card kind is scored,
  -- prefer 0.25 < correct < 0.75
$$ language sql volatile;
comment on function sg_public.select_card_to_learn(uuid)
  is 'After I select a subject, search for a suitable card.';
grant execute on function sg_public.select_card_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_child_subjects(subject sg_public.subject)
returns setof sg_public.subject as $$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_parent_child svpc
  where
    svpc.parent_entity_id = $1.entity_id
    and s.version_id = svpc.child_version_id;
$$ language sql stable;
comment on function sg_public.subject_child_subjects(sg_public.subject)
  is 'Collects the direct children of the parent subject.';
grant execute on function sg_public.subject_child_subjects(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_all_child_subjects(subject sg_public.subject)
returns setof sg_public.subject as $$
  with recursive all_children as (
    select scs.*
    from sg_public.subject_child_subjects(subject) scs
    union all
    select scs.*
    from
      all_children,
      lateral sg_public.subject_child_subjects(all_children) scs
  )
  select *
  from all_children;
$$ language sql stable;
comment on function sg_public.subject_all_child_subjects(sg_public.subject)
  is 'Collects all the children of the parent subject.';
grant execute on function sg_public.subject_all_child_subjects(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_child_count(subject sg_public.subject)
returns bigint as $$
  select count(*)
  from sg_public.subject_child_subjects(subject);
$$ language sql stable;
comment on function sg_public.subject_child_count(sg_public.subject)
  is 'Count the number of children directly on the subject.';
grant execute on function sg_public.subject_child_count(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_card_count(subject sg_public.subject)
returns bigint as $$
  select count(c.*)
  from sg_public.card c
  where c.subject_id = $1.entity_id;
$$ language sql stable;
comment on function sg_public.subject_card_count(sg_public.subject)
  is 'Count the number of cards directly on the subject.';
grant execute on function sg_public.subject_card_count(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_before_subjects(subject sg_public.subject)
returns setof sg_public.subject as $$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_before_after svba
  where
    svba.after_version_id = $1.version_id
    and s.entity_id = svba.before_entity_id;
$$ language sql stable;
comment on function sg_public.subject_before_subjects(sg_public.subject)
  is 'Get all the direct befores for a subject.';
grant execute on function sg_public.subject_before_subjects(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_has_needed_before(sg_public.subject, uuid[])
returns boolean as $$
  select exists(
    select x.entity_id
    from sg_public.subject_before_subjects($1) x
    where sg_public.select_subject_learned(x.entity_id) < 0.99
    and x.entity_id = any($2)
  );
$$ language sql stable;
comment on function sg_public.subject_has_needed_before(sg_public.subject, uuid[])
  is 'Does the learner/subject have a needed before?';
grant execute on function sg_public.subject_has_needed_before(sg_public.subject, uuid[])
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_after_subjects(subject sg_public.subject)
returns setof sg_public.subject as $$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_before_after svba
  where
    svba.before_entity_id = $1.entity_id
    and s.version_id = svba.after_version_id;
$$ language sql stable;
comment on function sg_public.subject_after_subjects(sg_public.subject)
  is 'Get all the direct afters for a subject.';
grant execute on function sg_public.subject_after_subjects(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_all_after_subjects(subject sg_public.subject)
returns setof sg_public.subject as $$
  with recursive all_afters as (
    select scs.*
    from sg_public.subject_after_subjects(subject) scs
    union all
    select scs.*
    from
      all_afters,
      lateral sg_public.subject_after_subjects(all_afters) scs
  )
  select *
  from all_afters;
$$ language sql stable;
comment on function sg_public.subject_all_after_subjects(sg_public.subject)
  is 'Collects all the afters of the before subject.';
grant execute on function sg_public.subject_all_after_subjects(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_all_after_count(subject sg_public.subject)
returns bigint as $$
  select count(*)
  from sg_public.subject_all_after_subjects($1);
$$ language sql stable;
comment on function sg_public.subject_all_after_count(sg_public.subject)
  is 'Count the number of subjects after the subject.';
grant execute on function sg_public.subject_all_after_count(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.select_subject_to_learn(subject_id uuid)
returns setof sg_public.subject as $$
  with subject as (
    select *
    from sg_public.subject
    where entity_id = $1
    limit 1
  ),
  all_subjects as (
    select a.*
    from subject, sg_public.subject_all_child_subjects(subject) a
    union
    select * from subject
  ),
  e (all_subjects) as (select array(select entity_id from all_subjects))
  select s.*
  from all_subjects s, e
  where
    sg_public.subject_child_count(s) = 0
    and sg_public.select_subject_learned(s.entity_id) < 0.99
    and not sg_public.subject_has_needed_before(s, e.all_subjects)
    -- TODO support "rewind"... going into out of goals befores
    -- when performance is low.
  order by
    sg_public.subject_all_after_count(s) desc,
    sg_public.subject_card_count(s) desc
  limit 5;
$$ language sql stable;
comment on function sg_public.select_subject_to_learn(uuid)
  is 'After I select a main subject, search for suitable child subjects.';
grant execute on function sg_public.select_subject_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;

create index on "sg_public"."subject_version_parent_child"("child_version_id");
create index on "sg_public"."subject_version_before_after"("after_version_id");

-- migrate:down

