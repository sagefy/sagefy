-- migrate:up

create index on "sg_public"."subject_version"("created");
create index on "sg_public"."card_version"("created");

-- migrate:down

