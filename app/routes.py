from flask import Flask, render_template, url_for, request, redirect, flash
from app import app, db
from app.models import User
from app.models_extended import Agent, Career, Consultation, Contact, Property, Valuation, Client
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# --- Core Pages ---
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/l', methods=['GET', 'POST'])  # Also map '/l' if links point there
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash('Login successful!', 'success')
            return redirect('/h')
        else:
            flash('Invalid email or password', 'danger')
    return render_template('l.html')

@app.route('/h')  # Also map '/h' if links point there
def home():
    return render_template('h.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'danger')
            return redirect('/register')
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect('/login')
    return render_template('register.html')

# --- Agent Routes ---
@app.route('/agent/new', methods=['GET', 'POST'])
def new_agent():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        agency = request.form.get('agency')

        existing_agent = Agent.query.filter_by(email=email).first()
        if existing_agent:
            flash('An agent with this email already exists.', 'danger')
            return redirect(url_for('new_agent'))

        new_agent = Agent(name=name, email=email, phone=phone, agency=agency)
        db.session.add(new_agent)
        db.session.commit()
        flash('Agent added successfully!', 'success')
        return redirect(url_for('agent_list'))
    return render_template('agent_form.html')

@app.route('/agent-dashboard')
def agent_list():
    agents = Agent.query.all()
    return render_template('agent-dashboard.html', agents=agents)

# --- Client Routes ---
@app.route('/clients', methods=['GET', 'POST'])
def client_list():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        existing_client = Client.query.filter_by(email=email).first()
        if existing_client:
            flash('A client with this email already exists.', 'danger')
            return redirect(url_for('client_list'))

        new_client = Client(name=name, email=email, phone=phone)
        db.session.add(new_client)
        db.session.commit()
        flash('Client added successfully!', 'success')
        return redirect(url_for('client_list'))

    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/client/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted successfully!', 'success')
    return redirect(url_for('client_list'))

# --- Career Routes ---
@app.route('/careers')
def careers():
    careers = Career.query.all()
    return render_template('careers.html', careers=careers)

@app.route('/career/new', methods=['GET', 'POST'])
def new_career():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_career = Career(title=title, description=description)
        db.session.add(new_career)
        db.session.commit()
        flash('Career added successfully!', 'success')
        return redirect(url_for('careers'))
    return render_template('career_form.html')

# --- Contact Routes ---
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect('/contact')
    return render_template('contact.html')

# --- Property Routes ---
@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/property/new', methods=['GET', 'POST'])
def new_property():
    if request.method == 'POST':
        title = request.form.get('title')
        address = request.form.get('address')
        agent_id = request.form.get('agent_id')
        description = request.form.get('description')
        price = request.form.get('price')
        new_property = Property(title=title, address=address, agent_id=agent_id, description=description, price=price)
        db.session.add(new_property)
        db.session.commit()
        flash('Property added successfully!', 'success')
        return redirect(url_for('properties'))
    return render_template('property_form.html')

# --- Valuation Routes ---
@app.route('/valuation', methods=['GET', 'POST'])
def valuation():
    if request.method == 'POST':
        property_id = request.form.get('property_id')
        value = request.form.get('value')
        new_valuation = Valuation(property_id=property_id, value=value)
        db.session.add(new_valuation)
        db.session.commit()
        flash('Valuation submitted successfully!', 'success')
        return redirect('/')
    return render_template('valuation.html')

# --- Consultation Routes ---
@app.route('/consultation/new', methods=['GET', 'POST'])
def new_consultation():
    if request.method == 'POST':
        client_name = request.form.get('client_name')
        client_email = request.form.get('client_email')
        agent_id = request.form.get('agent_id')
        date_str = request.form.get('date')
        notes = request.form.get('notes')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('new_consultation'))
        new_consultation = Consultation(client_name=client_name, client_email=client_email, agent_id=agent_id, date=date, notes=notes)
        db.session.add(new_consultation)
        db.session.commit()
        flash('Consultation added successfully!', 'success')
        return redirect(url_for('consultation_list'))
    agents = Agent.query.all()
    return render_template('consultation_form.html', agents=agents)

