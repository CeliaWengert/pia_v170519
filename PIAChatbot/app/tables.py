from flask_table import Table, Col
 
class Results(Table):
    id = Col('id', show=True)
    # username = Col("username")
    # email = Col('email')