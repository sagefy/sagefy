const db = require('./index')

/*

CREATE TABLE responses (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id uuid NOT NULL REFERENCES users (id),
  card_id uuid NOT NULL REFERENCES cards_entity_id (entity_id),
  unit_id uuid NOT NULL REFERENCES units_entity_id (entity_id),
  response text NOT NULL,
  score double precision NOT NULL CHECK (score >= 0 AND score <= 1),
  learned double precision NOT NULL CHECK (score >= 0 AND score <= 1)
);

*/

async function getLatestResponse(userId, unitId) {}

async function insertResponse(data) {}

module.exports = {
  getLatestResponse,
  insertResponse,
}
