import sys

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = """
    Command to calculate n'th number of fibonacci sequence
    Usage: python manage.py fibo [number]
    Function works very fast because it save cached numbers
    """

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **options):
        number: int = options['number']

        if number < 0:
            self.stderr.write(
                self.style.ERROR("Invalid number please enter positive int number")
            )
            sys.exit(-1)

        nums = [0] * number
        nums[0], nums[1] = 0, 1

        for i in range(2, number):
            nums[i] = nums[i - 1] + nums[i - 2]
        self.stdout.write(
            self.style.SUCCESS(f"Successfully calculated {number}'th number of fibonacci sequence:\n{nums[number - 1]}")
        )
