from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from django.shortcuts import _get_queryset
import hashlib
# import pdfkit
import hmac


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def convert_to_pdf_and_download(template_src, clinic_data, context_dict={}):
    try:
        html_string = render_to_string(template_src, context_dict)

        options = {'encoding': "UTF-8", 'quiet': '', 'page-size': 'A4'}

        # for windows
        path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        bytes_array = pdfkit.PDFKit(html_string, 'string', options=options, configuration=config).to_pdf()

        # for linux
        # path_wkhtmltopdf = r'/usr/bin/wkhtmltopdf'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        # bytes_array = pdfkit.PDFKit(html_string, 'string', options=options).to_pdf()


        response = HttpResponse(bytes_array, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        return response
    except Exception:
        pass


def allowed_groups(allowed_roles=[]):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            group = None
            user = request.user
            if user.is_superuser:
                return view(request, *args, **kwargs)
            
            if user:
                groups = user.groups.all()

                for group in groups:
                    if group.name in allowed_roles or request.user.is_superuser or allowed_roles == []:
                        return view(request, *args, **kwargs)
                raise Http404()
            else:
                raise Http404()
        return wrapper
    return decorator


def calculate_hmac(request):
    hmac_verification_keys = ['amount_cents', 'created_at', 'currency', 'error_occured', 'has_parent_transaction', 'id', 'integration_id', 'is_3d_secure', 'is_auth',  'is_capture', 'is_refunded', 'is_standalone_payment', 'is_voided', 'order', 'owner', 'pending', 'source_data.pan', 'source_data.sub_type', 'source_data.type', 'success']
    data_concatenated_string = ''
    for key in hmac_verification_keys:
        if request.query_params.get(key):
            data_concatenated_string += request.query_params.get(key)
    SECRET = bytearray('7B505C2BE2A6FB32EF81C38E7F4AAAB5'.upper(), "ASCII")
    STRING = bytearray(data_concatenated_string, "ASCII")
    generated_hmac = hmac.HMAC(key=SECRET, msg=STRING, digestmod=hashlib.sha512).hexdigest()
    is_secure = hmac.compare_digest(generated_hmac, request.query_params.get('hmac'))
    return is_secure

