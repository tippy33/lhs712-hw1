import re

def normalize_date(type, date):
  if type == "year" and len(str(date)) == 2:
    return '19'+str(date)
  elif type != "year" and len(str(date)) == 1:  #month or day
      return '0'+str(date)
  else:
    return date

def write(line_number, date):
  # print(type(date))
  f = open('LHS712-Assg1-hngchris.txt', 'a')
  f.write(line_number+'\t'+date+'\n')
  f.close()

def push_date(date):
  return

def eng_to_number(month):
  pattern = [r'^Jan[a-z]*', r'^Feb[a-z]*', r'^Mar[a-z]*', r'^Apr[a-z]*', 
            r'^May[a-z]*', r'^Jun[a-z]*', r'^Jul[a-z]*', r'^Aug[a-z]*', 
            r'^Sep[a-z]*', r'^Oct[a-z]*', r'^Nov[a-z]*', r'^Dec[a-z]*', ]
  idx = 1
  for p in pattern:
    if re.search(p, month) is not None:
      if idx<10:
        return '0'+str(idx)
      else:
        return str(idx)
    else:
      idx+=1
  return month
  
  # if month == 'Jan' or month=='January':
  #   return '01'
  # elif month == 'Feb' or month=='February':
  #   return '02'
  # elif month == 'Mar' or month=='March':
  #   return '03'
  # elif month == 'Apr' or month=='April':
  #   return '04'
  # elif month == 'May':
  #   return '05'
  # elif month == 'June':
  #   return '06'
  # elif month == 'Jul' or month=='July':
  #   return '07'
  # elif month == 'Aug' or month=='August':
  #   return '08'
  # elif month == 'Sep' or month=='September':
  #   return '09'
  # elif month == 'Oct' or month=='October':
  #   return '10'
  # elif month == 'Nov' or month=='November':
  #   return '11'
  # elif month == 'Dec' or month=='December' or month=='Decemeber':
  #   return '12'
  # else:
  #   return month

def is_month(first, second):
  pattern = [r'^Jan[a-z]*', r'^Feb[a-z]*', r'^Mar[a-z]*', r'^Apr[a-z]*', 
            r'^May[a-z]*', r'^Jun[a-z]*', r'^Jul[a-z]*', r'^Aug[a-z]*', 
            r'^Sep[a-z]*', r'^Oct[a-z]*', r'^Nov[a-z]*', r'^Dec[a-z]*', ]
  first_is_num = True
  second_is_num =True
  for p in pattern:
    if re.search(p, first) is not None:
      first_is_num = False
    if re.search(p, second) is not None:
      second_is_num = False
  if first_is_num is True and second_is_num is True:
    return True  # mm/dd
  elif first_is_num is False and second_is_num is True:
    return True  # April 15
  elif first_is_num is True and second_is_num is False:
    return False  # 06 Oct (#320)
  return False  # no case like this

def parse_date():
  file = open('dates.txt', 'r')
  # file = open('practice.txt', 'r')
  lines = file.readlines()
  for l in lines:
    line_number = re.search(r'^[0-9]+', l)  # find line number
    print(line_number[0])
    if line_number is None:
      continue   # no need to loop if line number is missing
    date = None
    date_pattern = [r'([0-9]{1,2})\/([0-9]{1,2})\/([0-9]{2,4})', # 3, xx/xx/xx(xx)
                    r'([0-9]{1,2})-([0-9]{1,2})-([0-9]{2,4})', # 3, 08-30-1965
                    r'[^\d+](\d{1,2})\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?,?\s?(\d{2,4})',
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*.?\s?(\d{2}),?\s(\d{2,4})',
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?,?\s?(\d{2,4})',
                    # r'(\d{1,2}\s?)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?(\d{1,2})?,?\s?(\d{2,4})',
                    # r'(\w+)\s([0-9]{1,2}),{0,1}\s([0-9]{2,4})', # 3, May 16(,) 1997
                    # r'([0-9]{1,2})\s(\w+)\s([0-9]{2,4})', # 3, 30 May 1993
                    r'([0-9]{1,2})\/([0-9]{2,4})', # 2, xx/xx(xx)
                    # r'(\w+)\s([0-9]{2,4})', # 2, April 1354
                    r'([0-9]{4})'] # 1, xxxx
    for p in date_pattern:
      print(p)
      date_group_ = re.search(p, l)
      # print(date_group.group())
      if date_group_ is not None:
        # print(len(date_group.groups()))
        # idx = 0
        date_group = []
        # print(date_group_)
        # print(date_group_.groups())
        first_is_month = None
        if len(date_group_.groups()) == 3:
          # print(str(date_group_[1]))
          # print(type(date_group_[2]))
          first_is_month = is_month(str(date_group_[1]), str(date_group_[2]))  # if date_group[0] True
          # print(first_is_month)
        for d in date_group_.groups():   # change English month to number
          date_group.append(eng_to_number(d))
          # idx+=1
        # print(date_group)
        if len(date_group) == 3:  #xx/xx/xx or May 16, 1997
          if first_is_month is True:
            month = normalize_date('month', date_group[0])
            day = normalize_date('day', date_group[1])
            year = normalize_date('year', date_group[2])
          else:  # 03 April, 1992
            month = normalize_date('month', date_group[1])
            day = normalize_date('day', date_group[0])
            year = normalize_date('year', date_group[2])
        elif len(date_group) == 2:  # May 2020
          day = '01'
          month = normalize_date('month', date_group[0])
          year = normalize_date('year', date_group[1])
        elif len(date_group) == 1:
          day = '01'
          month = '01'
          year = normalize_date('year', date_group[0])
        date = str(year)+'-'+str(month)+'-'+str(day)
        print(date)
        write(line_number=str(line_number[0]), date=date)
        # print(date)
        break
  return

if __name__ == '__main__':
  open('LHS712-Assg1-hngchris.txt', 'w').close()
  parse_date()