import re

def normalize_date(type, date):
  if type == "year" and len(str(date)) == 2:
    return '19'+str(date)
  elif type != "year" and len(str(date)) == 1:
      return '0'+str(date)
  else:
    return date

def write(line_number, date):
  # print(type(date))
  f = open('LHS712-Assg1-hngchris.txt', 'a')
  f.write(line_number+'\t'+date+'\n')
  f.close()

def parse_date():
  file = open('dates.txt', 'r')
  lines = file.readlines()
  for l in lines:
    line_number = re.search(r'^[0-9]+', l)  # find line number
    print(line_number[0])
    if line_number is None:
      continue   # no need to loop if line number is missing
    date = None
    date_pattern = [r'([0-9]{1,2})\/([0-9]{1,2})\/([0-9]{2,4})', 
                    r'([0-9]{1,2})\/([0-9]{2,4})',
                    r'([0-9]{4})']
    for p in date_pattern:
      date_group = re.search(p, l)
      # print(date_group.group())
      if date_group is not None:
        # print(len(date_group.groups()))
        if len(date_group.groups()) == 3:
          month = normalize_date('month', date_group[1])
          day = normalize_date('day', date_group[2])
          year = normalize_date('year', date_group[3])
        elif len(date_group.groups()) == 2:
          day = '01'
          month = normalize_date('month', date_group[1])
          year = normalize_date('year', date_group[2])
        elif len(date_group.groups()) == 1:
          day = '01'
          month = '01'
          year = normalize_date('year', date_group[1])
        date = str(year)+'-'+str(month)+'-'+str(day)
        write(line_number=str(line_number[0]), date=date)
        # print(date)
        break
  return

if __name__ == '__main__':
  parse_date()