-- migrate:up

CREATE OR REPLACE FUNCTION slugify("value" TEXT)
RETURNS TEXT AS $$
  -- from https://www.kdobson.net/2019/ultimate-postgresql-slug-function/
  -- removes accents (diacritic signs) from a given string --
  WITH "unaccented" AS (
    SELECT unaccent("value") AS "value"
  ),
  -- lowercases the string
  "lowercase" AS (
    SELECT lower("value") AS "value"
    FROM "unaccented"
  ),
  -- remove single and double quotes
  "removed_quotes" AS (
    SELECT regexp_replace("value", '[''"]+', '', 'gi') AS "value"
    FROM "lowercase"
  ),
  -- replaces anything that's not a letter, number, hyphen('-'), or underscore('_') with a hyphen('-')
  "hyphenated" AS (
    SELECT regexp_replace("value", '[^a-z0-9\\-_]+', '-', 'gi') AS "value"
    FROM "removed_quotes"
  ),
  -- trims hyphens('-') if they exist on the head or tail of the string
  "trimmed" AS (
    SELECT regexp_replace(regexp_replace("value", '\-+$', ''), '^\-', '') AS "value"
    FROM "hyphenated"
  )
  SELECT "value" FROM "trimmed";
$$ LANGUAGE SQL STRICT IMMUTABLE;
comment on function slugify(text)
  is 'Given a string, turn it into a URL slug.';
grant execute on function slugify(text)
  to sg_anonymous, sg_user, sg_admin;



create or replace function sg_public.subject_slug(subject sg_public.subject)
returns text as $$
  select slugify(subject.name);
$$ language sql stable;
comment on function sg_public.subject_slug(sg_public.subject)
  is 'The subject''s name as a slug, for URLs.';
grant execute on function sg_public.subject_slug(sg_public.subject)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

