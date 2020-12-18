from pony.orm import *
from tor_db.db import db
import tor_db.models.domain


class BitcoinAddress(db.Entity):
    _table_ = "bitcoin_address"
    address = Required(str, 100, unique=True)
    pages = Set(
        "Page", reverse="bitcoin_addresses", column="page", table="bitcoin_address_link"
    )

    def domains(self):
        return select(
            d
            for d in tor_db.models.domain.Domain
            for p in d.pages
            for b in p.bitcoin_addresses
            if b == self
        )

    @db_session
    def get_all():
        return select(
            d
            for d in tor_db.models.domain.Domain
            for p in d.pages
            for b in p.bitcoin_addresses
            if b is not None
        )
