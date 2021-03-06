from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from cuenca_validations.types import DepositNetwork

from .accounts import Account
from .base import Transaction
from .resources import retrieve_uri


@dataclass
class Deposit(Transaction):
    _resource: ClassVar = 'deposits'

    network: DepositNetwork
    source_uri: Optional[str]
    tracking_key: Optional[str]  # clave rastreo if network is SPEI

    @property  # type: ignore
    def source(self) -> Optional[Account]:
        if self.source_uri is None:  # cash deposit
            acct = None
        else:
            acct = cast(Account, retrieve_uri(self.source_uri))
        return acct
