import base64

import bcrypt
import jsons

SECRET_NATIONAL_ID_SALT = "SECRET_NATIONAL_ID_SALT"


class Ballot:
    """
    A ballot that exists in a specific, secret manner
    """

    def __init__(self, ballot_number: str, chosen_candidate_id: str, voter_comments: str):
        self.ballot_number = ballot_number
        self.chosen_candidate_id = chosen_candidate_id
        self.voter_comments = voter_comments


def generate_ballot_number(national_id: str, salt: str = None) -> str:
    """
    Produces a ballot number. Feel free to add parameters to this method, if you feel those are necessary.

    Remember that ballot numbers must respect the following conditions:

    1. Voters can be issued multiple ballots. This can be because a voter might make a mistake when filling out one
       ballot, and therefore might need an additional ballot. However it's important that only one ballot per voter is
       counted.
    2. All ballots must be secret. Voters have the right to cast secret ballots, which means that it should be
       technically impossible for someone holding a ballot to associate that ballot with the voter.
    3. In order to minimize the risk of fraud, a nefarious actor should not be able to tell that two different ballots
       are associated with the same voter.

    :return: A string representing a ballot number that satisfies the conditions above
    """
    sanitized_national_id = national_id.replace("-", "").replace(" ", "").strip()
    if not salt:
        salt = bcrypt.gensalt()
    ballot_hash = bcrypt.hashpw(sanitized_national_id.encode("utf-8"), salt).decode("utf-8")
    encoded_salt = base64.b64encode(salt).decode("utf-8")
    json_string = jsons.dumps({"ballot": ballot_hash, "salt": encoded_salt})
    return base64.b64encode(json_string.encode("utf-8")).decode("utf-8")
