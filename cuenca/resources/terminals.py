import datetime as dt
from typing import ClassVar, Optional, cast

from pydantic import BaseModel, Field, StrictStr
from pydantic.dataclasses import dataclass

from .base import Creatable, Queryable, Retrievable, Updateable


class TerminalCreateRequest(BaseModel):  # TO-DO: Move to cuenca_validations
    brand_name: StrictStr
    brand_image: StrictStr
    slug: str = Field(regex=r'^[a-z0-9-_]{5,24}[a-z0-9]$')
    card_active: bool
    cash_active: bool
    spei_active: bool


class TerminalUpdateRequest(BaseModel):  # TO-DO: Move to cuenca_validations
    brand_name: Optional[StrictStr]
    brand_image: Optional[StrictStr]
    slug: Optional[str] = Field(regex=r'^[a-z0-9-_]{5,24}[a-z0-9]$')
    card_active: Optional[bool]
    cash_active: Optional[bool]
    spei_active: Optional[bool]


@dataclass
class Terminal(Queryable, Retrievable, Creatable, Updateable):

    _resource: ClassVar = 'terminal'

    brand_name: str
    brand_image: str
    slug: str  # only alphanumeric, - or _ allowed
    card_active: bool
    cash_active: bool
    spei_active: bool
    stripe_ready: bool  # read-only: Is Stripe setup been fully completed?
    updated_at: dt.datetime  # read-only

    @classmethod
    def create(
        cls,
        brand_name: str,
        slug: str,
        brand_image: Optional[str] = '',
        cash_active: Optional[bool] = True,
        spei_active: Optional[bool] = True,
    ) -> 'Terminal':
        """
        :param brand_name: Commercial brand name for the merchant
        :param brand_image: URL of the image/logo
        :param slug: custom part of the payment URL i.e. cuenca.com/${slug}
        :param card_active: card payments enabled? (requires stripe_ready)
        :param cash_active: cash payments enabled?
        :param spei_active: spei payments enabled?
        :return: Terminal object
        """

        # TO-DO: Support https://feedme.cuenca.io/files

        req = TerminalCreateRequest(
            brand_name=brand_name,
            brand_image=brand_image,
            slug=slug,
            card_active=False,  # Can never be True when creating
            cash_active=cash_active,
            spei_active=spei_active,
        )
        return cast('Terminal', cls._create(**req.dict()))

    @classmethod
    def update(
        cls,
        id: str,
        brand_name: Optional[str] = None,
        slug: Optional[str] = None,
        brand_image: Optional[str] = None,
        card_active: Optional[bool] = None,
        cash_active: Optional[bool] = None,
        spei_active: Optional[bool] = None,
    ) -> 'Terminal':
        """
        :param brand_name: Commercial brand name for the merchant
        :param brand_image: URL of the image/logo
        :param slug: custom part of the payment URL, i.e. cuenca.com/${slug}
        :param card_active: card payments enabled? (requires stripe_ready)
        :param cash_active: cash payments enabled?
        :param spei_active: spei payments enabled?
        :return: Terminal object
        """

        # TO-DO: Support https://feedme.cuenca.io/files

        req = TerminalUpdateRequest(
            brand_name=brand_name,
            brand_image=brand_image,
            slug=slug,
            card_active=card_active,
            cash_active=cash_active,
            spei_active=spei_active,
        )

        return cast('Terminal', cls._update(id, **req.dict(exclude_none=True)))
