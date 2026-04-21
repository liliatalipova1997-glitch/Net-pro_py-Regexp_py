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

# ОБЪЕДИНЕНИЕ
unique = {}

for contact in contacts_list[1:]:

  key = (contact[0], contact[1])

  if key not in unique:
    unique[key] = contact.copy()
  else:
    for i in range(len(contact)):
      if contact[i] and not unique[key][i]:
        unique[key][i] = contact[i]


# ТЕЛЕФОН
phone_pattern = re.compile(
  r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})-?(\d{2})-?(\d{2})'
  r'(?:\s*\(?(доб.)\s*(\d+)\)?)?'
)

def format_phone(phone):
  return phone_pattern.sub(
    lambda m: f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}" +
              (f" {m.group(6)}{m.group(7)}" if m.group(6) else ""),
    phone
  ).strip()


for contact in unique.values():
  if contact[5]:
    contact[5] = format_phone(contact[5])

# РЕЗУЛЬТАТ
result = [contacts_list[0]] + list(unique.values())
# убираем пустые строки
result = [row for row in result if any(row)]
pprint(result)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
  datawriter = csv.writer(f)
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(result)