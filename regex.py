import re

def parse_date():
  file = open('dates.txt', 'r')
  lines = file.readlines()
  for l in lines:
    line_number = re.search(r'^[0-9]+', l)  # find line number
    if line_number is None:
      continue   # no need to loop if line number is missing
    date = None
    date_pattern = [r'([0-9]{1,2})\/([0-9]{1,2})\/([0-9]{1,2})']
    for p in date_pattern:
      date_group = re.search(p, l)
      print(date_group)
      if date_group is not None:
        # print(date_group[0])
        # print(date_group[1])
        # print(date_group[2])
        ######
        month = date_group[1]
        if len(str(month)) == 1:
          month = '0'+str(month)
        day = date_group[2]
        if len(str(day)) == 1:
          day = '0'+str(day)
        year = date_group[3]
        if len(str(year)) == 2:
          year = '19'+str(year)
        date = year+'-'+month+'-'+day
        print(date)
        break
  return

if __name__ == '__main__':
  parse_date()