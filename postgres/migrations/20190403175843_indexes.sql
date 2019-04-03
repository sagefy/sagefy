-- migrate:up

-- Create indexes to clear out Postgraphile warnings.

create index on "sg_public"."card_version"("entity_id");
create index on "sg_public"."card_version"("previous_id");
create index on "sg_public"."card_version"("user_id");
create index on "sg_public"."card_version"("subject_id");
create index on "sg_public"."subject_version"("entity_id");
create index on "sg_public"."subject_version"("previous_version_id");
create index on "sg_public"."subject_version"("user_id");
create index on "sg_public"."subject_version_parent_child"("parent_entity_id");
create index on "sg_public"."subject_version_before_after"("before_entity_id");
create index on "sg_public"."user_subject"("subject_id");

-- migrate:down

