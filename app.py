from flask import Flask
import jaydebeapi
import jpype

app = Flask(__name__)


def get_jdbc_connection():
    if jpype.isJVMStarted() and not jpype.isThreadAttachedToJVM():
        jpype.attachThreadToJVM()
        jpype.java.lang.Thread.currentThread().setContextClassLoader(jpype.java.lang.ClassLoader.getSystemClassLoader())
    connection = jaydebeapi.connect(
        'com.teradata.jdbc.TeraDriver',
        'jdbc:teradata://edw-dev.company.org',
        {'secretNAME': 'admin', 'password': 'admin', 'tmode': 'TERA', 'charset': 'UTF8'},
        '/path/')
    return connection

@app.route('/hello/')
def hello_world():
    print('Init second connection')
    get_jdbc_connection()
    print('Success')
    return 'Hello world!'


if __name__ == '__main__':
    print('Init connection')
    test_connection = get_jdbc_connection()
    test_connection.close()
    print('Init connection closed')
    app.run(host='localhost', port=5000, threaded=True, debug=True)
