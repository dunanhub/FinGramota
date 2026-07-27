from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from marketplace.services.product_sync import ProductSyncService


class Command(BaseCommand):
    help = 'Import marketplace products from a completed local VBR capture.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--input-dir',
            default='/app/.vbr-pages/latest',
            help='Directory containing manifest.json and captured VBR pages.',
        )

    def handle(self, *args, **options):
        input_directory = Path(options['input_dir'])
        if not input_directory.exists():
            raise CommandError(f'Input directory does not exist: {input_directory}')
        try:
            result = ProductSyncService().sync_from_directory(input_directory)
        except (OSError, ValueError) as error:
            raise CommandError(str(error)) from error
        self.stdout.write(
            self.style.SUCCESS(
                'Marketplace sync completed: '
                f'created={result.created}, updated={result.updated}, '
                f'skipped={result.skipped}, deactivated={result.deactivated}'
            )
        )
