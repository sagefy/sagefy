-- migrate:up

alter table sg_public.card_version
drop constraint card_version_previous_id_fkey;

ALTER TABLE ONLY sg_public.card_version
    ADD CONSTRAINT card_version_previous_id_fkey FOREIGN KEY (previous_id) REFERENCES sg_public.card_version(version_id)
    ON DELETE CASCADE;

-- migrate:down
