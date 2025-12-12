import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Compiles SCSS files to CSS using Sass CLI"

    def add_arguments(self, parser):
        parser.add_argument(
            "--watch",
            action="store_true",
            help="Watch for changes and re-compile automatically",
        )

    def handle(self, *args, **options):
        sass_path = shutil.which("sass") or shutil.which("sass.cmd")

        project_dir = Path(settings.PROJECT_ROOT).resolve()
        static_dir = project_dir / "static" / "css"

        files = [
            ("scss/style.scss", "css/style.css"),
            ("scss/plugins.scss", "css/plugins.css"),
        ]

        # Checa se o Sass está instalado
        try:
            subprocess.run([sass_path, "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as ex:
            raise CommandError(
                "O Sass não está instalado. Instale com: npm install -g sass" + str(ex)
            )

        # Compila cada arquivo
        for scss_name, css_name in files:
            scss_path = static_dir / scss_name
            css_path = static_dir / css_name

            if not scss_path.exists():
                self.stderr.write(self.style.ERROR(f"File not found: {scss_path}"))
                continue

            if options["watch"]:
                cmd = [sass_path, "--watch", str(scss_path), str(css_path)]
                self.stdout.write(f"Watching changes: {scss_path}")
                subprocess.Popen(cmd)
            else:
                cmd = [sass_path, str(scss_path), str(css_path)]
                self.stdout.write(f"Compiling: {scss_name} → {css_name}")
                subprocess.run(cmd, check=True)

        self.stdout.write(self.style.SUCCESS("Compilation finished"))
