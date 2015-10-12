import sys
from  connect_db import connect_db
from connect_db_socool import connect_db_socool
import MySQLdb
import json
from datetime import *
from types import *
import time

def build_serial_list():
    deployed = []
    choices=[]

    db = connect_db_socool()
    cursor = db.cursor()
    query = "select serial from sites where serial != 0"
    cursor.execute(query)
    results = cursor.fetchall()
    for serial in results:
        deployed.append(serial[0])

    cursor.close()
    db.close()

    for number in range(0,100):
        if number in deployed:
            next
        else:
            choices.append((number, number))
    return choices

def get_site(site):
    site_data = []
    conn = connect_db_socool()
    cursor =  conn.cursor(MySQLdb.cursors.DictCursor)
    site_query = "select * from sites where site = '%s'" % site
    cursor.execute(site_query)
    result = cursor.fetchall()
    for site in result:
        return site

def get_sites():
    sites = []
    conn = connect_db_socool()
    cursor =  conn.cursor(MySQLdb.cursors.DictCursor)
    #get opd status
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for opd logs
    site_query = "select * from sites order by deployed desc"
    cursor.execute(site_query)
    result = cursor.fetchall()
    for line in result:
      sites.append(line)
    cursor.close()
    conn.close()
    return sites

def get_netlog():
    net_log = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for opd logs
    log_query = "select from_unixtime(epoch) as DATETIME, logline \
from opd_logs where ascii(logline) < 128 AND from_unixtime(epoch) > (NOW() - INTERVAL 7 DAY) ORDER BY epoch DESC"
    cursor.execute(log_query)
    result = cursor.fetchall()
    for line in result:
      net_log.append(line)
    cursor.close()
    conn.close()
    return net_log

def get_nav_links():
    nav_links  = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    nav_query = "select title, url from nav_links \
ORDER BY display_order ASC"
    cursor.execute(nav_query)
    result = cursor.fetchall()
    for link in result:
      nav_links.append(link)
    cursor.close()
    conn.close()
    return nav_links


def get_partners():
    partners  = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    partner_query = "select partner, url, image from partners \
ORDER BY display_order ASC"
    cursor.execute(partner_query)
    result = cursor.fetchall()
    for partner in result:
      partners.append(partner)
    cursor.close()
    conn.close()
    return partners


def get_gliderops_data():
    ops  = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    ops_query = "select caption, url, image from glider_ops"
    cursor.execute(ops_query)
    result = cursor.fetchall()
    for op in result:
      ops.append(op)
    cursor.close()
    conn.close()
    return ops

def get_home_apps():
    home_apps  = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    home_app_query = "select title, url, image from home_apps \
ORDER BY display_order ASC"
    cursor.execute(home_app_query)
    result = cursor.fetchall()
    for app in result:
      home_apps.append(app)
    cursor.close()
    conn.close()
    return home_apps


def get_apps_data():
    apps  = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    app_query = "select caption, url, image from apps \
ORDER BY caption ASC"
    cursor.execute(app_query)
    result = cursor.fetchall()
    for app in result:
      apps.append(app)
    cursor.close()
    conn.close()
    return apps

def get_glider_data():
    active_gliders = []
    conn = connect_db_socool()
    socool_cursor =conn.cursor(MySQLdb.cursors.DictCursor)

    get_active_query = "select serial,operator,deployed from deployed_gliders \
ORDER BY serial ASC"
    socool_cursor.execute(get_active_query)
    actives = socool_cursor.fetchall()
    for active in actives:
        glider_query = "select operator, deployed_gliders.serial, deployed, \
sci_water_temp, horz_dist, dc_ratio, avg_speed, last_report, \
latitude, longitude from deployed_gliders,glider_data \
where deployed_gliders.serial = '%s' \
ORDER BY last_report DESC LIMIT 1;" % (active['serial'])

        socool_cursor.execute(glider_query)
        result = socool_cursor.fetchall()
        for glider in result:
            #Date math to calculate days_wet
            current_date = date.today()
            days_wet = (current_date - glider['deployed'])
            glider['days_wet'] = days_wet.days
            glider['deployed']  = glider['deployed'].strftime('%Y-%m-%d')
            glider['last_report'] = glider['last_report'].strftime('%Y-%m-%d %H:%M')
            glider['epoch'] = int(time.mktime(time.strptime(glider['last_report'], '%Y-%m-%d %H:%M')))
            glider['time_delta'] = int(time.time() - glider['epoch'])

            for key, value in glider.iteritems():
                if type(value) is LongType:
                    glider[key] = int(value)
            active_gliders.append(glider)

    socool_cursor.close()
    conn.close()
    return active_gliders


