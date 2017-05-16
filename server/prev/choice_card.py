from random import shuffle


class ChoiceCard():
    def validate_response(self, response):
        """
        Ensure the given response body is valid,
        given the card information.
        """

        # If not a choice card, return [{'message': 'No response is valid.'}]

        values = [opt['value'] for opt in self['options']]

        if response not in values:
            return [{'message': 'Value is not an option.'}]

        return []

    def score_response(self, response):
        """
        Score the given response.
        Returns the score and feedback.
        """

        # If not a choice card, raise Exception("No method implemented.")

        for opt in self['options']:
            if response == opt['value']:
                if opt['correct']:
                    return 1.0, opt['feedback']
                else:
                    return 0.0, opt['feedback']

        return 0.0, 'Default error ajflsdvco'

    def deliver(self, access=None):
        """
        Overwrite to randomize option order and limit number of options.
        """

        data = super().deliver(access)

        if access is 'learn':
            if self['order'] == 'random':
                shuffle(data['options'])

            if self['max_options_to_show']:
                data['options'] = data['options'][:self['max_options_to_show']]

        return data
