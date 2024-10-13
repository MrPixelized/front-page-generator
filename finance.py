from util import *
from dataclasses import dataclass


Account = str
CurrencyAmount = List[str]


def read_hledger_csv(data):
    f = {}
    current = {}

    for row in data:
        identifier = row[0].lstrip("<").rstrip(">").lower()

        if identifier in {"assets", "liabilities", "net:", "account", "total:",
                          "expenses", "equity", "unbudgeted"}:
            current = dict()
            f[identifier.rstrip(":")] = current
            identifier = "total"

        if not any(row[1:]):
            continue

        current[identifier] = [field.split(", ") for field in row][1:]

    return f
        


@dataclass
class BalanceSheet:
    liabilities: Dict[Account, List[CurrencyAmount]]
    assets: Dict[Account, List[CurrencyAmount]]
    net: List[CurrencyAmount]

    @classmethod
    def from_hledger(cls, *args, **kwargs):
        data = csv_from_subprocess("hledger", "bs", output_format="csv", *args, **kwargs)

        f = read_hledger_csv(data)

        return cls(
            liabilities=f["liabilities"],
            assets=f["assets"],
            net=f["net"],
        )

    def __str__(self):
        return json.dumps(asdictify(self))


@dataclass
class BudgetIndication:
    used: List[CurrencyAmount]
    total: List[CurrencyAmount]

    def __post_init__(self):
        for i, (amount_used, amount_total) in enumerate(zip(self.used, self.total)):
            if not amount_used:
                self.used[i] = "0.00 " + amount_total.split()[-1]


@dataclass
class BudgetSheet:
    budgets: Dict[Account, BudgetIndication]
    #  net: BudgetIndication

    @classmethod
    def from_hledger(cls, *args, **kwargs):
        data = csv_from_subprocess("hledger", "bal", "--budget", output_format="csv", p="since this month", *args, **kwargs)

        f = read_hledger_csv(data)

        #  f["expenses"].pop("total")

        budgets = {k: BudgetIndication(*v) for k, v in f["expenses"].items()}
        budgets["total"] = budgets["total"]
        #  budgets["total"] = BudgetIndication(*f["total"]["total"])

        return cls(
            budgets=budgets,
        )
