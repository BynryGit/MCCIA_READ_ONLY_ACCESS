
# System Modules
charset='utf-8'
import smtplib, traceback, json
from decimal import Decimal
from xhtml2pdf import pisa
import cStringIO as StringIO
from cgi import escape
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# User Models
from membershipapp.models import UserDetail


# Download Member Proforma Invoice
def download_proforma_invoice(request, m_id, m_year):
    try:
        print '\nRequest IN | member_proforma_invoice | download_proforma_invoice | User = ', request.user

        html = ''
        member_obj = UserDetail.objects.get(id=m_id)
        m_year = str(m_year).replace('_', '-')
        if member_obj.membership_slab:
            template = get_template('backoffice/membership/member_proforma_invoice.html')
            tax_amount = Decimal(member_obj.membership_slab.annual_fee) * Decimal(0.09)
            tax_amount = '%.2f' % tax_amount
            total_amount = Decimal(member_obj.membership_slab.annual_fee) + Decimal(Decimal(tax_amount) * 2)
            total_amount = '%.2f' % total_amount
            html = template.render(Context({'member_obj': member_obj, 'year': m_year, 'tax_amount': tax_amount,
                                            'total_amount': total_amount}))
            result = StringIO.StringIO()
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="PI_'+str(m_year)+'_'+str(member_obj.company.company_name).strip()+'.pdf"'
                return response
            return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
        else:
            return HttpResponse('No Slab Found. Please update slab in Member Profile.<pre>%s</pre>' % escape(html))
    except Exception,e:
        print '\nException IN | member_proforma_invoice | download_proforma_invoice | Excp = ', str(traceback.print_exc())
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def send_pi_through_email_to_user(request,m_id,m_year):
    try:
        print '\nRequest IN | member_proforma_invoice| send_pi_through_email_to_user '
        member_obj = UserDetail.objects.get(id=m_id)
        print "username = ", member_obj
        m_year = str(m_year).replace('_', '-')

        print "year = ",m_year
        if m_year:
            to_list = []
            gmail_user = "membership@mcciapune.com"
            gmail_pwd = "mem@2011ship"


            if member_obj.enroll_type == "CO":
                if member_obj.company.ceo_email_confirmation == True:
                    if member_obj.poc_email and member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.ceo_email))
                        to_list.append(str(member_obj.poc_email))
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
                    elif member_obj.poc_email:
                        to_list.append(str(member_obj.ceo_email))
                        to_list.append(str(member_obj.poc_email))
                    elif member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.ceo_email))
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
                    else:
                        to_list.append(str(member_obj.ceo_email))
                else:
                    if member_obj.poc_email and member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.poc_email))
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
                    elif member_obj.poc_email:
                        to_list.append(str(member_obj.poc_email))
                    elif member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
            else:
                to_list.append(str(member_obj.ceo_email))

            msg = MIMEMultipart('related')

            server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)

            TO = to_list
            CC = ['membership@mcciapune.com', 'vijendra.chandel@bynry.com']

            html = get_template('backoffice/membership/content_for_proforma_invoice.html').render(Context)
            htmlfile = MIMEText(html, 'html', _charset=charset)
            msg.attach(htmlfile)
            msg['subject'] = 'PI MCCIA membership renewal'
            msg['from'] = 'mailto: <membership@mcciapune.com>'
            msg['to'] = ",".join(TO)
            msg['cc'] = ",".join(CC)

            pdf_response = download_proforma_invoice(request,m_id,m_year)
            attachment = MIMEApplication(pdf_response.getvalue(),content_type='application/pdf')
            attachment['Content-Disposition'] = 'inline; filename="PI_' + str(m_year) + '_' + str(
                member_obj.company.company_name).strip() + '.pdf"'
            msg.attach(attachment)

            toaddrs = TO + CC
            server.sendmail(msg['from'], toaddrs, msg.as_string())
            server.quit()
            print '\nResponse OUT | member_proforma_invoice | send_pi_through_email_to_user | Mail is send to', TO
            return HttpResponse('<center><h2>Mail Sent.</h2></center>')
        else:
            return HttpResponse('<center><h2>Proforma Not Found.</h2></center>')
    except Exception, exc:
        print '\nException | member_proforma_invoice| send_pi_through_email_to_user | EXCP = ', str(traceback.print_exc())
        data = {'success': 'true', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')