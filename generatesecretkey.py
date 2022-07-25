from django.core.management import utils

new_secret_key = utils.get_random_secret_key()
f = open(".env", "x")
f.write(f"SECRET_KEY='{new_secret_key}'")
f.close()
