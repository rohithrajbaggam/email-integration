from time import sleep
from celery import shared_task, Task
from .emails import *
from core.celery import celery
from .models import appEmailDataModel, appEmailUserCredentialsModel
from core.settings import GMAIL_DIR_LIST


# <editor-fold desc="Celery Task to save mails to database">
class MyTask(Task, DataExtraction):
    def run(self, *args, **kwargs):
        print("Requesting mails.....")
        final_dict_email_id = []
        for query in appEmailUserCredentialsModel.objects.all():
            for g_dir in GMAIL_DIR_LIST:
                CONFIGURATION = imaplib.IMAP4_SSL(IMP_URL)
                CONFIGURATION.login(query.email, query.smtp_password)
                CONFIGURATION.select(g_dir)
                CONFIGURATION.search(None, 'ALL')
                data = CONFIGURATION.search(None, 'ALL')
                mail_ids = data[1]
                id_list = mail_ids[0].split()

                msgs = []

                for id in id_list[0:-1]:
                    data = get_email_with_ids(id, CONFIGURATION)
                    msgs.append(data)
                    final_dict_email_id.append(id)
                result_data = get_email_format(msgs)

                for i in range(len(result_data)):
                    data = result_data[i]
                    smtp_id = self.get_smtp_id(data['Received'])
                    from_user = self.get_email_address(data['from'])
                    to_user = self.get_email_address(data['to'])
                    subject = data["subject"]
                    content = data["body"]
                    received_at = self.get_datetime(data['Received'])

                    if appEmailDataModel.objects.filter(smtp_id=smtp_id).exists():
                        pass
                    else:
                        appEmailDataModel.objects.create(
                            smtp_id=smtp_id,
                            from_user=from_user,
                            to_user=to_user,
                            subject=subject,
                            content=content,
                            dir=g_dir,
                            received_at=received_at,
                        )

        print('task completed.....')


MyTask = celery.register_task(MyTask())


# </editor-fold>


# <editor-fold desc="Celery Beat Task to save mails to database">
class MyTaskCeleryBeat(Task, DataExtraction):
    def run(self, *args, **kwargs):
        print("Requesting mails.....")
        final_dict_email_id = []
        for query in appEmailUserCredentialsModel.objects.all():
            data = CONFIGURATION.search(None, 'ALL')
            CONFIGURATION = imaplib.IMAP4_SSL(IMP_URL)
            CONFIGURATION.login(query.email, query.smtp_password)

            CONFIGURATION.select("INBOX")
            mail_ids = data[1]
            id_list = mail_ids[0].split()
            msgs = []
            for id in id_list[0:-1]:
                data = get_email_with_ids(id, CONFIGURATION)
                msgs.append(data)
                final_dict_email_id.append(id)
            result_data = get_email_format(msgs)

            for i in range(len(result_data)):
                data = result_data[i]
                smtp_id = self.get_smtp_id(data['Received'])
                from_user = self.get_email_address(data['from'])
                to_user = self.get_email_address(data['to'])
                subject = data["subject"]
                content = data["body"]
                received_at = self.get_datetime(data['Received'])

                if appEmailDataModel.objects.filter(smtp_id=smtp_id).exists():
                    pass
                else:
                    appEmailDataModel.objects.create(
                        smtp_id=smtp_id,
                        from_user=from_user,
                        to_user=to_user,
                        subject=subject,
                        content=content,
                        received_at=received_at,
                    )

        print('task completed.....')


MyTaskCeleryBeat = celery.register_task(MyTaskCeleryBeat())
# </editor-fold>


#
# @shared_task
# def saving_emails(message):
#     print("Requesting mails.....")
#     data = CONFIGURATION.search(None, 'ALL')
#     mail_ids = data[1]
#     id_list = mail_ids[0].split()
#     msgs = []
#     final_dict_email_id = []
#     for id in id_list[-10:-1]:
#         data = get_email_with_ids(id, CONFIGURATION)
#         msgs.append(data)
#         final_dict_email_id.append(id)
#     result_data = get_email_format(msgs)
#
#     for i in range(len(result_data)):
#         print()
#         print()
#         print()
#         print()
#         data = result_data[i]
#         print(f'subject -> {data["subject"]}')
#         print(f'from -> {data["from"]}')
#         print(f'to -> {data["to"]}')
#         print(f'received -> {data["Received"]}')
#         print(f'body -> {data["body"]}')
#
#     print('task completed.....')


# class MyTask(Task, DataExtraction):
#     def run(self, *args, **kwargs):
#         print("Requesting mails.....")
#         data = CONFIGURATION.search(None, 'ALL')
#         mail_ids = data[1]
#         id_list = mail_ids[0].split()
#
#         msgs = []
#         final_dict_email_id = []
#         for id in id_list[0:-1]:
#             data = get_email_with_ids(id, CONFIGURATION)
#             msgs.append(data)
#             final_dict_email_id.append(id)
#         result_data = get_email_format(msgs)
#
#         for i in range(len(result_data)):
#             data = result_data[i]
#             smtp_id = self.get_smtp_id(data['Received'])
#             from_user = self.get_email_address(data['from'])
#             to_user = self.get_email_address(data['to'])
#             subject = data["subject"]
#             content = data["body"]
#             received_at = self.get_datetime(data['Received'])
#
#             if appEmailDataModel.objects.filter(smtp_id=smtp_id).exists():
#                 pass
#             else:
#                 appEmailDataModel.objects.create(
#                     smtp_id=smtp_id,
#                     from_user=from_user,
#                     to_user=to_user,
#                     subject=subject,
#                     content=content,
#                     received_at=received_at,
#                 )
#
#         print('task completed.....')
#
#
# MyTask = celery.register_task(MyTask())
