from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import render_to_response, render
from django.utils.html import escape
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from loadprograms import dbcontext
import requests
import pprint
#module to break the google return strin
import base64
import simplejson as json

import auth
import sys
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import xlsxwriter
from xlsxwriter.workbook import Workbook

def loginpage(request):
    print 'IP address for debug-toolbar: ', request.META['REMOTE_ADDR']
    print 'sys.path = ', sys.path
    return render_to_response('mainpage.html')

def startpage(request):
    return render_to_response('startpage.html')

@csrf_exempt
def googleauthlogin(request):
    GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID 
    GOOGLE_REDIRECT_URL = settings.GOOGLE_REDIRECT_URL 
    print 'GOOGLE_CLIENT_ID =', GOOGLE_CLIENT_ID
    print 'GOOGLE_REDIRECT_URL =', GOOGLE_REDIRECT_URL
    #The get request contains the following - client_id , response_type, scope, redirect_uri(from the console)
    return HttpResponseRedirect('https://accounts.google.com/o/oauth2/auth?client_id='+ GOOGLE_CLIENT_ID + '&response_type=code&scope=openid%20email&redirect_uri='+GOOGLE_REDIRECT_URL)
    #return HttpResponseRedirect('https://accounts.google.com/o/oauth2/auth?client_id=690178314820-85fvo4eq56se4mppdaf0pt6tnnjo552c.apps.googleusercontent.com&response_type=code&scope=openid%20email&redirect_uri=http://onlineshop.prem1980.webfactional.com/mainpage')

def mainpage(request):
    code = request.GET['code']
    payload = {'code':code,'client_id':settings.GOOGLE_CLIENT_ID,'client_secret':settings.GOOGLE_SECRET,'redirect_uri':settings.GOOGLE_REDIRECT_URL,'grant_type':'authorization_code'}
    r = requests.post('https://accounts.google.com/o/oauth2/token',payload)
    print 'type =', type(r.json()['id_token'].encode('utf-8'))
    token = r.json()['id_token'].encode('utf-8')
    print 'token type =', type(token)
    segments = token.split('.')
    if (len(segments) != 3): 
       raise Exception('Wrong number of segments in token: %s' % segments) 
    b64string = segments[1]
    b64string = b64string.encode('ascii') 
    padded = b64string + '=' * (4 - len(b64string) % 4) 
    padded = base64.urlsafe_b64decode(padded)
    
    #Create a new session
    ses_id = auth.create_session_id()
    
    if 'sessionid' not in request.session:
        request.session['sessionid'] = ses_id
        request.session['acsrfid'] = auth.get_acsrf(ses_id)
    print 'old request session id =', request.session['sessionid']
    print 'old request acsrf id =', request.session['acsrfid']
    request.session['sessionid'] = ses_id
    request.session['acsrfid'] = auth.get_acsrf(ses_id)
    print 'new request session id =', request.session['sessionid']
    print 'new request acsrf id =', request.session['acsrfid']
    return render_to_response('startpage.html',context_instance=RequestContext(request))

def categorypage(request,categoryid):
    print 'request.get = ', request.GET.get('categoryid')
    if checksessionauthentication(request):
        return render_to_response('categorypage.html',{'categoryid':categoryid},context_instance=RequestContext(request))

def checksessionauthentication(request):
    try:
        ses_id = request.session['sessionid']
        acsrf = request.session['acsrfid']
        print 'checksessionauthentication ses_id = ', request.session['sessionid']
        print 'checksessionauthentication acsrf = ', request.session['acsrfid']
        print 'User authenticated'
        return True
    except KeyError:
        return False
@csrf_exempt
def createpdf(request):
    print 'Going to create pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response,pagesize=letter)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    json_response = allproducts(1)
    
    width, height = letter
    
    p.setLineWidth(.3)
    p.setFont('Helvetica',12)
    (incr, x, y, x1) = initpages(height)
    print 'Actual value of y = {0}'.format(y)
    print 'Actual value of x = {0}'.format(x)
    print 'Actual value of height = {0}'.format(height)
    for each in json_response:
        print 'value of height = {0} , value of x = {1} , value of y = {2}'.format(height,x,y)
        if y < 40:
            print 'page break called'
            p.showPage()
            (incr, x, y, x1) = initpages(height)
            #p.append(PageBreak())
        p.drawString(x, y, 'Name:')
        p.drawString(x1, y, each['name'])
        y = y - incr
        p.drawString(x, y, 'Price:')
        p.drawString(x1, y, '$'+str(each['price']))
        y = y - incr
        p.drawString(x, y, 'Old Price:')
        p.drawString(x1, y, '$'+str(each['old_price']))
        y = y - incr
        p.drawString(x, y, 'Author Name:')
        p.drawString(x1, y, each['author_name'])
        y = y - incr
    # Close the PDF object cleanly, and we're done.
        p.drawString(x, y, 120 * '-')
        y = y - incr

    p.save()
    print 'PDF response done'
    return response

def initpages(height):
    incr = 20
    x = 20
    x1 = 100
    y = height - 30
    return incr, x, y, x1

@csrf_exempt
def createexcel(request):
    import StringIO
    # create a workbook in memory
    output = StringIO.StringIO()

    book = Workbook(output)
    

    sheet = book.add_worksheet('test')
    boldformat = book.add_format({'bold':True})

    sheet.set_column(0,15,25)       
    
    sheet.write(0, 0, 'All Products', boldformat)
    
    sheet.write(3, 0, 'Name',boldformat)
    sheet.write(3, 1, 'Price',boldformat)
    sheet.write(3, 2, 'Old Price',boldformat)
    sheet.write(3, 3, 'Author Name',boldformat)
    
    row = 4
    print 'Call all products for excel'
    json_response = allproducts(1,serialize_now="N")
    print 'json_response = ', json_response
    for each in allproducts(1, serialize_now = "N"):
        #print 'xlsxwriter each = ', each
        sheet.write(row,0,each['name'])
        sheet.write(row,1,'$'+str(each['price']))
        sheet.write(row,2,'$'+str(each['old_price']))
        sheet.write(row,3,each['author_name'])
        row += 1
        
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    return response

def createdoc(request):
    return None

@csrf_exempt    
def getproductinfo(request):
    print 'get product info'
    print 'category id =', request.POST.get('categoryid')
    categoryid = request.POST.get('categoryid')
    if checksessionauthentication(request):
        json_response = allproducts(categoryid,serialize_now = "Y")
        return HttpResponse(json_response,content_type='application/json')
    

def allproducts(categoryid,serialize_now = ""):
    x = dbcontext.DBContext()    
    qry = """Select id,name,author_name,price,old_price,description,image_caption from Products where category_id = {0} """.format(int(categoryid))
    print 'qry = ', qry
    results = x.executequery(qry)
    output = []
    for each in results:
        output.append(each)
    #print 'output =', output
    x.close()
    #for each in output:
    #    print 'each = ', each
    print 'Serializing now = ', serialize_now
    
    if serialize_now == "Y": 
        try:
            json_response = json.dumps(output)
        except (TypeError, ValueError, NameError) as err:
            print 'Error:', err
        return json_response
    else:   
        return output
            
     
    
    
