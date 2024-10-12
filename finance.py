from util import *
from dataclasses import dataclass


@dataclass
class BalanceSheet:
    liabilities: Dict
    assets: Dict
    net: str

    @classmethod
    def from_hledger(cls, *args, **kwargs):
        data = csv_from_subprocess("hledger", "bs", output_format="csv", *args, **kwargs)

        f = {}
        current = {}

        for row in data:
            identifier = row[0].strip(":").lower()

            if identifier in ["assets", "liabilities", "net", "account"]:
                current = dict()
                f[row[0].strip(":").lower()] = current
                row[0] = "total"

            if not row[1]:
                continue

            current[row[0]] = row[1].split(", ")
        
        return cls(
            liabilities=f["liabilities"],
            assets=f["assets"],
            net=f["net"],
        )

    def __str__(self):
        return json.dumps(asdictify(self))