def get_opd_data():
    inactive_sites = []
    conn = connect_db_socool()
    socool_cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    site_cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    inactive_query = "select site, latitude, longitude from sites where serial = 0";
    socool_cursor.execute(inactive_query)
    result = socool_cursor.fetchall()
    for site in result:
      inactive_sites.append(site)

    active_sites = []
    #conn = connect_db()
    #cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #active_cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #[TO DO] Need to add query to get all 'ACTIVE' serials here
    #and then do a for serial in cursor: query

    get_active_query = "select serial,operator,deployed,site \
from sites where status='active' and serial != '' ORDER BY serial ASC";
    socool_cursor.execute(get_active_query)
    actives = socool_cursor.fetchall()
    for active in actives:
        active_data_query = " select voltage, pressure_drop, error_code, \
integration_time, water_vol, date,cdom_slope, intercept, similarity_index, \
target_model,sites.site, sites.serial, sites.operator, sites.deployed,\
sites.latitude, sites.longitude from opd_data,sites where \
opd_data.serial = '%d' and opd_data.serial = sites.serial and \
sites.status = 'active' order by date \
desc limit 1" % active['serial']

        socool_cursor.execute(active_data_query)
        result = socool_cursor.fetchall()
        for site in result:
          #Date math to calculate days_wet
          current_date = date.today()
          days_wet = (current_date - site['deployed'])
          site['days_wet'] = days_wet.days
          site['deployed']  = site['deployed'].strftime('%Y-%m-%d')
          site['date'] = site['date'].strftime('%Y-%m-%d %H:%M')
          site['epoch'] = int(time.mktime(time.strptime(site['date'], '%Y-%m-%d %H:%M')))
          site['time_delta'] = int(time.time() - site['epoch'])

          for key, value in site.iteritems():
            if type(value) is LongType:
              site[key] = int(value)
          active_sites.append(site)
    socool_cursor.close()
    site_cursor.close()
    conn.close()
    return inactive_sites, active_sites

def fetch_glider_data():
 #images for data and kmz links
    data_img = 'chart.png'
    kmz_img = 'kml_icon.jpg'

    #Query DB for expanded headers
    conn = connect_db_socool()
    cursor = conn.cursor()
    headerQuery = 'SELECT expandedName from deploymentExpandedNames'
    try:
        cursor.execute(headerQuery)
    except MySQLdb.Error as e:
        print "Query failed. Error: %s" % e
        sys.exit()
    tableHeaders = []
    for(header) in cursor:
        tableHeaders.append(header[0])

    cursor.close()
    #get data
    data = []
    cursor = conn.cursor()

    #we need to get unexpanded defs and build this string
    dataString = "vehicle,project,deployed,recovered,dayswet,battstart,\
battend,distance,data,kmz,plots"
    dataQuery = "SELECT %s from deployments ORDER BY \
deployed DESC" % dataString
    cursor.execute(dataQuery)
    for row in cursor:
        data.append(row)
    return data, tableHeaders


def get_opd_historical(interval):
    active_sites = []
    conn =  connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #[TO DO] Need to add query to get all 'ACTIVE' serials here
    #and then do a for serial in cursor: query
    if interval != 0:
        active_data_query = "select * from opd_data  where date >  \
NOW() - INTERVAL %d DAY order by date DESC" % interval
    else:
        active_data_query = "select * from opd_data order by date DESC"
    cursor.execute(active_data_query)
    result = cursor.fetchall()
    for record in result:
      for key, value in record.iteritems():
        if type(value) is LongType:
          record[key] = int(value)
      active_sites.append(record)
    cursor.close()
    conn.close()
    return active_sites

