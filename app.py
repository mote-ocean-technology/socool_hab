import sys
from flask import Flask, render_template, flash, redirect, request
from flask.ext.basicauth import BasicAuth
import MySQLdb
import collections
from logging.handlers import RotatingFileHandler
import json
import ast
from datetime import *
from types import *
#
sys.path.insert(0, './static/python')
from socool_utils import *
from forms import opdDeploymentForm

app = Flask(__name__)
app.config.from_object('config')
app.config['BASIC_AUTH_USERNAME'] = 'oceantech'
app.config['BASIC_AUTH_PASSWORD'] = 'm0t3_ot'
basic_auth = BasicAuth(app)

#routes
@app.route('/login/opd/deploy/update', methods=['POST'])
@basic_auth.required
def update():

    conn = connect_db_socool()
    cursor =  conn.cursor(MySQLdb.cursors.DictCursor)

    serial = int(request.form['serial'])
    operator = request.form['operator']
    deployed = request.form['deployed']
    site = request.form['site']

    if deployed == '':
        deployed = '0000-00-00T00:00:00'

    update_query = "update sites set serial = %s, operator = '%s', \
deployed='%s' where site = '%s'" % (serial, operator, deployed, site)

    try:
        cursor.execute(update_query)
    except MySQLdb.Error as e:
        print "Query failed. Error: %s" % e
        return
    cursor.execute('commit')
    nav_links = get_nav_links()
    sites = get_sites();

    cursor.close()
    conn.close()
    return render_template('opd.html',
nav_links=nav_links, sites=sites)

@app.route('/login/opd/deploy/<site>', methods=['GET','POST'])
def opdDeploy(site):
    partners = get_partners()
    home_apps = get_home_apps()
    nav_links = get_nav_links()
    site = get_site(site)

    form = opdDeploymentForm()
    #Build serial number choices the pythonic way
    #[TO DO] db query and eliminate already deployed serials from the list
    serial_choices = build_serial_list()

    operator_choices = [('Mote','Mote'), ('Mote/FWRI','Mote/FWRI'),
('Mote/SCCF','Mote/SCCF'),('Mote/GCOOS','Mote/GCOOS'),
('Mote/USF','Mote/USF'),('NOAA','NOAA')]
    form.serial.choices=serial_choices
    form.operator.choices=operator_choices
    form.serial.data = site['serial']
    form.site.data = site['site']
    form.operator.data = site['operator']
    form.deployed.data = site['deployed']

    return render_template('opdDeploy.html',
                          title='Deploy/Retrieve OPD',
                          partners=partners,
                          home_apps=home_apps,
                          nav_links=nav_links,
                          form=form)

@app.route('/plots/<site>/<param>')
def plot(site, param):
  opdData = get_graph_data(site, param)
  opdData = str(opdData)
  opdData = opdData.replace("'","")
  return  opdData

@app.route('/testing')
def testing():
    print "testing()"
    partners = get_partners()
    home_apps = get_home_apps()
    nav_links = get_nav_links()
    return render_template('testing.html', partners=partners, home_apps=home_apps,\
 nav_links=nav_links)

@app.route('/home')
def home():
    partners = get_partners()
    home_apps = get_home_apps()
    nav_links = get_nav_links()
    return render_template('home.html', partners=partners, home_apps=home_apps,\
 nav_links=nav_links)

@app.route('/netlog')
def netlog():
    nav_links = get_nav_links()
    net_log = get_netlog()
    return render_template('netlog.html', nav_links=nav_links, \
net_log = net_log)

@app.route('/')
def root():
    partners = get_partners()
    home_apps = get_home_apps()
    nav_links = get_nav_links()
    return render_template('home.html',partners=partners, home_apps=home_apps,\
 nav_links=nav_links)


@app.route('/gliderops')
def gliderops():
    nav_links = get_nav_links()
    ops = get_gliderops_data()
    return render_template('gliderops.html',ops=ops,\
 nav_links=nav_links)


@app.route('/gliderops/deployments')
def deployments():
    nav_links = get_nav_links()
    active_gliders = get_glider_data()
    return render_template('deployments.html',active_gliders=active_gliders,\
 nav_links=nav_links)

@app.route('/gliderops/summaries')
def summaries():
    nav_links = get_nav_links()
    data_img = 'chart.png'
    kmz_img = 'kml_icon.jpg'
    data, tableHeaders = fetch_glider_data()

    return render_template('glider_summary.html',headers=tableHeaders,data=data,
d_i=data_img,k_i=kmz_img,nav_links=nav_links)

@app.route('/fixed')
def fixed():
    nav_links = get_nav_links()
    inactive_sites, active_sites = get_opd_data()
    return render_template('fixed.html', inactive_sites=inactive_sites,
active_sites=active_sites, nav_links=nav_links)

@app.route('/products/<interval>')
def products(interval):
    nav_links = get_nav_links()
    active_sites = get_opd_historical(int(interval))
    return render_template('products.html', active_sites=active_sites,
nav_links=nav_links)

#menu items
@app.route('/about')
def about():
    nav_links = get_nav_links()
    return render_template('about.html', nav_links=nav_links)

@app.route('/people')
def people():
    nav_links = get_nav_links()
    staff = get_people_data()
    return render_template('people.html', staff=staff,
nav_links=nav_links)

@app.route('/technology')
def technology():
    nav_links = get_nav_links()
    tech = get_technology_data()
    return render_template('technology.html',tech=tech,
nav_links=nav_links)

@app.route('/documents')
def publications():
    nav_links = get_nav_links()
    publication_types = get_publications_data()
    return render_template('documents.html',pubtypes=publication_types,
nav_links=nav_links)

@app.route('/documents/presentations')
def presentations():
    nav_links = get_nav_links()
    presentations = get_presentations()
    return render_template('presentations.html',presentations=presentations,
nav_links=nav_links)

@app.route('/documents/techdocs')
def techdocs():
    nav_links = get_nav_links()
    tech_docs = get_techdocs()
    return render_template('techdocs.html',tech_docs=tech_docs,
nav_links=nav_links)

@app.route('/documents/instrumentdocs')
def instrument_docs():
    nav_links = get_nav_links()
    inst_docs = get_inst_docs()
    return render_template('instrumentdocs.html',inst_docs=inst_docs,
nav_links=nav_links)

@app.route('/documents/gliderdocs')
def glider_docs():
    nav_links = get_nav_links()
    glider_docs = get_glider_docs()
    return render_template('gliderdocs.html',glider_docs=glider_docs,
nav_links=nav_links)

@app.route('/contact')
def contact():
    partners = get_partners()
    home_apps = get_home_apps()
    nav_links = get_nav_links()
    return render_template('contact.html',partners=partners, home_apps=home_apps,\
 nav_links=nav_links)

@app.route('/login')
@basic_auth.required
def login():
    nav_links = get_nav_links()
    apps = get_apps_data()
    return render_template('staffapps.html', apps=apps,
nav_links=nav_links)

@app.route('/login/sop')
@basic_auth.required
def sop():
    nav_links = get_nav_links()
    sop = get_sop_docs()
    return render_template('sop.html', sop=sop,
nav_links=nav_links)

@app.route('/login/opd')
def opd():
    nav_links = get_nav_links()
    sites = get_sites();
    return render_template('opd.html',
nav_links=nav_links, sites=sites)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
