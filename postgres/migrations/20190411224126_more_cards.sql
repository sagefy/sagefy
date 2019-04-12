-- migrate:up

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
  ),
  xsubject as (select * from sg_public.subject where entity_id = $1),
  r (rand) as (select random())
  select c.*
  from sg_public.card c, prior, k, xsubject, r
  where c.subject_id = $1
    and c.kind = any(k.kinds)
    and (prior.card_id is null or c.entity_id <> prior.card_id)
    and r.rand < sg_public.subject_card_count(xsubject) / 10::real
  order by random()
  limit 1;
  -- Future version: When estimating parameters and the card kind is scored,
  -- prefer 0.25 < correct < 0.75
$$ language sql volatile;


-- migrate:down

