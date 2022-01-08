import json
from os import name
import wmi
import psutil 
from logging import shutdown
from lcu_driver import Connector


connector = Connector()

# Check if the game is running
def CheckProcess():
    f = wmi.WMI()
    # Printing the header for the later columns
    # print("pid   Process name")
    onClient = False
    # Iterating through all the running processes
    for process in f.Win32_Process():
        if "LeagueClient.exe" in process.Name:
            onClient = True
        # if "Garena.exe" in process.Name:
        #     print(f"{process.ProcessId:<10} {process.Name} {process.Description}")
    # for proc in psutil.process_iter():
    #     for conns in proc.connections(kind='inet'):
    #         if conns.laddr.port == 8080:
    #             print(conns)
    if onClient: 
        return True
    return None
    # process = psutil.pids()
    # for pid in process:
    #     if psutil.Process(pid).name() == 'LeagueClient.exe':
    #         return pid
    #     if psutil.Process(pid).name() == 'garena.exe':
    #         print("Garena"+pid)
    #         return pid
    #     if pid == 476:
    #         print("hi")
    # else:
    #     return None

##### get all friends #######
async def getFriends(connection):
    response = await (await connection.request('get', '/lol-chat/v1/friends')).json()
    print(json.dumps(response, indent=4))


##### check Wishsky is Online #######
async def checkWisOnline(connection):
    response = await (await connection.request('get', '/lol-chat/v1/friends')).json()
    # print(json.dumps(response, indent=4, ensure_ascii=False))
    output_dict = [x for x in response if x['name'] == 'WhiskyOnRock']
    # away/offline/dnd/chat
    # Transform python object back into json
    output_json = json.dumps(output_dict[0])
    print(output_json)

# ##### check Wishsky is Online #######
# async def check(connection, s_name):
#     params = {
#         "name":s_name
#     }
#     response = await (await connection.request('get', '/lol-summoner/v1/status', params=params)).json()
#     print(json.dumps(response, indent=4, ensure_ascii=False))
#     # output_dict = [x for x in response if x['name'] == 'WhiskyOnRock']
#     # # away/offline/dnd/chat
#     # # Transform python object back into json
#     # output_json = json.dumps(output_dict[0])
#     # print(output_json)

@connector.ready
async def connect(connection):
    # print('LCU API is ready to be used.')
    # summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    # summonerData = await summoner.json()
    # print(json.dumps(summonerData, indent=4))
    await checkWisOnline(connection)

# @connector.ws.register('/lol-summoner/v1/current-summoner', event_types=('UPDATE',))
# async def icon_changed(connection, event):
#     print(f'The summoner {event.data["displayName"]} was updated.')

@connector.close
async def disconnect(connection):
    # print('The client was closed')
    await connector.stop()



if __name__ == '__main__':
    # test1.py executed as script
    # do something
    if CheckProcess() == None:
        # print('無法讀取遊戲數據\n需要先啟動客戶端，再運行此程序。')
        print("Client not open\n無法讀取遊戲數據，需要先啟動客戶端，再運行此程序。")
    connector.start()