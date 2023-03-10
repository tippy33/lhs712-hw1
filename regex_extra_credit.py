import re
import datetime

original_date_is_en = []  # True: english, False: number

def normalize_date(type, date):
  if type == "year" and len(str(date)) == 2:
    return '19'+str(date)
  elif type != "year" and len(str(date)) == 1:  #month or day
      return '0'+str(date)
  else:
    return date

def debug(line_number, orginal, date):
  f = open('debug.txt', 'a')
  f.write(line_number+'\t'+orginal+'\t'+date+'\n')
  f.close()

def write(line_number, date, end_date, push_date_en):
  # print(type(date))
  f = open('LHS712-Assg1-hngchris-extra-credit.txt', 'a')
  f.write(line_number+'\t'+date+'\t'+end_date+'\t'+push_date_en+'\n')
  f.close()

def push_date_en(push_date):
  # print(push_date)
  months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  date = re.search(r'(\d{2})-(\d{2})-(\d{4})', push_date)
  year = int(date[3])
  month = normalize_date('month', int(date[1]))
  day = normalize_date('day', int(date[2]))
  if original_date_is_en.pop() == True:  # English form
    return str(months[int(month)-1])+' '+str(day)+', '+str(year)
  else:  # Number form
    return str(month)+'/'+str(day)+'/'+str(year)

def push_date(date):
  # print(date)
  date = re.search(r'(\d{2})-(\d{2})-(\d{4})', date)
  # print(date[1], date[2], date[3])
  year = int(date[3])
  month = int(date[1])
  day = int(date[2])
  start_date = datetime.date(year=year, month=month, day=day)
  end_date = start_date + datetime.timedelta(days=40)
  # print(end_date)
  date = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', str(end_date))
  year = int(date[1])
  month = normalize_date('month', int(date[2]))
  day = normalize_date('day', int(date[3]))
  final_date = str(month)+'-'+str(day)+'-'+str(year)
  return final_date

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
    # print(line_number[0])
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
    idx = 0
    for p in date_pattern:
      date_group_ = re.search(p, l)
      if date_group_ is not None:
        # store original date form (english or number)
        if idx == 2 or idx==3 or idx==4:
          original_date_is_en.append(True)
        else: 
          original_date_is_en.append(False)
        # normalize date
        date_group = []
        first_is_month = None
        if len(date_group_.groups()) == 3:
          first_is_month = is_month(str(date_group_[1]), str(date_group_[2]))  # if date_group[0] True
        for d in date_group_.groups():   # change English month to number
          date_group.append(eng_to_number(d))
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
        date = str(month)+'-'+str(day)+'-'+str(year)
        pushed_date = push_date(date)
        write(line_number=str(line_number[0]), date=date, end_date=pushed_date, push_date_en=push_date_en(pushed_date))
        break
      idx += 1
  return

if __name__ == '__main__':
  open('LHS712-Assg1-hngchris-extra-credit.txt', 'w').close()
  parse_date()