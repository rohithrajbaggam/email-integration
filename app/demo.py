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
