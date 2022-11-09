from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .emails import get_emails, get_body, search, get_email_with_ids, get_email_format, DataExtraction
from core.settings import CONFIGURATION
from core.settings import EMAIL_HOST_USER as user, EMAIL_HOST_PASSWORD as password, IMP_URL
import imaplib, email as email_package
from .serializers import appFromEmailSearchSerializer
from rest_framework.generics import GenericAPIView
from .tasks import MyTask, MyTaskCeleryBeat
from .models import appEmailDataModel, appEmailUserCredentialsModel, appGmailDirModel
from .serializers import appEmailDataModelListSerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


#
# class appEmailSMTPListView(APIView):
#     def get(self, request):
#
#         return


# <editor-fold desc="all mails from db">
class appEmailDataModelListView(ListAPIView):
    queryset = appEmailDataModel.objects.all().order_by('-created_at')
    serializer_class = appEmailDataModelListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['from_user', 'to_user', 'dir']

    def list(self, request, *args, **kwargs):
        for query in self.queryset.all():
            if query.received_at == None:
                print(f"id {query.id} -> ", query.received_at, " count ",
                      self.queryset.filter(received_at=None).count())
            # if len(query.smtp_id) > 20:
            #     print("smtp-id", query.smtp_id)
        serializer = self.get_serializer(self.paginate_queryset(self.filter_queryset(self.get_queryset())), many=True,
                                         context={"request": request})
        return self.get_paginated_response(serializer.data)


# </editor-fold>


# class appEmailCreateEndPoint(APIView):
#     def get

class DemoClassView(APIView):
    def get(self, request):
        MyTask.delay()
        return Response("ok")


# <editor-fold desc="list of all inbox emails from gmail through smtp">
class appEmailinFormatView(APIView, DataExtraction):

    def add_emaildata(self, result_data):

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

    def get(self, request):
        data = CONFIGURATION.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        msgs = []
        final_dict_email_id = []
        for id in id_list[-20:-1]:
            print('id --> ', id)
            data = get_email_with_ids(id, CONFIGURATION)
            msgs.append(data)
            final_dict_email_id.append(id)
        result_data = get_email_format(msgs)
        # print('result_data', result_data)
        self.add_emaildata(result_data)

        return Response(result_data)


# </editor-fold>


class appEmailMyinbox(APIView):
    def get(self, request):
        final_dict_email_id = []
        for query in appEmailUserCredentialsModel.objects.all():
            print("query.email, query.smtp_password", query.email, query.smtp_password)
            CONFIGURATION = imaplib.IMAP4_SSL(IMP_URL)
            CONFIGURATION.login(query.email, query.smtp_password)
            CONFIGURATION.select("INBOX")
            data = CONFIGURATION.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()
            msgs = []

            for id in id_list[-11:-1]:
                data = get_email_with_ids(id, CONFIGURATION)
                msgs.append(data)
                final_dict_email_id.append(id)
            msgs.reverse()
            final_dict_email_id.reverse()
            print(len(msgs))
            email_message_body = []
            for msg in msgs:
                email_message_body.append(get_body(email_package.message_from_bytes(msg[0][1])))

            final_dict = {}
            for i in range(len(email_message_body)):
                final_dict[i] = {'id': final_dict_email_id[i], 'User': user, 'body': email_message_body[i]}
        return Response(final_dict)


class appFromEmailSearchView(GenericAPIView):
    queryset = None
    serializer_class = appFromEmailSearchSerializer

    def post(self, request):
        email = request.data['email']
        print("email", email)
        try:
            msgs = get_emails(search('FROM', email, CONFIGURATION), CONFIGURATION)
            email_message_body = []
            for msg in msgs:
                email_message_body.append(get_body(email_package.message_from_bytes(msg[0][1])))
            final_dict = {}
            for i in range(len(email_message_body)):
                final_dict[i] = {'From': email, 'To': user, 'body': email_message_body[i]}
            return Response(final_dict)
        except Exception as e:
            print("Exception", e)
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


# <editor-fold desc="demo class">
class appEmailsForSpecificEmailsView(APIView):
    def get(self, request):
        email = "rohithbaggamintern@techarion.com"
        msgs = get_emails(search('FROM', email, CONFIGURATION), CONFIGURATION)
        email_message_body = []
        for msg in msgs:
            email_message_body.append(get_body(email_package.message_from_bytes(msg[0][1])))
        final_dict = {}
        for i in range(len(email_message_body)):
            final_dict[i] = {'From': email, 'To': user, 'body': email_message_body[i]}
        return Response(final_dict)
# </editor-fold>
