# attendance_analyser

A Django based application that would be used to display the attendance of students along with necessary graphs. 

There are two modules to the application:
 
One for students where they can: 
  > See their aggregate attendance.
  > See a pie chart comparing their attendance in all the subjects.
  > Use two handy metrics, one for calculating future attendance and the other for make up attendance.

Other for faculty where they can: 
  > View the attendance of a particular student.
  > View the attendance of a particular subject.
  > View the attendance of a whole class with its respective graph.
  
For the purpose of demonstration we used a sample database (cse.db) that contains: 
> The attendance of students of 2 batches (academic years), where each batch has four sections (A, B, C, D), which correspond to total of 8 tables. 
  Each table consists of one column for roll number (ID) of a student, and other columns for the attendance count in various subjects.
  The first row of each table consists of the total number of classes (till that date) in various subjects (under the ID 'total').
> A table containing the credentials (IDs and passwords) of faculty.

The graphs are generated using 'matplotlib' library ( http://matplotlib.org/ ) in Python.

To run the application on your computer, clone the repository onto your computer and execute command "manage.py runserver" in command line (cmd for Windows). Then go to http://127.0.0.1:8000/ on a browser.
P.S.: Make your current directory as the repository cloned. 

Credentials for demo:
Faculty:
> ID: FACSE1234
> Password: Guest1
Student:
> Hallticket: 14h61a0501
> Batch: 14
> Section: a

Following are screenshots of the project:

![screenshot 9](https://cloud.githubusercontent.com/assets/16423060/21471588/1034f012-cadd-11e6-8d56-369fa0c84362.png)
![screenshot 10](https://cloud.githubusercontent.com/assets/16423060/21471587/1034d974-cadd-11e6-8b43-0692135d7f0a.png)
![screenshot 11](https://cloud.githubusercontent.com/assets/16423060/21471589/10350584-cadd-11e6-948e-a728043edffe.png)
![screenshot 12](https://cloud.githubusercontent.com/assets/16423060/21471590/103567cc-cadd-11e6-877c-6fe1143bfea9.png)
![screenshot 13](https://cloud.githubusercontent.com/assets/16423060/21471592/103ac87a-cadd-11e6-913b-322b245c9bc6.png)
![screenshot 14](https://cloud.githubusercontent.com/assets/16423060/21471591/1037170c-cadd-11e6-8669-8c38be356027.png)
![screenshot 15](https://cloud.githubusercontent.com/assets/16423060/21471593/105e93a4-cadd-11e6-8ebd-8f6d491f6c92.png)
![screenshot 16](https://cloud.githubusercontent.com/assets/16423060/21471594/105f04ba-cadd-11e6-8c69-0e03ae974ab5.png)
![screenshot 17](https://cloud.githubusercontent.com/assets/16423060/21471595/105fad5c-cadd-11e6-88b4-851dd6e75cfb.png)
![screenshot 18](https://cloud.githubusercontent.com/assets/16423060/21471596/10605d24-cadd-11e6-93bc-af61259f672a.png)
![screenshot 19](https://cloud.githubusercontent.com/assets/16423060/21471597/10647df0-cadd-11e6-8d69-2da9622e28bf.png)
![screenshot 20](https://cloud.githubusercontent.com/assets/16423060/21471598/1064ae9c-cadd-11e6-955e-e9b13db3dc43.png)
![screenshot 21](https://cloud.githubusercontent.com/assets/16423060/21471599/1088e6fe-cadd-11e6-8791-0c24b9ef4b3e.png)
![screenshot 22](https://cloud.githubusercontent.com/assets/16423060/21471602/108b23d8-cadd-11e6-8a6d-00404c0c9dde.png)
![screenshot 23](https://cloud.githubusercontent.com/assets/16423060/21471601/10899c70-cadd-11e6-8d72-4b473824e412.png)

Check 'Demo' directory for screenshots of the project if images are not visible.

Python version: 2.7.12
Django version: 1.10.1
