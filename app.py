from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_mysqldb import MySQL
from xhtml2pdf import pisa
from config import Config
from datetime import datetime
import io

app = Flask(__name__)

app.config.from_object(Config)


mysql = MySQL(app)

#index
@app.route('/')
def index():
    return render_template('index.html')


#homepage
@app.route("/Home")
def Home():
    return render_template('index.html')


#login page
@app.route("/login")
def login():
    return render_template('login.html')



#switching between user and admin
@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        con = mysql.connection.cursor()
        
 
        con.execute("SELECT Password,role FROM users WHERE Mail_ID = %s", [user_email])
        
       
        user_data = con.fetchone()
        
        if user_data is None:
            message = 'Invalid email'
            message_type = 'danger'
        else:
            stored_password = user_data[0]
            user_role = user_data[1] 
            if user_password == stored_password:
                message = 'Login successful!'
                message_type = 'success'
                if user_role == 'admin':
                    return redirect(url_for('admin_dashboard'))  
                else:
                    return redirect(url_for('user_dashboard'))  
            
            else:
                message = 'Invalid password. Please try again.'
                message_type = 'danger'
        
        con.close()

        
        return render_template('login.html', message=message, message_type=message_type)

    return render_template('login.html')




#admin login
@app.route('/admin_dashboard')
def admin_dashboard():
    # Admin dashboard logic
    con=mysql.connection.cursor()
    sql="SELECT * from event"
    con.execute(sql)
    res=con.fetchall()
    return render_template('admin_dashboard.html',datas=res)




#create event
@app.route("/create_event",methods=['GET','POST'])
def create_event():
    if request.method=='POST':
        name=request.form['name']
        description=request.form['description']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        location=request.form['location']
        capacity=request.form['capacity']
        organizer=request.form['organizer']
        category=request.form['category']
        con=mysql.connection.cursor()
        sql="insert into event(name,description,start_date,end_date,location,capacity,organizer,categories) value ( %s,%s,%s,%s,%s,%s,%s,%s)"
        con.execute(sql,[name,description,start_date,end_date,location,capacity,organizer,category])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("admin_dashboard"))

    return render_template("create_event.html")



#view Registrants
@app.route('/view_registrants')
def view_registrants():
    con=mysql.connection.cursor()
    sql="SELECT Name,Dob,Phone,Mail_ID,Role from users"
    con.execute(sql)
    res=con.fetchall()
    
    con=mysql.connection.cursor()
    sql="SELECT * from registration"
    con.execute(sql)
    datas=con.fetchall()

    con=mysql.connection.cursor()
    sql="SELECT * from ticket"
    con.execute(sql)
    ticket=con.fetchall()

    return render_template('view_registrants.html',res=res,datas=datas,ticket=ticket)




