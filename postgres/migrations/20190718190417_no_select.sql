-- migrate:up

alter function sg_public.select_popular_subjects() rename to "popular_subjects";
alter function sg_public.select_card_to_learn(uuid) rename to "choose_card";

-- Remove the old functions

drop function if exists sg_public.select_latest_response;
drop function if exists sg_public.select_subject_learned;
drop function if exists sg_public.select_subject_to_learn;

-- Create the new functions

create or replace function sg_public.subject_latest_response(subject sg_public.subject)
returns sg_public.response as $$
  select r.*
  from sg_public.response r
  where r.subject_id = $1.entity_id and (
    user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
    or session_id = nullif(current_setting('jwt.claims.session_id', true), '')::uuid
  )
  order by r.created desc
  limit 1;
$$ language sql stable;
comment on function sg_public.subject_latest_response(sg_public.subject)
  is 'Get the latest response from the user on the given subject.';
grant execute on function sg_public.subject_latest_response(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_learned(subject sg_public.subject)
returns real as $$
  select case when learned is not null then learned else 0.4 end
  from sg_public.subject_latest_response($1);
$$ language sql stable;
comment on function sg_public.subject_learned(sg_public.subject)
  is 'Get the latest learned value for the user on the given subject.';
grant execute on function sg_public.subject_learned(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.subject_next_child_subjects(subject sg_public.subject)
returns setof sg_public.subject as $$
  with subject as (
    select *
    from sg_public.subject
    where entity_id = $1.entity_id
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
    and sg_public.subject_learned(s) < 0.99
    and not sg_public.subject_has_needed_before(s, e.all_subjects)
    -- TODO support "rewind"... going into out of goals befores
    -- when performance is low.
  order by
    sg_public.subject_all_after_count(s) desc,
    sg_public.subject_card_count(s) desc
  limit 5;
$$ language sql stable;
comment on function sg_public.subject_next_child_subjects(sg_public.subject)
  is 'After I select a main subject, search for suitable child subjects.';
grant execute on function sg_public.subject_next_child_subjects(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;


-- Update depending functions

create or replace function sg_public.subject_has_needed_before(sg_public.subject, uuid[])
returns boolean as $$
  select exists(
    select x.entity_id
    from sg_public.subject_before_subjects($1) x
    where sg_public.subject_learned(x) < 0.99
    and x.entity_id = any($2)
  );
$$ language sql stable;

create or replace function sg_private.score_response()
returns trigger as $$
  declare
    card sg_public.card;
    subject sg_public.subject;
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
    select s.* into subject
    from sg_public.subject s
    where entity_id = card.subject_id;
    prior_learned := (select sg_public.subject_learned(subject));
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

create or replace function sg_public.choose_card(subject_id uuid)
returns sg_public.card as $$
  declare
    xsubject sg_public.subject;
    xprior sg_public.response;
    kinds sg_public.card_kind[];
    xcard sg_public.card;
  begin
    select * into xsubject
    from sg_public.subject
    where entity_id = $1;
    select * into xprior
    from sg_public.subject_latest_response(xsubject);
    if (random() < (0.5 + 0.5 * sg_public.subject_learned(xsubject))) then
      kinds := array['choice'];
    else
      kinds := array['video', 'page', 'unscored_embed'];
    end if;
    select c.* into xcard
    from sg_public.card c
    where c.subject_id = $1
      and c.kind = any(kinds)
      and (xprior.card_id is null or c.entity_id <> xprior.card_id)
      and random() < sg_public.subject_card_count(xsubject) / 10::real
    order by random()
    limit 1;
    return xcard;
  end;
  -- Future version: When estimating parameters and the card kind is scored,
  -- prefer 0.25 < correct < 0.75
$$ language plpgsql;


-- migrate:down

