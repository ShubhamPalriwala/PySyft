# relative
from .grammar import GrammarTerm
from .grammar import GrammarVerb
from .grammar import HostGrammarTerm
from .grammar import SourceGrammarTerm
from .names import random_name


def get_launch_verb() -> GrammarVerb:
    full_sentence = [
        {
            "name": "node_name",
            "type": "adjective",
            "klass": GrammarTerm,
            "default": random_name,
            "example": "'My Domain'",
        },
        {
            "name": "node_type",
            "type": "object",
            "klass": GrammarTerm,
            "default": "domain",
            "options": ["domain", "network"],
        },
        {
            "name": "preposition",
            "type": "preposition",
            "klass": GrammarTerm,
            "default": "to",
            "options": ["to"],
        },
        {
            "name": "host",
            "type": "propernoun",
            "klass": HostGrammarTerm,
            "default": "docker",
            "example": "docker:8081+",
        },
        {
            "name": "preposition",
            "type": "preposition",
            "klass": GrammarTerm,
            "default": "from",
            "options": ["from"],
        },
        {
            "name": "source",
            "type": "propernoun",
            "klass": SourceGrammarTerm,
            "default": "github.com/OpenMined/PySyft/tree/demo_strike_team_branch_4",
        },
    ]

    abbreviations = {
        6: [
            "adjective",  # name
            "object",  # node_type
            "preposition",  # to
            "propernoun",  # host
            "preposition",  # from
            "propernoun",  # source
        ],
        5: [
            None,  # name
            "object",  # node_type
            "preposition",  # to
            "propernoun",  # host
            "preposition",  # from
            "propernoun",  # source
        ],
        4: [
            "adjective",  # name
            "object",  # node_type
            "preposition",  # to
            "propernoun",  # host
            None,  # ignore
            None,  # ignore
        ],
        3: [
            None,  # ignore
            "object",  # node_type
            "preposition",  # to
            "propernoun",  # host
            None,  # ignore
            None,  # ignore
        ],
        2: [
            "adjective",  # name
            "object",  # node_type
            None,  # ignore
            None,  # ignore
            None,  # ignore
            None,  # ignore
        ],
        1: [
            None,  # ignore
            "object",  # node_type
            None,  # ignore
            None,  # ignore
            None,  # ignore
            None,  # ignore
        ],
    }

    return GrammarVerb(
        command="launch",
        full_sentence=full_sentence,
        abbreviations=abbreviations,
    )
