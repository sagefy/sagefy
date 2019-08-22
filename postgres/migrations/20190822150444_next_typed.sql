-- migrate:up

create type sg_public.next_option as enum (
  'complete_subject',
  'choose_step',
  'create_card',
  'learn_card'
);
comment on type sg_public.next_option
  is 'List of next page options.';

create type sg_public.next_page as (
  goal uuid,
  step uuid,
  next sg_public.next_option,
  kind sg_public.card_kind,
  card uuid
);
comment on type sg_public.next_page
  is 'Describes the next page to go to in the experience.';

drop function sg_public.next;

create or replace function sg_public.next
  (goal_entity_id uuid, step_entity_id uuid default null)
returns sg_public.next_page as $$
  declare
    xgoal sg_public.subject;
    xstep sg_public.subject;
    xcard sg_public.card;
    xnext uuid[];
  begin
    -- First we'll validate the goal by selecting it
    select s.* into xgoal
    from sg_public.subject s
    where s.entity_id = goal_entity_id;
    -- Select the step if it exists
    select s.* into xstep
    from sg_public.subject s
    where s.entity_id = step_entity_id;
    -- Always attempt to add the goal to user_subject
    insert into sg_public.user_subject (subject_id)
    values (xgoal.entity_id)
    on conflict do nothing;
    -- If there's no step, or p(learned >= 0.99)..
    -- -- Nota bene: `row(...) is not null` behaves unexpectedly! Beware!
    if (xstep is null or sg_public.subject_learned(xstep) >= 0.99) then
      -- We need to choose the next step...
      xnext := array(
        select entity_id
        from sg_public.subject_next_child_subjects(xgoal)
      );
      -- If there's no next step, then we are done
      if (array_length(xnext, 1) is null) then
        return (
          xgoal.entity_id,
          null,
          'complete_subject'::sg_public.next_option,
          null,
          null
        )::sg_public.next_page;
      end if;
      -- If there's exactly one step level, choose it automatically
      if (array_length(xnext, 1) = 1) then
        return sg_public.next(xgoal.entity_id, xnext[1]);
      end if;
      -- Otherwise, let the learner choose the next step
      return (
        xgoal.entity_id,
        null,
        'choose_step'::sg_public.next_option,
        null,
        null
      )::sg_public.next_page;
    end if;
    -- If there's a step, and p(learned) < 0.99...
    select * into xcard
    from sg_public.choose_card(xstep.entity_id);
    -- Create a card if there isn't one
    if (xcard is null) then
      return (
        xgoal.entity_id,
        xstep.entity_id,
        'create_card'::sg_public.next_option,
        null,
        null
      )::sg_public.next_page;
    end if;
    -- Learn a card
    return (
      xgoal.entity_id,
      xstep.entity_id,
      'learn_card'::sg_public.next_option,
      xcard.kind,
      xcard.entity_id
    )::sg_public.next_page;
  end;
$$ language plpgsql;
comment on function sg_public.next(uuid, uuid)
  is 'Determine the next thing to do.';
grant execute on function sg_public.next(uuid, uuid)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

