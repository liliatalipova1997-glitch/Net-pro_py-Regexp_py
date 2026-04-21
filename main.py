from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


header = contacts_list[0]
data = contacts_list[1:]


# ФИО
# def normalize_fio(contact):
#   fio = ' '.join(contact[:3]).split()
#   fio = fio + [''] * (3 - len(fio))
#   contact[0], contact[1], contact[2] = fio[:3]
#   return contact
def normalize_fio(contact):
  fio = ' '.join(contact[:3]).split()
  fio = fio + [''] * (3 - len(fio))
  return fio[:3] + contact[3:]

data = [normalize_fio(contact) for contact in data]


# ОБЪЕДИНЕНИЕ
def merge_contacts(data):
  unique = {}

  for contact in data:
    key = (
      contact[0].strip().lower(),
      contact[1].strip().lower()
    )

    if key not in unique:
      unique[key] = contact.copy()
    else:
      for i in range(len(contact)):
        new_value = contact[i].strip() if isinstance(contact[i], str) else contact[i]
        old_value = unique[key][i]

        # если старого нет — берём новое
        if not old_value and new_value:
          unique[key][i] = new_value

        # если оба есть, но разные — НЕ теряем данные
        elif old_value and new_value and old_value != new_value:
          # склеиваем через ";"
          parts = set(old_value.split(";") + new_value.split(";"))
          unique[key][i] = ";".join(sorted(parts))

  return list(unique.values())

# ТЕЛЕФОН
# phone_pattern = re.compile(
#   r'(\+7|8)?\s*\(?(\d{3})\)?\s*[- ]?(\d{3})\s*[- ]?(\d{2})\s*[- ]?(\d{2})'
#   r'(?:\s*\(?(?:доб\.?|ext\.?)\s*(\d+)\)?)?'
# )
phone_pattern = re.compile(
  r'(\+7|8)?\s*\(?(\d{3})\)?\s*[- ]?(\d{3})'
  r'[- ]?(\d{2})[- ]?(\d{2})'
  r'(?:\s*\(?\s*(?:доб\.?|ext\.?)\s*(\d+)\s*\)?)?'
)

def repl(m):
  base = f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
  ext = f" доб.{m.group(6)}" if m.group(6) else ""
  return base + ext


def normalize_phones(data):

  for contact in data:
    for i, field in enumerate(contact):
      if isinstance(field, str):
        contact[i] = phone_pattern.sub(repl, field)
  return data

# РЕЗУЛЬТАТ

result = normalize_phones(merge_contacts(data))


# убираем пустые строки
result = [row for row in result if any(row)]


result = [header] + result
pprint(result)
# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
  datawriter = csv.writer(f)
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(result)