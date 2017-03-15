"Proof connection at SQLAlchemy level, on top of pyodbc."
#!/usr/bin/env python
# Test SQLAlchemy connection. Result is 42.
# Note parameters in connection string, <PARAMETER>.
import urllib
import json
import os
from sqlalchemy import create_engine
from flask import Flask
from flask import request
from flask import make_response
from sqlalchemy import create_engine
# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")
	cur = create_engine('mssql+pyodbc:///?odbc_connect=' +
                    urllib.quote_plus('DRIVER=FreeTDS;SERVER=52.202.54.188;PORT=1433;DATABASE=IRSeForm;UID=IRSUsr_Analytic;PWD=9_8-eF-2@9-Sm-01;TDS_Version=8.0;')
                    )
	cur=con.cursor()
	cur.execute("select * from C_Submissions where ref_no='"zone"'")
	for row in cur:
		speech =  row.PK_C_S_key + "," + row.FK_2290F_key
	cur.close()
	con.close()
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