@app.route('/consultation')
def consultation_list():
    consultations = Consultation.query.all()
    return render_template('consultation.html', consultations=consultations)

# --- Additional Routes for remaining templates ---

@app.route('/about')
def about():
    return render_template('about.html')

from app.models_extended import Property, Client, Consultation

@app.route('/admin')
def admin():
    total_properties = Property.query.count()
    active_listings = Property.query.count()  # Assuming all properties are active for now
    pending_approvals = 0  # Placeholder, implement if applicable
    total_revenue = db.session.query(db.func.sum(Property.price)).scalar() or 0

    recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()
    recent_consultations = Consultation.query.order_by(Consultation.date.desc()).limit(5).all()

    return render_template('admin.html',
                           total_properties=total_properties,
                           active_listings=active_listings,
                           pending_approvals=pending_approvals,
                           total_revenue=total_revenue,
                           recent_properties=recent_properties,
                           recent_consultations=recent_consultations)

@app.route('/ai')
def ai():
    return render_template('ai.html')

@app.route('/apartment1')
def apartment1():
    return render_template('apartment1.html')

@app.route('/apartment2')
def apartment2():
    return render_template('apartment2.html')

@app.route('/apartment3')
def apartment3():
    return render_template('apartment3.html')

@app.route('/apartment4')
def apartment4():
    return render_template('apartment4.html')

@app.route('/apartment5')
def apartment5():
    return render_template('apartment5.html')

@app.route('/apartments')
def apartments():
    return render_template('apartments.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/buying-guide')
def buying_guide():
    return render_template('buying-guide.html')

@app.route('/consultation_form')
def consultation_form():
    return render_template('consultation_form.html')

@app.route('/cottage1')
def cottage1():
    return render_template('cottage1.html')

@app.route('/cottage2')
def cottage2():
    return render_template('cottage2.html')

@app.route('/cottage3')
def cottage3():
    return render_template('cottage3.html')

@app.route('/cottage4')
def cottage4():
    return render_template('cottage4.html')

@app.route('/cottage5')
def cottage5():
    return render_template('cottage5.html')

@app.route('/cozzy-cottage')
def cozzy_cottage():
    return render_template('cozzy-cottage.html')

@app.route('/due-diligence')
def due_diligence():
    return render_template('due-diligence.html')

@app.route('/environmental')
def environmental():
    return render_template('environmental.html')

@app.route('/f')
def f():
    return render_template('f.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/financing')
def financing():
    return render_template('financing.html')

@app.route('/guides')
def guides():
    return render_template('guides.html')

@app.route('/land-use')
def land_use():
    return render_template('land-use.html')

@app.route('/land-valuation')
def land_valuation():
    return render_template('land-valuation.html')

@app.route('/land1')
def land1():
    return render_template('land1.html')

@app.route('/land2')
def land2():
    return render_template('land2.html')

@app.route('/land3')
def land3():
    return render_template('land3.html')

@app.route('/land4')
def land4():
    return render_template('land4.html')

@app.route('/land5')
def land5():
    return render_template('land5.html')

@app.route('/listing-options')
def listing_options():
    return render_template('listing-options.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

@app.route('/modern1')
def modern1():
    return render_template('modern1.html')

@app.route('/modern2')
def modern2():
    return render_template('modern2.html')

@app.route('/modern3')
def modern3():
    return render_template('modern3.html')

@app.route('/modren-house')
def modren_house():
    return render_template('modren-house.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/rent')
def rent():
    return render_template('rent.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/sell')
def sell():
    return render_template('sell.html')

@app.route('/selling-process')
def selling_process():
    return render_template('selling-process.html')

@app.route('/surveying')
def surveying():
    return render_template('surveying.html')

@app.route('/tax-implications')
def tax_implications():
    return render_template('tax-implications.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/vacant-land')
def vacant_land():
    return render_template('vacant-land.html')

@app.route('/zoning-info')
def zoning_info():
    return render_template('zoning-info.html')
