import logging

class BaseRequirement:

    def __init__(self, requirement_info):
        self.enforcements = requirement_info['enforcements']
        # Define logging for parsers derived from BaseReqirement. 
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
        self.log.info('Initializing BaseParser instance with name: %s', __name__ )

    def is_valid_relationship(self, used_facts, relationship):
        """
        Checks if the used facts for a link match with the list of known fact relationships
        :param used_facts:
        :param relationship:
        :return: True if there is a match, False if not
        """
        if not self._check_edge(relationship.edge):
            return False
        if 'target' in self.enforcements.keys():
            for fact in used_facts:
                if self._check_target(relationship.target, fact):
                    return True
            return False
        return True

    """ PRIVATE """

    @staticmethod
    def _get_relationships(uf, relationships):
        return [r for r in relationships if r.source.trait == uf.trait and r.source.value == uf.value]

    @staticmethod
    def _check_target(target, match):
        if target.trait == match.trait and target.value == match.value:
            return True
        return False

    def _check_edge(self, edge):
        if edge == self.enforcements['edge']:
            return True
        return False
