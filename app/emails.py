from core.settings import ATTACHMENT_DIR
import os
import imaplib, email as email_package
from datetime import datetime
from core.settings import IMP_URL, EMAIL_HOST_USER as user, EMAIL_HOST_PASSWORD as password


# <editor-fold desc="DataExtraction Class">
# class DataExtraction():
#     weekdays_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#     months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     years_list = []
#
#     for i in range(1990, 2050):
#         years_list.append(str(i))
#
#     def __init__(self):
#         pass
#
#     def get_smtp_id(self, rec_str):
#         smtp_id = ""
#         id_index = -1
#         try:
#             id_index = rec_str.index('id')
#         except Exception as e:
#             return -1
#
#         for i in rec_str[id_index + 3:]:
#             if i == ';':
#                 break
#             smtp_id += i
#         if len(smtp_id) == 0:
#             return None
#         return smtp_id
#
#     def get_id_index(self, rec_str, rec_list):
#         id_index = -1
#         for i in rec_list:
#             try:
#                 id_index = rec_str.index(i)
#                 return rec_list.index(i)
#             except Exception as e:
#                 pass
#         if id_index == -1:
#             return -1
#
#     def add_o(self, rec_str):
#         try:
#             if int(rec_str) < 10:
#                 string = '0' + str(rec_str)
#                 return string
#         except Exception as e:
#             print('Exception', e)
#         return rec_str
#
#     def remove_o(self, rec_str):
#         i = ""
#         try:
#             if int(rec_str) > 10:
#                 return rec_str
#             i = rec_str[0]
#             print('i', i)
#         except Exception as e:
#             print("Exception", e)
#         try:
#             if int(i) == 0:
#                 return rec_str[1:]
#         except Exception as e:
#             print(e)
#             return rec_str[1:]
#         return rec_str
#
#     def get_datetime(self, rec_str):
#         id_index = -1
#         for i in self.weekdays_list:
#             try:
#                 id_index = rec_str.index(i)
#             except:
#                 pass
#         if id_index == -1:
#             return -1
#         datetime_string = rec_str[id_index + 4:id_index + 26]
#         day = self.remove_o(self.add_o(datetime_string[0:3]))
#         month = self.remove_o(self.add_o(str(self.get_id_index(datetime_string, self.months_list))))
#         year = str(self.years_list[self.get_id_index(datetime_string, self.years_list)])
#         timeline = datetime_string[-9:-1]
#         hour = self.remove_o(self.add_o(timeline[0:2]))
#         minitue = self.remove_o(self.add_o(timeline[3:5]))
#         second = self.remove_o(self.add_o(timeline[-2:]))
#         new_time_format = f"{str(day)}/{str(month)}/{str(year)} {str(hour)}:{str(minitue)}:{str(second)}".strip()
#         time_zone = None
#         try:
#             time_zone = datetime.strptime(
#                 new_time_format,
#                 "%d/%m/%Y %H:%M:%S"
#             )
#         except Exception as e:
#             print(e)
#
#         return time_zone
#
#     def get_email_address(self, rec_str):
#         if rec_str[-1] == '>':
#             index = 0
#             for i in range(len(rec_str)):
#                 if rec_str[i] == '<':
#                     index = i
#
#             return rec_str[index + 1:-1]
#         else:
#             return rec_str
class DataExtraction():
    weekdays_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years_list = []

    for i in range(1990, 2050):
        years_list.append(str(i))

    def __init__(self):
        pass

    def get_smtp_id(self, rec_str):
        smtp_id = ""
        id_index = -1
        try:
            id_index = rec_str.index('id')
        except Exception as e:
            return -1

        for i in rec_str[id_index + 3:]:
            if i == ' ':
                break
            smtp_id += i
        if len(smtp_id) == 0:
            return None
        return smtp_id

    def get_id_index(self, rec_str, rec_list):
        id_index = -1
        for i in rec_list:
            try:
                id_index = rec_str.index(i)
                return rec_list.index(i)
            except Exception as e:
                pass
        if id_index == -1:
            return -1

    def add_o(self, rec_str):
        if int(rec_str) < 10:
            string = '0' + str(rec_str)
            return string
        return rec_str

    def remove_o(self, rec_str):
        if int(rec_str) > 10:
            return rec_str
        i = rec_str[0]
        if int(i) == 0:
            return rec_str[1:]
        return rec_str

    def get_date(self, rec_str):
        x = ''
        for i in rec_str.strip():
            x = x + i
            if i == ' ':
                break
        if int(x) < 10:
            return '0' + x
        return x

    def get_month(self, rec_str, rec_list):
        for i in rec_list:
            try:
                id = rec_list.index(i) + 1
                if int(id) < 10:
                    return '0' + str(id)
                return id
            except:
                pass
        return 0

    def get_datetime(self, rec_str):
        datetime_string = ''
        id_index = -1
        for i in self.weekdays_list:
            try:
                id_index = rec_str.index(i)
            except:
                pass
        if id_index == -1:
            return -1
        datetime_string = rec_str[id_index + 4:id_index + 26]
        day = self.get_date(datetime_string)
        month = self.get_month(datetime_string, self.months_list)
        year = str(self.years_list[self.get_id_index(datetime_string, self.years_list)])
        timeline = datetime_string[-10:-1]
        timeline_hour = timeline.strip()
        hour = self.remove_o(self.add_o(timeline_hour[0:2]))
        minitue = self.remove_o(self.add_o(timeline_hour[3:5]))
        second = self.remove_o(self.add_o(timeline_hour[-2:]))
        new_time_format = f"{str(day).strip()}/{str(month).strip()}/{str(year.strip())} {str(hour.strip())}:{str(minitue.strip())}:{str(second.strip())}".strip()
        time_zone = None
        try:
            time_zone = datetime.strptime(
                new_time_format,
                "%d/%m/%Y %H:%M:%S"
            )
        except Exception as e:
            print(e)
        return time_zone

    def get_email_address(self, rec_str):
        if rec_str[-1] == '>':
            index = 0
            for i in range(len(rec_str)):
                if rec_str[i] == '<':
                    index = i

            return rec_str[index + 1:-1]
        else:
            return rec_str