def get_people_data():
    staff  = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    staff_query = "select last, first, title, url, image from staff \
ORDER BY LAST ASC"
    cursor.execute(staff_query)
    result = cursor.fetchall()
    for person in result:
      staff.append(person)
    cursor.close()
    conn.close()
    return staff

def get_graph_data(site, param):
    graph_data = []
    conn = connect_db_socool()
    conn2 = connect_db_socool()
    socool_cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor2 = conn2.cursor(MySQLdb.cursors.DictCursor)

    #get deployed date
    deployed_query = "Select deployed, serial from sites where site = '%s'" % site
    socool_cursor.execute(deployed_query)
    for row in socool_cursor:
      deployed = row['deployed']
      serial = row['serial']

    data_query = "select %s, unix_timestamp(date) as epoch from opd_data where \
site = '%s' AND date > '%s' AND serial = '%s' order by epoch asc" % \
(param, site, deployed, serial)

    #get data
    cursor2.execute(data_query)
    result = cursor2.fetchall()
    for record in result:
      #multiply by 1000 to get ms for highcharts
      record['epoch'] = record['epoch']*1000
      row = "[%s, %s]" % (record['epoch'], record[param])
      print row
      graph_data.append(row)

    conn.close()
    conn2.close()
    cursor2.close()
    socool_cursor.close()
    return graph_data

def get_techdocs():
    tech_pubs = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    pub_query = "select title, authors, url, date from techdocs \
ORDER BY date DESC"
    cursor.execute(pub_query)
    result = cursor.fetchall()
    for pub in result:
      tech_pubs.append(pub)
    cursor.close()
    conn.close()
    return tech_pubs

def get_presentations():
    presentations = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    pub_query = "select title, authors, url, event from presentations \
ORDER BY title ASC"
    cursor.execute(pub_query)
    result = cursor.fetchall()
    for pub in result:
      presentations.append(pub)
    cursor.close()
    conn.close()
    return presentations

def get_publications_data():
    publication_types = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    pub_query = "select caption, url, image from publication_types \
ORDER BY caption ASC"
    cursor.execute(pub_query)
    result = cursor.fetchall()
    for pub in result:
      publication_types.append(pub)
    cursor.close()
    conn.close()
    return publication_types

def get_techdocs():
    tech_pubs = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    pub_query = "select title, authors, url, date from techdocs \
ORDER BY date DESC"
    cursor.execute(pub_query)
    result = cursor.fetchall()
    for pub in result:
      tech_pubs.append(pub)
    cursor.close()
    conn.close()
    return tech_pubs

def get_inst_docs():
    inst_docs = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    pub_query = "select instrument, title, url, revdate from inst_docs \
ORDER BY instrument ASC"
    cursor.execute(pub_query)
    result = cursor.fetchall()
    for doc in result:
      inst_docs.append(doc)
    cursor.close()
    conn.close()
    return inst_docs

def get_glider_docs():
    glider_docs = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    pub_query = "select title, url, revdate from glider_docs \
ORDER BY title ASC"
    cursor.execute(pub_query)
    result = cursor.fetchall()
    for doc in result:
      glider_docs.append(doc)
    cursor.close()
    conn.close()
    return glider_docs

def get_sop_docs():
    sop_docs = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    pub_query = "select title, url, revdate from sop_docs \
ORDER BY title ASC"
    cursor.execute(pub_query)
    result = cursor.fetchall()
    for doc in result:
      sop_docs.append(doc)
    cursor.close()
    conn.close()
    return sop_docs



def get_technology_data():
    tech  = []
    conn = connect_db_socool()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #query for inactive sites
    tech_query = "select caption, url, image from technology \
ORDER BY caption ASC"
    cursor.execute(tech_query)
    result = cursor.fetchall()
    for technology in result:
        tech.append(technology)
    return tech

inactive_sites, active_sites = get_opd_data()

