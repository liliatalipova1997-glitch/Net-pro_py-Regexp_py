from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
  # pprint(contacts_list)

# ФИО
for contact in contacts_list[1:]:
  fio = ' '.join(contact[:3]).split()
  f = ['', '', '']
  fio.extend(f[len(fio):])
  contact[0], contact[1], contact[2] = fio

# ТЕЛЕФОН
phone_pattern = re.compile(
  r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})-?(\d{2})-?(\d{2})'
  r'(?:\s*\(?(доб.)\s*(\d+)\)?)?'
)

def format_phone(phone):
  return phone_pattern.sub(
    r'+7(\2)\3-\4-\5 \6\7',
    phone
  ).strip()

for contact in contacts_list[1:]:
  if contact[5]:
    contact[5] = format_phone(contact[5])



unique = {}
for contact in contacts_list[1:]:
  key = tuple(contact[:2])

  if key not in unique:
    unique[key] = contact
  else:
    old = unique[key]
    for i in range(len(contact)):
      if contact[i] and not old[i]:
        old[i] = contact[i]


result = [contacts_list[0]] + list(unique.values())
pprint(result)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8",newline="") as f:
  datawriter = csv.writer(f)
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(result)