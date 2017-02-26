from django.shortcuts import render
from django.shortcuts import redirect

from matplotlib import pylab
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import *

import StringIO
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader

import sqlite3
import random

from .forms import NameForm
from django.template.context_processors import csrf

from django.urls import reverse

batchsel = ''
sectionsel = ''

#returning to home page
def home(request):
    return render(request, 'home/home.html')

#validating faculty credentials
def faculty1(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        password1 = request.POST.get('password')
    
        #faculty login credentials
        import sqlite3

        #Database connection
        conn = sqlite3.connect('cse.db')
        c = conn.cursor()

        id=faculty_id
        password=password1
        #table name of faculty login(id and password)
        tab = "facultyLogin"

        c.execute('select * from ' +tab)
        attdata = c.fetchall()
        i = 0
        for row in attdata:
            if(row[0]==id and row[1]==password):
                i=i+1
        # directing it to the facutly page
        if(i==1):
            return render(request, 'home/faculty.html')
        else:
            return HttpResponse('Login unsuccessful')

# directing it to the student attendance page
def student1(request):
    return render(request, 'home/student.html')

# renders faculty form in home page
def homefaculty(request):
    form = NameForm()
    return render(request, 'home/homefaculty.html', {'form': form})

# renders student form in home page
def homestudent(request):
    return render(request, 'home/homestudent.html')

#rendering faculty page
def faculty(request):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    #collecting form data
    if request.method == 'POST':
        batchsel = request.POST.get('batch')
        sectionsel = request.POST.get('section')
        optionsel = request.POST.get('option')
        subjectsel = request.POST.get('subjectsel')
        studentsel = request.POST.get('studentsel')

        batch = batchsel
        section = sectionsel
        sub = subjectsel

        #returning response according to the option selected
        if(optionsel=='overall'):
            return overall(batch,section)
        if(optionsel=='subjectwise'):
            return subjectwise(batch,section,sub)
        if(optionsel=='studentwise'):
            return studentwise(batch,section,studentsel)

#rendering image for overall attendance
def overall(a,b):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    batch = a
    section = b
    
    fig = Figure()

    conn = sqlite3.connect('cse.db')
    c = conn.cursor()

    #accept from web page
    year = batch
    sec = section
    tab = 'cse'+year+sec

    #plotting data 
    roll_no = list()
    no_of_classes_attended = list()
    roll_no1 = list()
    no_of_classes_attended1 = list()

    c.execute('select * from ' +tab)
    attdata = c.fetchall()
    i = 0
    sum=0
    for row in attdata:
        if(i==0):
            for j in range(len(row)-1):
                    sum=sum+row[j+1]
            tot_classes = str(sum)
            i += 1
            sum=0
        else:
            if(i<31):
                var = row[0]
                roll_no.append(var[0:2]+'-'+var[len(var)-2:])
                for j in range(len(row)-1):
                    sum=sum+row[j+1]
                no_of_classes_attended.append(sum)
                i += 1
                sum=0
            else:
                var = row[0]
                roll_no1.append(var[0:2]+'-'+var[len(var)-2:])
                for j in range(len(row)-1):
                    sum=sum+row[j+1]
                no_of_classes_attended1.append(sum)
                i+= 1
                sum=0


    #calculate 75%
    p75=75*int(tot_classes)/100

    #calculate 65%
    p65=65*int(tot_classes)/100

    #calculate 50%
    p50=50*int(tot_classes)/100

    #create subplots
    fig= Figure()
    ax1=fig.add_subplot(211)
    ax2=fig.add_subplot(212)

    #BAR GRAPH 1
    bar_width = 0.4
    x_pos = np.arange(len(roll_no))
    ax1.bar(x_pos + bar_width, no_of_classes_attended,color='midnightblue',align='center')
    ax1.set_xticks(x_pos + bar_width)
    ax1.set_xticklabels(roll_no,rotation=30)
    ax1.set_ylabel('NUMBER OF CLASSES\n')


    #writing inside the bar
    x=0
    for i in no_of_classes_attended:
        ax1.text(x + bar_width,i-15,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;

    #BAR GRAPH 2
    bar_width = 0.4
    x_pos = np.arange(len(roll_no1))
    ax2.bar(x_pos + bar_width, no_of_classes_attended1,color='midnightblue',align='center')
    ax2.set_xticks(x_pos + bar_width)
    ax2.set_xticklabels(roll_no1,rotation=30)
    ax2.set_ylabel('NUMBER OF CLASSES\n')
    ax2.set_xlabel('\nHALLTICKET NUMBERS')

    #writing inside the bar
    x=0
    for i in no_of_classes_attended1:
        ax2.text(x + bar_width,i-15,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;
        
    #green line
    ax1.axhline(y=p75, linewidth=2, color='green')
    ax2.axhline(y=p75, linewidth=2, color='green')

    #yellow line
    ax1.axhline(y=p65, linewidth=2, color='gold')
    ax2.axhline(y=p65, linewidth=2, color='gold')

    #red line
    ax1.axhline(y=p50, linewidth=2, color='red')
    ax2.axhline(y=p50, linewidth=2, color='red')

    ax1.set_title('BAR CHART OF ATTENDANCE OF STUDENTS\n')

    #ax.grid(True)
    #fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20, 10.5, forward=True)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')

    canvas.print_png(response)
    canvas.print_figure('home/static/home/graphs/clstot.png')

    return response

#rendering image for a single student's attendance
def student(request):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    
    if request.method == 'POST':
        hallt = request.POST.get('hallticket')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        
        studentsel = hallt.upper()

        #Database connection
        conn = sqlite3.connect('cse.db')
        c = conn.cursor()

        #accept from web page
        roll=hallt.upper()
        year=batch
        sec=section
        
        #Calculations
        #make table name
        tab = 'cse'+year+sec

        #extract all classes for the particular student
        c.execute("select * from "+tab+" where htno='"+roll+"'")
        attdata = c.fetchall()

        #caluculate sum of all classes
        sum=0.0
        for row in attdata:
            j=1
            for i in row:
                if(j==1):
                    j=2
                    continue
                sum=sum+i
                   
        #extract total classes in all subjects
        c.execute("select * from "+tab+" where htno='total'")
        attdata = c.fetchall()

        #calculate sum of total classes held
        tsum=0.0
        for row in attdata:
            j=1
            for i in row:
                if(j==1):
                    j=2
                    continue
                tsum=tsum+i
                
        #calculate attendance percentage
        percent1=round(((sum/tsum)*100),2)

        #print percent

        #html = "<html><body><h1>%s</h1></body></html>" % str(percent)

        #Establishing the connection
        year = batch
        sec = section
        tab = 'cse'+year+sec
        #name='daa'
        conn = sqlite3.connect('cse.db')
        c = conn.cursor()
        cursor = conn.execute('select * from '+tab)
        sub_name=list()
        sub_name = [description[0] for description in cursor.description]
        indexvalue = 1
        sub_name.remove('htno')
        roll=studentsel

        #Generating number of the classes lists
        classes =list()
        tot_class =list()
        c.execute('select * from ' +tab+ ' where htno=\''+roll+'\'')
        attdata = c.fetchall()
        for row in attdata:
            row = list(row)
            subatt = row.pop(indexvalue)
            row.pop(0)
            classes = row
            classes = [subatt] + classes
        c.execute('select * from ' +tab+ ' where htno=\'total\'')
        attdata = c.fetchall()
        for row in attdata:
            row = list(row)
            totsubatt = row.pop(indexvalue)
            row.pop(0)
            tot_class = row
            tot_class = [totsubatt] + tot_class

        #create percentage list
        percent=list()
        for i in range(0,len(tot_class)):
            p=round(((float(classes[i])/float(tot_class[i]))*100),1)
            percent.append(p)

        #create lables and explode values for pie chart
        explode=[0.1]    
        labels=list()
        for i in range(0,len(percent)): 
            labels.append(sub_name[i]+'\n('+str(percent[i])+'%)')
            if(i==0):continue
            explode.append(0)
           

        colors = ['yellowgreen', 'lightcoral','gold','lightblue','plum']        

        #pie chart
        plt.pie(percent, labels=labels, colors=colors, shadow=True, startangle=90)
                
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        #title
        S='COMPARISION OF CLASSES ATTENDED BY STUDENT '+roll+'\nIN ALL SUBJECTS \n\n'
        plt.title(S)
        plt.tight_layout()

        savefig('home/static/home/graphs/stutot.png', transparent="True")
        
        plt.cla()
        plt.clf()
        
    return render(request, 'home/student.html', {'perstu':percent1,'clsatt':sum,'totatt':tsum})

#rendering image for subjectwise attendance
def subjectwise(a,b,c):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    batch = a
    section = b
    sub = c

    fig = Figure()

    conn = sqlite3.connect('cse.db')
    c = conn.cursor()

    #accept from web page
    year = batch
    sec = section
    subject = sub
    tab = 'cse'+year+sec

    #plotting data 
    roll_no = list()
    no_of_classes_attended = list()
    roll_no1 = list()
    no_of_classes_attended1 = list()

    c.execute('select htno, ' +subject+' from ' +tab)
    attdata = c.fetchall()
    i = 0
    for row in attdata:
        if(i==0):
            tot_classes = str(row[1])
            i += 1
        else:
            if(i<31):
                var = row[0]
                roll_no.append(var[0:2]+'-'+var[len(var)-2:])
                no_of_classes_attended.append(row[1])
                i += 1
            else:
                var = row[0]
                roll_no1.append(var[0:2]+'-'+var[len(var)-2:])
                no_of_classes_attended1.append(row[1])
                i+= 1
    c.close()
    conn.close()

    #calculate 75%
    p75=75*int(tot_classes)/100

    #calculate 65%
    p65=65*int(tot_classes)/100

    ax1=fig.add_subplot(211)
    ax2=fig.add_subplot(212)

    #BAR GRAPH 1
    bar_width = 0.4
    x_pos = np.arange(len(roll_no))
    ax1.bar(x_pos + bar_width, no_of_classes_attended,color='midnightblue',align='center')
    ax1.set_xticks(x_pos + bar_width)
    ax1.set_xticklabels(roll_no,rotation=30)
    ax1.set_ylabel('NUMBER OF CLASSES\n')

    #writing inside the bar
    x=0
    for i in no_of_classes_attended:
        ax1.text(x + bar_width,i-2,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;

    #BAR GRAPH 2
    bar_width = 0.4
    x_pos = np.arange(len(roll_no1))
    ax2.bar(x_pos + bar_width, no_of_classes_attended1,color='midnightblue',align='center')
    ax2.set_xticks(x_pos + bar_width)
    ax2.set_xticklabels(roll_no1,rotation=30)
    ax2.set_ylabel('NUMBER OF CLASSES\n')
    ax2.set_xlabel('\nHALLTICKET NUMBERS')

    #writing inside the bar
    x=0
    for i in no_of_classes_attended1:
        ax2.text(x + bar_width,i-2,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;

    #green line
    s=tot_classes+"\n100%"
    ax1.axhline(y=int(tot_classes), linewidth=2, color='green',label="")
    ax2.axhline(y=int(tot_classes), linewidth=2, color='green',label="")

    #yellow line
    ax1.axhline(y=p75, linewidth=2, color='gold')
    ax2.axhline(y=p75, linewidth=2, color='gold')

    #red line
    ax1.axhline(y=p65, linewidth=2, color='red')
    ax2.axhline(y=p65, linewidth=2, color='red')

    #plt.legend(('green','gold','red'), ('100%', '75%','60%'))
    roman={'13':'IV','14':'III','15':'II','16':'I'}
    ax1.set_title('ATTENDANCE OF '+roman[batch]+' CSE '+section.upper()+' IN '+subject.upper()+'\n')



    #ax.grid(True)
    #fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20, 10.5, forward=True)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')

    canvas.print_png(response, transparent="True")
    canvas.print_figure('home/static/home/graphs/clssub.png')

    return response
    
#rendering image for studentwise attendance
def studentwise(a,b,c):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    batch = a
    section = b
    studentsel = c.upper()
    

    #Establishing the connection
    year = batch
    sec = section
    tab = 'cse'+year+sec
    conn = sqlite3.connect('cse.db')
    c = conn.cursor()
    cursor = conn.execute('select * from '+tab)
    sub_name=list()
    sub_name = [description[0] for description in cursor.description]
    indexvalue =1
    sub_name.remove('htno')
    roll=studentsel

    #Generating number of the classes lists
    classes =list()
    tot_class =list()
    c.execute('select * from ' +tab+ ' where htno=\''+roll+'\'')
    attdata = c.fetchall()
    for row in attdata:
        row = list(row)
        subatt = row.pop(indexvalue)
        row.pop(0)
        classes = row
        classes = [subatt] + classes
    c.execute('select * from ' +tab+ ' where htno=\'total\'')
    attdata = c.fetchall()
    for row in attdata:
        row = list(row)
        totsubatt = row.pop(indexvalue)
        row.pop(0)
        tot_class = row
        tot_class = [totsubatt] + tot_class

    #create percentage list
    percent=list()
    for i in range(0,len(tot_class)):
        p=round(((float(classes[i])/float(tot_class[i]))*100),1)
        percent.append(p)

    #create lables and explode values for pie chart
    explode=[0.1]    
    labels=list()
    for i in range(0,len(percent)): 
        labels.append(sub_name[i]+'\n('+str(percent[i])+'%)')
        if(i==0):continue
        explode.append(0)
       

    colors = ['yellowgreen', 'lightcoral','gold','lightblue','plum']    

    #pie chart
    plt.pie(percent, labels=labels, colors=colors, shadow=True, startangle=90)
            
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    #title
    S='COMPARISION OF CLASSES ATTENDED BY STUDENT '+roll+'\nIN ALL SUBJECTS \n\n'
    plt.title(S)
    plt.tight_layout()

    response = HttpResponse(content_type="image/jpeg")
    savefig(response)

    plt.cla()
    plt.clf()

    return response
