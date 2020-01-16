from flask import abort, make_response, Flask, jsonify
import platform,socket,re,uuid,json,psutil
import RPi.GPIO as GPIO
from time import sleep

app = Flask(__name__)

def getSystemInfo():
    try:
            info={}
            info['platform']=platform.system()
            info['platform-release']=platform.release()
            info['platform-version']=platform.version()
            info['architecture']=platform.machine()
            info['hostname']=socket.gethostname()
            info['ip-address']=socket.gethostbyname(socket.gethostname())
            info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info['processor']=platform.processor()
            info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
            return json.dumps(info)
    except Exception as e:
        logging.exception(e)

@app.route('/home/api/v1.0/raspberry-pi/info', methods=['GET'])
def get_info():
    return getSystemInfo()

@app.route('/home/api/v1.0/raspberry-pi/light-on', method=['GET'])
def light_on():
    GPIO.output(8, GPIO.HIGH)
    return "Light On"

@app.route('/home/api/v1.0/raspberry-pi/light-off', method=['GET'])
def light_off():
    GPIO.output(8, GPIO.Low)
    return "Light Off"

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8,GPIO, initial=GPIO.LOW)
    app.run(debug=True)


