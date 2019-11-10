from codes import subdiv_codes


class SubdivModel():

    def __init__(self, subdiv_code, description):
        self.subdiv_code = subdiv_code
        self.description = description

    @classmethod
    def find_by_code(cls, subdiv_code):
        # error handling
        if subdiv_code in subdiv_codes:
            return {'subdiv_code': subdiv_code, 'description': subdiv_codes[subdiv_code]}
        return None
