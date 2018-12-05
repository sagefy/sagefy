// Looking at a single unit...

//// Constants /////////////////////////////////////////////////////////////////

const INIT_GUESS = 0.3
const INIT_SLIP = 0.1
const INIT_LEARNED = 0.4
const MAX_LEARNED = 0.99
const INIT_TRANSIT = 0.05

//// Formulas //////////////////////////////////////////////////////////////////

function calculateCorrect(guess, slip, learned) {
  return learned * (1 - slip) + (1 - learned) * guess
}

function calculateIncorrect(guess, slip, learned) {
  return learned * slip + (1 - learned) * (1 - guess)
}

function updateLearned({ score, learned, guess, slip, transit }) {
  const posterior =
    score 
      * calculateCorrect(0, slip, learned) 
      / calculateCorrect(guess, slip, learned)
    + (1 - score) 
      * calculateIncorrect(0, slip, learned) 
      / calculateIncorrect(guess, slip, learned)
  return posterior + (1 - posterior) * transit
}

function mean (arr) {
  return arr.reduce((sum, val) => sum + val, 0) / arr.length
}

function error (cards, param, realParam) {
  return mean(cards.map(card => (card[param] - card[realParam]) ** 2))
}

function control (cards, realParam, init) {
  return mean(cards.map(card => (init - card[realParam]) ** 2))
}

function around(value) {
  return value + Math.random() * value - 0.5 * value
}

function choose(arr) {
  return arr[Math.floor(Math.random() * arr.length)]
}

//// Mock //////////////////////////////////////////////////////////////////////

function createCards(numCards = 50) {
  return [...Array(numCards).keys()]
    .map(i => ({
      name: i,
      realGuess: around(INIT_GUESS),
      guess: INIT_GUESS,
      realSlip: around(INIT_SLIP),
      slip: INIT_SLIP,
      realTransit: around(INIT_TRANSIT),
      transit: INIT_TRANSIT,
      responses: [],
    }))
}

function createLearners(numLearners = 10000) {
  return [...Array(numLearners).keys()]
    .map(i => ({ name: i, learned: INIT_LEARNED }))
}

//// Simluate //////////////////////////////////////////////////////////////////

function getScore(learner, card) {
  const correct = calculateCorrect(
    card.realGuess, 
    card.realSlip, 
    learner.learned
  )
  return +(correct > Math.random())
}

function updateLearner(learner, params) {
  learner.learned = updateLearned(params)
}

function updateCard(card) {
  // THIS IS WHERE THE EXPERIMENT OCCURS!!!
  // card.guess = ???
  // card.slip = ???
  // card.transit = ???

  function calcGuess({ score, learned, guess, slip, transit }) {
    if (score === 0) return 0
    return 1 - learned
  }

  function calcSlip({ score, learned, guess, slip, transit }) {
    if (score === 1) return 0
    return learned
  }

  function calcTransit({ score, learned, guess, slip, transit }) {
    if (score === 1) return 0
    return learned
  }

  card.guess = card.responses.length > 30
    ? mean(card.responses.map(calcGuess))
    : INIT_GUESS
    
  card.slip = card.responses.length > 30
    ? mean(card.responses.map(calcSlip))
    : INIT_SLIP

  card.transit = card.responses.length > 30
    ? mean(card.responses.map(calcTransit))
    : INIT_TRANSIT
}

function simulate(rounds = 10000000) {
  const cards = createCards()
  const learners = createLearners()

  for (let i = 0; i < rounds; i++) {
    const card = choose(cards)
    const learner = choose(learners)

    if (learner.learned > MAX_LEARNED) continue

    const score = getScore(learner, card)

    card.responses.push({
      learned: learner.learned,
      score,
      guess: card.guess,
      slip: card.slip,
      transit: card.transit,
    })

    // Update learner
    updateLearner(learner, { 
      score, 
      learned: learner.learned,
      guess: card.guess,
      slip: card.slip,
      transit: card.transit
    })

    // Update card
    updateCard(card)

    // console.log(i, learner, card)
  }

  return { cards, learners }
}

//// Result ////////////////////////////////////////////////////////////////////

if (require.main === module) {
  const { cards, learners } = simulate()
  // The goal is to beat `1`.
  console.log('guess', 
    error(cards, 'guess', 'realGuess')
    / control(cards, 'realGuess', INIT_GUESS)
  )
  console.log('slip', 
    error(cards, 'slip', 'realSlip')
    / control(cards, 'realSlip', INIT_SLIP)
  )
  console.log('transit', 
    error(cards, 'transit', 'realTransit')
    / control(cards, 'realTransit', INIT_TRANSIT)
  )
}
