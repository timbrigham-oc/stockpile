import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

class BaseRequirement:

    # Define logging for parsers derived from BaseReqirement. 
    # Make these class wide. This also needs applied to the parsers which don't inherit from this class. 
    format = "%(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    console = Console(theme=Theme({"logging.level.warning": "yellow"}))
    level=logging.DEBUG
    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        handlers=[RichHandler(rich_tracebacks=True, markup=True, console=console)]
    )

    for logger_name in logging.root.manager.loggerDict.keys():
        if logger_name in ("aiohttp.server", "asyncio"):
            continue
        else:
            logging.getLogger(logger_name).setLevel(100)
    logging.getLogger("markdown_it").setLevel(logging.WARNING)
    logging.captureWarnings(True)



    def __init__(self, requirement_info):
        self.enforcements = requirement_info['enforcements']

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
