import math
import sys
from argparse import ArgumentParser

"""
Loan Calculator.

Project implementation from Hyperskill.
See https://hyperskill.org/projects/90
"""


def get_args():
    """Parse command line arguments to get the loan parameters"""
    parser = ArgumentParser(description="A simple loan parser")
    parser.add_argument("--payment", help="The payment amount")
    parser.add_argument("--principal", help="The principal loan amount")
    parser.add_argument("--periods", help="Number of months needed to repay the loan")
    parser.add_argument("--interest", help="Interest rate. Mandatory argument")
    parser.add_argument(
        "--type",
        help="Type of payment. Must be annuity or diff.",
    )
    args = parser.parse_args()

    # Check the parameters' validity
    if (
            args.type is None
            or (args.type not in ["annuity", "diff"])
            or (args.type == "diff" and args.payment is not None)
            or (args.interest is None)
            or len(sys.argv) < 5
            or some_arg_is_negative([args.principal, args.payment, args.periods, args.interest])
    ):
        raise ValueError("Incorrect parameters")

    return args


def some_arg_is_negative(args):
    """Check if one of the parameter is a negative number"""
    try:
        for arg in args:
            if arg is not None and float(arg) < 0:
                return True
    except ValueError:
        return False

    return False


def compute_nominal_rate(interest_rate):
    """Compute nominal (monthly) interest rate"""
    return interest_rate * 0.01 / 12


def compute_period_ratio(periods, nominal_rate):
    """Compute the period ratio. Intermediate calculation used in other methods"""
    return (nominal_rate * math.pow(1 + nominal_rate, periods)
            / (math.pow(1 + nominal_rate, periods) - 1)
            )


def compute_annuity_payment(principal, periods, nominal_rate):
    """Compute the annuity payment"""
    return math.ceil(principal * compute_period_ratio(periods, nominal_rate))


def compute_periods(principal, payment, nominal_rate):
    """Compute the periods (number of months needed to repay the loan"""
    return math.ceil(
        math.log(payment / (payment - nominal_rate * principal),
                 1 + nominal_rate
                 ))


def compute_principal(payment, periods, nominal_rate):
    return math.floor(payment / compute_period_ratio(periods, nominal_rate))


def print_periods(periods):
    years = periods // 12
    months = periods % 12
    message = "It will take "
    if years > 0:
        message += str(years) + " year" + ("s" if years > 1 else "")
    if months > 0 and years > 0:
        message += " and "
    if months > 0:
        message += str(months) + " month " + ("s" if months > 1 else "")
    message += " to repay this loan!"
    print(message)


def print_annuity(annuity_payment, overpayment):
    """Print annuity payment"""
    print(f"Your monthly payment = {annuity_payment}!")
    print(overpayment)


def print_principal(principal):
    print(f"Your loan principal = {principal}!")


def compute_diff_payment(principal, periods, nominal_rate):
    """Compute differentiate payments """
    payments = []
    for m in range(0, periods):
        month = m + 1
        payment = math.ceil(principal / periods
                   + nominal_rate * (principal - (principal * (month - 1) / periods)))
        payments.append(payment)
    return payments


def compute_diff_overpayment(principal, payments):
    """Get the overpayment value for differentiated loans."""
    return math.floor(sum(payments) - principal)


def compute_annuity_overpayment(principal, annuity, periods):
    """Get the overpayment value for annuity loans."""
    return math.floor((annuity * periods) - principal)


def print_diff_payments(payments, overpayment):
    """Prints the differentiated monthly payments."""
    for i in range(0, len(payments)):
        payment = payments[i]
        print(f"Month {i}: {payment}")
    print_overpayment(overpayment)



def print_overpayment(overpayment):
    print()
    print(f"Overpayment = {overpayment}")


def main():
    """Main program."""
    try:
        args = get_args()
    except ValueError:
        print("Incorrect parameters")
        exit()

    nominal_rate = compute_nominal_rate(float(args.interest))
    if args.payment is None:
        if args.type == "annuity":
            annuity = compute_annuity_payment(float(args.principal), int(args.periods), nominal_rate)
            overpayment = compute_annuity_overpayment(float(args.principal), annuity, int(args.periods))
            print_annuity(annuity, overpayment)
        elif args.type == "diff":
            payments = compute_diff_payment(float(args.principal), int(args.periods), nominal_rate)
            overpayment = compute_diff_overpayment(float(args.principal), payments)
            print_diff_payments(payments, overpayment)

    elif args.periods is None:
        periods = compute_periods(float(args.principal), float(args.payment), nominal_rate)
        if args.type == "diff":
            overpayment = compute_diff_overpayment(float(args.principal), float(args.payments))
        else:
            overpayment = compute_annuity_overpayment(float(args.principal), float(args.payment), periods)
        print_periods(periods)
        print_overpayment(overpayment)

    elif args.principal is None:
        principal = compute_principal(float(args.payment), int(args.periods), nominal_rate)
        if args.type == "diff":
            overpayment = compute_diff_overpayment(principal, float(args.payments))
        else:
            overpayment = compute_annuity_overpayment(principal, float(args.payment), int(args.periods))
        print_principal(principal)
        print_overpayment(overpayment)


if __name__ == "__main__":
    main()
