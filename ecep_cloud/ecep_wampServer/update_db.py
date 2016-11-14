"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakar,
Praveen Prabhakaran, Tejeshwar Chandra Kamaal

Function to update the database according to the
response received from end node
"""

import threading
import time
from server.ecep_db.controller import *

# maintain all the registered devices
regDevice = {}


# decorator for threads
def threaded(func):
    def func_wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
        return thread

    return func_wrapper


class updateDB(object):
    """
    Contains function to check the heartbeat and update DB.
    """
    
    def addComputeNode(self, data):
        """
        used to add a new entry in db
        """
        if data["command"] == 'create':
            data["status"] = "creating"
            node = Compute_Manager()
            node.add_new_compute_node(**data)
            
    
    def updateComputeNode(self, data):
        """
        Used to update db
        """
        node = Compute_Manager()
        node.update_compute_node(**data)
        
    
    def deviceReg(self, deviceInfo):
        """
        The device registers when there is no previous device
        """
        print 'deviceReg'
        print deviceInfo
        global regDevice
        
        if deviceInfo['deviceId'] in regDevice:
            print ('heartbeat from ' + deviceInfo['deviceId'] + ' received')
        else:
            devManager = Device_Manager()
            devManager.add_new_device_node(args)
            print ('registering a new device: ' + deviceInfo['deviceId'])
            print ('acrhitecture: ' + deviceInfo['arch'] + ', at location: ' + deviceInfo['location'])

        regDevice[deviceInfo['deviceId']] = True

    @threaded
    def checkHeartbeat(self):
        """
        check if the end node is alive
        """
        global regDevice
        while True:
            print regDevice
            for device in regDevice:
                if regDevice[device] == False:
                    print 'no heartbeat'
                    # remove the entry
                    regDevice.pop(device, None)
                    
                else:
                    print device + ' is alive'
                    regDevice[device] = False
            time.sleep(600)
            
            
    def updateContainerStatus(self, statusList):
        """
        Periodic update of status of all containers
        """
        keyList = ('containerName', 'status')
        
        try:
            for entries in statusList:
                data = dict((key, entries[key]) for key in keyList)
                data['username'] = entries['containerName'].split('_')[0]
                data['containerName'] = entries['containerName'].split('_')[1]
                print data
                self.updateComputeNode(data)
        except Exception as e:
            print 'Could not update the node with periodic status, error: ' + e
            
    def updateDeviceResponse(self, response):
        """
        update the response received from end node
        """
        keyList = ('containerName', 'status', 'command')
        
        try:
            data = dict((key, response[key]) for key in keyList)
            data['username'] = response['containerName'].split('_')[0]
            data['containerName'] = response['containerName'].split('_')[1]

            if data['command'] == 'create':
                data['container_id'] = response['ID']

            self.updateComputeNode(data)
            
            #TODO: complete for remove
            
        except Exception as e:
            print 'Could not update device response, error: ' + e
                
        


if __name__ == '__main__':
    trial = updateDB()
    handle = trial.checkHeartbeat()
    while True:
        time.sleep(1)
    #	print 'abhi'
    handle.join()
