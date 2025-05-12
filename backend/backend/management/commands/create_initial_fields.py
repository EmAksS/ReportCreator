from django.core.management import BaseCommand
from backend.scripts import initial_fields as ini
from backend.models.fields import Field

class Command(BaseCommand):
    help = "Load initial fields from backend.scripts.initial_fields into Fields model."

    def handle(self, *args, **options):
        for i, dic in enumerate(ini.ALL_ITEMS):
            print(f"Cheching values from {ini.STR_ITEMS[i]}:", end='\t')
            added_fields = []
            for field in dic:
                # Так как могут быть добавлены новые поля, `get_or_create` не подходит. 
                # Вмето этого нужно овершать проверку по ключевым полям и создавать поля только если они есть.
                if not Field.objects.filter(key_name=field['key_name'], related_item=field['related_item']).exists():
                    Field.objects.create(
                        id=f"{field['key_name']}__{field['related_item']}",
                        is_custom=False,
                        **field)
                    print("1", end='')
                    added_fields.append(f"{field['key_name']}__{field['related_item']}")
                else:
                    obj = Field.objects.filter(key_name=field['key_name'], related_item=field['related_item']).update(**field)
            self.stdout.write(self.style.SUCCESS('\tDone'))
            if len(added_fields) > 0:
                for x in added_fields:
                    print(f"\tДобавлено поле: {x}.")
                