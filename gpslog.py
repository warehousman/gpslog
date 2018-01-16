import serial
import pynmea2
from geopy.geocoders import Nominatim
import logging
import time


geolocator = Nominatim()

ser = serial.Serial("/dev/cu.usbserial")
ser.baudrate = 38400

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'mylog.log')


while True:
    if ser.is_open:
        pass
    else:
        ser.open()
    line = ser.readline()
    try:
        if line.startswith('$GPGGA'):
            gpsdata = pynmea2.parse(line)
            if gpsdata.gps_qual > 0:
                print 'Got GPS lock: %s, Quality %s' %(gpsdata, gpsdata.gps_qual)
                try:
                    location = geolocator.reverse("%s, %s" %(gpsdata.latitude, gpsdata.longitude))
                    logging.info(u'%s, %s, Location: %s'%(gpsdata.latitude, gpsdata.longitude, location.address))
                    print u'%s, %s, Location: %s'%(gpsdata.latitude, gpsdata.longitude, location.address)
                    time.sleep(10)
                except:
                    logging.info(u'Failed to get Location, gpsdata %s' %(gpsdata))
                    print 'Failed to get Location, gpsdata %s' %(gpsdata)
            else:
                #logging.error(u'No Signal: Quality: %s, readline: %s' % (gpsdata.gps_qual, line))
                print u'No Signal: Quality: %s, %s' % (gpsdata.gps_qual, line)
        else:
            #logging.info(line)
            print line
    except:
        logging.error('Failed to read serial')
        print 'Failed to read serial'
        ser.close()
        time.sleep(3)
