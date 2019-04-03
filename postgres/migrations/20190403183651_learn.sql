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

create function sg_public.select_latest_response(subject_id uuid)
returns sg_public.response as $$
  -- If no response yet, default to 0.4
  select *
  from sg_public.response
  where sg_public.response.subject_id = subject_id and (
    user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
    or session_id = nullif(current_setting('jwt.claims.session_id', true), '')::uuid
  )
  order by created desc
  limit 1;
$$ language sql stable;
comment on function sg_public.select_latest_response(uuid)
  is 'Get the latest response from the user on the given subject.';

create or replace function sg_private.score_response()
returns trigger as $$
  declare
    card sg_public.card;
    prior sg_public.response;
    prior_learned real := 0.4;
    option jsonb;
    score real;
    learned real;
    slip constant real := 0.1;
    guess constant real := 0.3;
    transit constant real := 0.05;
  begin
    -- Overall: Fill in (subject_id, score, learned)
    -- Validate if the response to the card is valid.
    card := (
      select *
      from sg_public.card
      where sg_public.card.entity_id = new.card_id
      limit 1
    );
    if (!card) then
      raise exception 'No card found.' using errcode = 'EE05C989';
    end if;
    if (card.kind <> 'choice') then -- scored kinds only
      raise exception 'You may only respond to a scored card.'
        using errcode = '1306BF1C';
    end if;
    option := card.data->'options'->new.response;
    if (!option) then
      raise exception 'You must submit an available response `id`.'
        using errcode = '681942FD';
    end if;
    -- Set default values
    new.subject_id := card.subject_id;
    -- Score the response
    new.score := case when option->'correct' then 1 else 0 end;
    -- Calculate p(learned)
    prior := sg_public.select_latest_response(card.subject_id);
    if (prior) then
      prior_learned := prior.learned;
    end if;
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

-- Insert response: any via function.
grant insert (card_id, response)
  on table sg_public.response to sg_anonymous, sg_user, sg_admin;
create policy insert_response on sg_public.response
  for insert to sg_anonymous, sg_user, sg_admin;
comment on policy insert_response on sg_public.response
  is 'Anyone may insert `card_id` and `response` into responses.';

-- Update & delete response: none.

create function sg_public.select_card_to_learn(subject_id uuid)
returns sg_public.card as $$
  declare
    latest_response sg_public.response;
    kinds text[];
  begin
    -- What is p(learned) currently for the subject?
    latest_response := (select sg_public.select_latest_response(subject_id));
    -- Decide on a scored or unscored type
    kinds := (
      select case when random() > (
        0.5 + 0.5 * (latest_response.learned or 0.4)
      ) then
        array['choice'] -- scored kinds
      else
        array['video', 'page', 'unscored_embed'] -- unscored kinds
      end
    );
    select *
    from sg_public.card
    where sg_public.card.subject_id = subject_id
      and sg_public.card.kind = any(kinds)
      -- Don't allow the previous card as the next card
      and sg_public.card.entity_id <> latest_response.card_id
    -- Select cards of kind at random
    order by random()
    limit 1;
  end;
  -- Future version: When estimating parameters and the card kind is scored,
  -- prefer 0.25 < correct < 0.75
$$ language plpgsql strict security definer;
comment on function sg_public.select_card_to_learn(uuid)
  is 'After I select a subject, search for a suitable card.';
grant execute on function sg_public.select_card_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.select_subject_to_learn(subject_id uuid)
returns sg_public.subject as $$
  -- determine all child subjects graph
  with recursive children_graph (version_id, entity_id, path) as (
    select
      s.version_id,
      s.entity_id,
      array[s.entity_id]
    from
      sg_public.subject s
    where
      s.entity_id = subject_id
    union all
    select
      s.version_id,
      s.entity_id,
      cg.path || s.entity_id
    from
      children_graph cg,
      sg_public.subject s,
      sg_public.subject_version_parent_child svpc
    where
      cg.version_id = svpc.child_version_id
      and svpc.parent_entity_id = s.entity_id
  ),
  -- only keep those with direct cards
  filtered as (
    select cg.*, (
      select count(*)
      from sg_public.card c
      where c.subject_id = cg.entity_id
    ) as card_count
    from children_graph cg
    -- where card_count > 0
  ),
  -- count the depth -- how many subjects after this one
  before_graph (version_id, entity_id, path) as (
    select
      s.version_id,
      s.entity_id,
      array[s.entity_id]
    from filtered s
    union all
    select
      s.version_id,
      s.entity_id,
      bg.path || s.entity_id
    from
      before_graph bg,
      sg_public.subject_version_before_after svba,
      sg_public.subject s
    where
      bg.version_id = svba.after_version_id
      and svba.before_entity_id = s.entity_id
  ),
  -- cut inaccessibile subjects -- haven't learned a before > 0.99
  allowed as (
    select *
    from
      before_graph bg
    where (
      select count((
        select r.learned
        from sg_public.select_latest_response(entity_id) r
      ) > 0.99)
      from unnest(bg.path) as entity_id
    ) = array_length(bg.path, 1)
  )
  -- limit 5
  select s.*
  from
    allowed a,
    sg_public.subject s
  where
    a.version_id = s.version_id
  order by
    array_length(a.path, 1) desc
  limit 5;
$$ language sql stable;
comment on function sg_public.select_subject_to_learn(uuid)
  is 'After I select a main subject, search for suitable child subjects.';
grant execute on function sg_public.select_subject_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

