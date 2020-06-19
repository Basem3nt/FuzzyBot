class BasicNLP:
    
    @staticmethod
    def messenger_nlp(nlp):
        """
        great nlp function of all time. Does nothing but parsing. lOl
        this function will return a tuple of (None, None) if it does not match the usual
        otherwise, it will return in the format of (<REPLY>, <NLP_CLASSIFICATION>)

        nlp: nlp stuffs receives from Facebook

        return: returns a str and state in a tuple. example: "Hello", "greetings" where "greetings" state that it is conversation initializer and "Hello" is the appropriate reply for this state.
        """
        KEYWORDS = ['bye', 'thanks', 'greetings']
        VALUE_DICTIONARY = {
            'bye': -1,
            'thanks': -1,
            'greetings': -1,
        }
        entities = nlp['entities'] if 'entities' in nlp else None

        if entities is not None:
            for key in entities:
                if key in KEYWORDS:
                    nlp_val = entities[key]
                    if type(nlp_val) == list and len(nlp_val) > 0:
                        if 'confidence' in nlp_val[0]:
                            VALUE_DICTIONARY[key] = nlp_val[0]['confidence']

            if VALUE_DICTIONARY['thanks'] > VALUE_DICTIONARY['bye'] \
                    and VALUE_DICTIONARY['thanks'] > VALUE_DICTIONARY['greetings'] \
                    and VALUE_DICTIONARY['thanks'] >= 0.70:
                return "You are most welcome.", "thanks"
            elif VALUE_DICTIONARY['bye'] > VALUE_DICTIONARY['thanks'] \
                    and VALUE_DICTIONARY['bye'] > VALUE_DICTIONARY['greetings'] \
                    and VALUE_DICTIONARY['bye'] >= 0.70:
                return "Bye bye. Have a nice day.", "bye"
            else:
                if VALUE_DICTIONARY['greetings'] >= 0.70:
                    return "Hello", "greetings"
        return (None, None)