#report generation
@app.route('/generate_report')
def generate_report():
    
    con=mysql.connection.cursor()
    sql="SELECT Name,Dob,Phone,Mail_ID,Role from users"
    con.execute(sql)
    users=con.fetchall()
    
    con=mysql.connection.cursor()
    sql="SELECT * from event"
    con.execute(sql)
    events=con.fetchall()

    con=mysql.connection.cursor()
    sql="SELECT * from ticket"
    con.execute(sql)
    ticket=con.fetchall()  

    rendered = render_template('report.html', users=users, events=events, ticket=ticket)

    
    pdf_file = io.BytesIO()
    pisa.CreatePDF(io.StringIO(rendered), dest=pdf_file)

    
    response = make_response(pdf_file.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

    return response





#edit event
@app.route("/edit_event/<string:id>",methods=['GET','POST'])
def edit_event(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        description=request.form['description']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        location=request.form['location']
        capacity=request.form['capacity']
        organizer=request.form['organizer']
        category=request.form['category']
        sql="update event set name=%s,description=%s,start_date=%s,end_date=%s,location=%s,capacity=%s,organizer=%s,categories=%s where event_id=%s"
        con.execute(sql,[name,description,start_date,end_date,location,capacity,organizer,category,id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("admin_dashboard"))
    con=mysql.connection.cursor()
    sql="select * from event where event_id=%s"
    con.execute(sql,[id])
    datas=con.fetchone()
    return render_template("edit_event.html", datas=datas)




#delete Event
@app.route("/delete_event/<string:id>",methods=['GET','POST'])
def delete_event(id):
    con=mysql.connection.cursor()
    sql="delete from event where event_id=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    return redirect(url_for("admin_dashboard"))



#user login
@app.route('/user_dashboard')
def user_dashboard():
    # User dashboard logic
    con=mysql.connection.cursor()
    sql="SELECT * from event"
    con.execute(sql)
    res=con.fetchall()
    return render_template('user_dashboard.html',datas=res)



#book event
@app.route("/book_event/<string:id>", methods=['GET', 'POST'])
def book_event(id):
    con = mysql.connection.cursor()  

    sql = "SELECT name FROM event WHERE event_id = %s"
    con.execute(sql, [id])
    datas = con.fetchone()

    if not datas:
       
        con.close()
        return "Event not found", 404

    if request.method == 'POST':
        
        name = request.form['attendee_name']
        mail = request.form['attendee_mail']
        phone = request.form['attendee_phone']
        registration_date = datetime.now()

       
        sql = """
            INSERT INTO registration (event_id, attendee_name, attendee_phone, attendee_email, registration_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        con.execute(sql, [id, name, phone, mail, registration_date])
        mysql.connection.commit()

        
        con.close()
        return redirect(url_for("tickets", id=id))

    
    con.close()
    return render_template('book_event.html', datas=datas)




#tickets 
@app.route("/tickets/<string:id>",methods=['GET','POST'])
def tickets(id):
     if request.method == 'POST':
        mail = request.form['mail']
        price = request.form['total_amount']
        quantity = request.form['quantity']
        ticket_type = request.form['category']          
        con=mysql.connection.cursor()
        sql="insert into ticket(Mail,price,quantity,ticket_type,event_id) value (%s, %s, %s, %s, %s)"
        con.execute(sql,[mail,price,quantity,ticket_type,id])
        mysql.connection.commit()
        con.close()
        con=mysql.connection.cursor()
        sql="select name from event where event_id=%s"
        con.execute(sql,[id])
        res=con.fetchone()
        return redirect(url_for("user_dashboard"))
     return render_template("tickets.html")


#view tickets
@app.route("/view_tickets", methods=['GET', 'POST'])
def view_tickets():
    if request.method == 'POST':
        user_email = request.form['mail']
        con = mysql.connection.cursor()

        
        sql = "SELECT * FROM ticket WHERE Mail = %s"
        con.execute(sql, [user_email])
        tickets = con.fetchall()
        con.close()

        print("Tickets fetched for email:", user_email)
        print("Tickets:", tickets)

        if tickets:
            return render_template('view_tickets.html', tickets=tickets)
        else:
            message = 'No tickets found for this email'
            message_type = 'warning'
            
            return redirect(url_for("view_tickets",message=message, message_type=message_type))
            

    return render_template('view_tickets.html', tickets=None)


#ticket report
@app.route('/generate_ticket_pdf', methods=['GET'])
def generate_ticket_pdf():
    user_email = request.args.get('mail') 
    if not user_email:
        return "Email parameter is missing.", 400

        
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM ticket WHERE Mail = %s"
    cursor.execute(query, (user_email,))
    tickets = cursor.fetchall()
    cursor.close()

    if not tickets:
        
        return "No tickets found for the provided email.", 404

   
    html_content = render_template('tickets_reports.html', tickets=tickets)

    
    pdf_output = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html_content.encode('utf-8')), dest=pdf_output)

    
    if pisa_status.err:
        return "Error generating PDF", 500

    
    pdf_output.seek(0)

    
    response = make_response(pdf_output.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{user_email}_tickets.pdf"'

    return response



#new user registration
@app.route("/user_reg")
def user_reg():
    return render_template('user_reg.html')


#registration form
@app.route("/adduser", methods=['GET','POST'])
def adduser():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_dob = request.form['user_dob']
        user_phone = request.form['user_phone']
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        role = ' user' 
        con=mysql.connection.cursor()
        sql="insert into users(Name,Dob,Phone,Mail_ID,Password,role) value (%s, %s, %s, %s, %s, %s)"
        con.execute(sql,[user_name,user_dob,user_phone,user_email,user_password,role])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("login"))

    return render_template('user_reg.html')

if __name__ == '__main__':
    app.run(debug=True)
