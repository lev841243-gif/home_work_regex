import re, csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    data = list(csv.reader(f))

# Обработка
for r in data[1:]:
    r[:3] = (' '.join(r[:3]).split() + ['']*3)[:3]
    if len(r)>5 and r[5]:
        d = re.sub(r'\D', '', r[5])
        e = re.search(r'доб\.?\s*(\d+)', r[5], re.I)
        e = f" доб.{e.group(1)}" if e else ""
        if d.startswith('8'): d = '7' + d[1:]
        if len(d)==11 and d.startswith('7'):
            r[5] = f"+7({d[1:4]}){d[4:7]}-{d[7:9]}-{d[9:]}{e}"

# Уникальные
u = {}
for r in data[1:]:
    k = (r[0].lower(), r[1].lower())
    if k not in u: u[k] = r
    else:
        for i in range(len(r)):
            if r[i] and not u[k][i]: u[k][i] = r[i]

# Сохранение
res = [data[0]] + sorted(u.values())
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    csv.writer(f).writerows(res)

# Вывод
print(f"Обработано: {len(res)-1} записей")
print("Первые 3 записи:")
for r in res[1:4]:
    print(f"  {r[0]} {r[1]} - {r[5]}")