# </editor-fold>


# <editor-fold desc="saves attachments in a folder if it presents">
def get_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(ATTACHMENT_DIR, fileName)
            with open(filePath, 'wb') as f:
                f.write(part.get_payload(decode=True))


# </editor-fold>


# <editor-fold desc="Returns body from encoded format">
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


# </editor-fold>


# <editor-fold desc="Returns the email label i.e from list of x mails which search mail id label">
def search(key, value, con):
    print("search fun : ", key, value, con)
    result, data = con.search(None, key, '"{}"'.format(value))
    return data


# </editor-fold>


# <editor-fold desc="Returns email id's">
def get_emails(result_bytes, con):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs


# </editor-fold>


# <editor-fold desc="returns email body by taking parameter as email id in list">
def get_email_with_ids(id, con):
    typ, data = con.fetch(id, '(RFC822)')
    return data


# </editor-fold>


def get_email_format(msgs):
    list_dict = {}
    id = 0
    for msg in msgs[::-1]:
        for response_part in msg:
            if type(response_part) is tuple:
                my_msgs = email_package.message_from_bytes((response_part[1]))
                for part in my_msgs.walk():
                    list_dict[id] = {'subject': my_msgs['subject'],
                                     'from': my_msgs['from'],
                                     'to': my_msgs['to'],
                                     'cc': my_msgs['cc'],
                                     'Received': my_msgs['Received'],
                                     'body': part.get_payload(),

                                     }
                #     list_dict[id] = { 'body' : part.get_payload()}
            # print('list_dict', list_dict)
        id += 1
        print('id', id)

    return list_dict

# def add_o(self, rec_str):
#        if int(rec_str) < 10:
#            return '0' + str(rec_str)
#        return rec_str
#
#    def get_datetime(self, rec_str):
#        id_index = -1
#        for i in self.weekdays_list:
#            try:
#                id_index = rec_str.index(i)
#            except:
#                pass
#        if id_index == -1:
#            return -1
#        datetime_string = rec_str[id_index + 4:id_index + 26]
#        day = self.add_o(datetime_string[0:3])
#        month = self.add_o(str(self.get_id_index(datetime_string, self.months_list)))
#        year = str(self.years_list[self.get_id_index(datetime_string, self.years_list)])
#        timeline = datetime_string[-9:-1]
#        hour = self.add_o(timeline[0:2])
#        minitue = self.add_o(timeline[3:5])
#        second = self.add_o(timeline[-2:])
#        new_time_format = f"{str(day)}/{str(month)}/{str(year)} {str(hour)}:{str(minitue)}:{str(second)}".strip()
#        time_zone = None
#        try:
#            time_zone = datetime.strptime(
#                new_time_format,
#                "%d/%m/%Y %H:%M:%S"
#            )
#        except Exception as e:
#            print('Exception', e)
#        return time_zone
