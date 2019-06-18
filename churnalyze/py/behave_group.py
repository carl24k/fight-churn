
import sys

from churn_calc import  ChurnCalculator


def main():
    schema = 'b'
    if len(sys.argv) >= 2:
        schema = sys.argv[1]

    churn_calc = ChurnCalculator(schema)

    churn_calc.calc_behavior_groups()

if __name__ == "__main__":

    main()
