import couchdb
from couchdb import Session
from couchdb import design

auth = Session()
auth.name = "admin"
auth.password = "admin"

#server = "http//172.26.130.151:5984/"
local = "http://127.0.0.1:5984/"

#couch = couchdb.Server(server,session=auth)
couch = couchdb.Server(local)

database_name = "aurin_school_db2"
db = couch[database_name]

# school count for each state
map_function_stateSchoolCount = """function(doc){
    emit(doc.properties.state, 1);
}"""

# total enrolments for each state
map_function_stateTtEnrolment = """function(doc){
    if(doc.properties.total_enrolments != null){
        emit(doc.properties.state, doc.properties.total_enrolments); 
    }
}
"""

# school-sector count for each state (Independent, Government, Catholic)
map_function_stateSchoolSector = """function(doc){
    school_sector = ['Independent', 'Government', 'Catholic'];
    if(school_sector.indexOf(doc.properties.school_sector)==0)
        emit(doc.properties.state, [1,0,0]); 
    else if(school_sector.indexOf(doc.properties.school_sector)==1)
        emit(doc.properties.state, [0,1,0]);
    else
        emit(doc.properties.state, [0,0,1]);
}
"""

reduce_function_sum= '_sum'

def create_view(db, design_name, view_name, map_function, reduce_function):
    view = design.ViewDefinition(design_name,view_name,map_function,reduce_function)
    view.sync(db)


create_view(db,'state','schoolCount',map_function_stateSchoolCount,reduce_function_sum)
create_view(db,'state','ttEnrolment',map_function_stateTtEnrolment,reduce_function_sum)
create_view(db, 'state', 'schoolSector', map_function_stateSchoolSector, reduce_function_sum)
