-- migrate:up

create or replace function sg_public.next
  (goal_entity_id uuid, step_entity_id uuid default null)
returns jsonb as $$
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
        return jsonb_build_object(
          'goal', xgoal.entity_id,
          'step', null,
          'next', 'complete_subject'
        );
      end if;
      -- If there's exactly one step level, choose it automatically
      if (array_length(xnext, 1) = 1) then
        return sg_public.next(xgoal.entity_id, xnext[1]);
      end if;
      -- Otherwise, let the learner choose the next step
      return jsonb_build_object(
        'goal', xgoal.entity_id,
        'step', null,
        'next', 'choose_step'
      );
    end if;
    -- If there's a step, and p(learned) < 0.99...
    select * into xcard
    from sg_public.choose_card(xstep.entity_id);
    -- Create a card if there isn't one
    if (xcard is null) then
      return jsonb_build_object(
        'goal', xgoal.entity_id,
        'step', xstep.entity_id,
        'next', 'create_card'
      );
    end if;
    -- Learn a card
    return jsonb_build_object(
      'goal', xgoal.entity_id,
      'step', xstep.entity_id,
      'next', 'learn_card',
      'kind', xcard.kind,
      'card', xcard.entity_id
    );
  end;
$$ language plpgsql;
comment on function sg_public.next(uuid, uuid)
  is 'Determine the next thing to do.';
grant execute on function sg_public.next(uuid, uuid)
  to sg_anonymous, sg_user, sg_admin;

-- More on the row is not null issue...
-- select row(null, null) is null; --> t
-- select row(null, null) is not null; --> f
-- select row(1000, 1000) is null; --> f
-- select row(1000, 1000) is not null; --> t
-- select row(null, 1000) is null; --> f
-- select row(null, 1000) is not null; --> f
-- select not row(null, 1000) is null; --> t
-- In order words, is null and is not null are not inverse operations!
-- For rows, is null checks if all the values are null,
-- while is not null checks if if any value is null.

-- migrate:down

drop function if exists sg_public.next(uuid, uuid);
