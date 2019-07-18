-- migrate:up

drop function if exists sg_public.topic_posts;
alter function sg_public.get_current_user() rename to "current_user";
alter function sg_public.get_anonymous_token() rename to "anonymous_token";
alter function sg_public.new_card(character varying, text, text[], uuid, sg_public.card_kind, jsonb) rename to "create_card";
alter function sg_public.new_subject(character varying, text, text[], text, uuid[], uuid[]) rename to "create_subject";
alter function sg_public.send_email_token(text) rename to "create_email_token";
alter function sg_public.send_password_token(text) rename to "create_password_token";
alter function sg_public.sign_up(text, text, text) rename to "create_user";

-- migrate:down

