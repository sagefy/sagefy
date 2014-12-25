from mock import main as create_responses
from formulae import update, init_learned, init_belief, \
    init_guess, init_slip  # , init_transit


def main(num_learners=26, num_cards=10):
    d = create_responses(num_learners, num_cards)
    responses, learners, cards = d['responses'], d['learners'], d['cards']

    my_cards = [{
        'name': card['name'],
        'guess': init_guess,
        'slip': init_slip,
        'transit': card['transit'],  # TODO instead use init_transit,
    } for card in cards]

    my_learners = [{
        'name': learner['name'],
        'learned': init_learned,
        'belief': init_belief,
    } for learner in learners]

    for i, response in enumerate(responses):
        # response keys: learner, card, time, score

        prev_response = get_previous_response(responses, i)
        my_learner = [ml for ml in my_learners
                      if ml['name'] == response['learner']][0]
        my_card = [mc for mc in my_cards
                   if mc['name'] == response['card']][0]

        c = update(learned=my_learner['learned'],
                   belief=my_learner['belief'],
                   guess=my_card['guess'],
                   slip=my_card['slip'],
                   transit=my_card['transit'],
                   score=response['score'],
                   time=response['time'],
                   prev_time=prev_response['time'],
                   prev_learned=0,  # TODO
                   prev_transit=0)  # TODO
        print(c)

        my_learner['learned'] = c['learned']
        my_learner['belief'] = c['belief']
        my_card['guess'] = c['guess']
        my_card['slip'] = c['slip']
        # TODO my_card['transit'] = c['transit']

    print('CARDS')
    for mc in my_cards:
        card = [card for card in cards if card['name'] == mc['name']][0]
        print(
            card['name'],
            my_card['guess'] - card['guess'],
            my_card['slip'] - card['slip'],
        )

    # print('LEARNERS')
    # for ml in my_learners:
    #     print(
    #         ml['name'],
    #         ml['learned'],
    #         ml['belief']
    #     )


def get_previous_response(responses, i):
    learner = responses[i]['learner']
    while True:
        i -= 1
        if responses[i]['learner'] == learner:
            return responses[i]


if __name__ == '__main__':
    main()
