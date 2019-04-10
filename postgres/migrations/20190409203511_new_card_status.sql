-- migrate:up

-- Nota bene that this is intended to be _temporary_.
create or replace function sg_private.insert_card_version_status()
returns trigger as $$
begin
  new.status = 'accepted'::sg_public.entity_status;
  return new;
end;
$$ language plpgsql strict security definer;
comment on function sg_private.insert_card_version_status()
  is 'When inserting a new card, '
     'automatically set the status to accepted.';

create trigger insert_card_version_status
  before insert on sg_public.card_version
  for each row execute procedure sg_private.insert_card_version_status();
comment on trigger insert_card_version_status
  on sg_public.card_version
  is 'When inserting a new card, '
     'automatically set the status to accepted.';

-- And this is more permanent...
create or replace function sg_public.subject_by_entity_id(entity_id uuid)
returns sg_public.subject as $$
  select s.*
  from sg_public.subject s
  where s.entity_id = $1
  limit 1;
$$ language sql stable;
comment on function sg_public.subject_by_entity_id(uuid)
  is 'Get a subject by entity id.';
grant execute on function sg_public.subject_by_entity_id(uuid)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

