-- migrate:up

create index card_version_distinct_idx
on sg_public.card_version (entity_id, created desc)
where status = 'accepted';

create index subject_version_distinct_idx
on sg_public.subject_version (entity_id, created desc)
where status = 'accepted';

-- migrate:down

