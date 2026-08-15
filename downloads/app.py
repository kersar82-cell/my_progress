import requests
from io import BytesIO
from flask import Flask, jsonify, request, send_file
app = Flask(__name__)
SUPPORTED_REGIONS={"IND","BR","US","SAC","NA","SG","RU","ID","TW","VN","TH","ME","PK","CIS","BD","EUROPE"}
def safe_get_url(url):
    response=requests.get(url)
    response.raise_for_status()
    return response
def fetch_player_data_by_uid_or_name(search_parameter):
    url=f"https://info.strikerxyash.online/player-info?uid={search_parameter}" if search_parameter.isdigit() else f"https://info.strikerxyash.online/player-info?name={search_parameter}"
    response=requests.get(url)
    if response.status_code!=200:
        return None
    data=response.json()
    basic_info=data.get("basicInfo")
    if not basic_info:
        return None
    return (basic_info.get("accountId"),basic_info.get("nickname"),basic_info.get("region","Not Choosen"),data)
def fetch_level_data_by_uid_or_name(search_parameter):
    if search_parameter.isdigit():
        url=f"https://info.strikerxyash.online/level?uid={search_parameter}"
    else:
        url=f"https://info.strikerxyash.online/level?name={search_parameter}"
    response=requests.get(url)
    if response.status_code!=200:
        return None
    data=response.json()
    return (data.get("accountId"),data.get("name"),data.get("region","Not Choosen"),data)
def fetch_level_target_data_by_uid_or_name(search_parameter,target_level):
    if search_parameter.isdigit():
        url=f"https://info.strikerxyash.online/level?uid={search_parameter}&target-level={target_level}"
    else:
        url=f"https://info.strikerxyash.online/level?name={search_parameter}&target-level={target_level}"
    response=requests.get(url)
    if response.status_code!=200:
        return None
    data=response.json()
    return (data.get("accountId"),data.get("name"),data.get("region","Not Choosen"),data)
def fetch_outfit_image(avatar_id,clothes,weapon):
    url=f"https://image.strikerxyash.online/outfit-image?avatar_id={avatar_id}&clothes={clothes}&weapon={weapon}"
    response=safe_get_url(url)
    return response.content
@app.route('/player-info',methods=['GET'])
def get_player_info():
    uid=request.args.get('uid')
    name=request.args.get('name')
    search_param=uid if uid else name
    if not search_param:
        return jsonify({"error":"Missing uid or name parameter"}),400
    result=fetch_player_data_by_uid_or_name(search_param)
    if not result:
        return jsonify({"error":"Player not found"}),404
    account_id,nickname,region,data=result
    return jsonify({"uid":account_id,"name":nickname,"region":region,"data":data})
@app.route('/region',methods=['GET'])
def get_region():
    uid=request.args.get('uid')
    name=request.args.get('name')
    search_param=uid if uid else name
    if not search_param:
        return jsonify({"error":"Missing uid or name parameter"}),400
    url=f"https://info.strikerxyash.online/region?uid={search_param}" if search_param.isdigit() else f"https://info.strikerxyash.online/region?name={search_param}"
    response=requests.get(url)
    if response.status_code!=200:
        return jsonify({"error":"Player not found"}),404
    data=response.json()
    return jsonify(data)
@app.route('/level',methods=['GET'])
def get_level():
    uid=request.args.get('uid')
    name=request.args.get('name')
    search_param=uid if uid else name
    if not search_param:
        return jsonify({"error":"Missing uid or name parameter"}),400
    result=fetch_level_data_by_uid_or_name(search_param)
    if not result:
        return jsonify({"error":"Player not found"}),404
    account_id,player_name,region,data=result
    return jsonify({"uid":account_id,"name":player_name,"region":region,"data":data})
@app.route('/level-target',methods=['GET'])
def get_level_target():
    uid=request.args.get('uid')
    name=request.args.get('name')
    target_level=request.args.get('target-level')
    if not target_level:
        return jsonify({"error":"Missing target-level parameter"}),400
    search_param=uid if uid else name
    if not search_param:
        return jsonify({"error":"Missing uid or name parameter"}),400
    result=fetch_level_target_data_by_uid_or_name(search_param,target_level)
    if not result:
        return jsonify({"error":"Player not found"}),404
    account_id,player_name,region,data=result
    return jsonify({"uid":account_id,"name":player_name,"region":region,"data":data})
@app.route('/bancheck',methods=['GET'])
def get_bancheck():
    uid=request.args.get('uid')
    name=request.args.get('name')
    search_param=uid if uid else name
    if not search_param:
        return jsonify({"error":"Missing uid or name parameter"}),400
    url=f"https://info.strikerxyash.online/bancheck?uid={search_param}" if search_param.isdigit() else f"https://info.strikerxyash.online/bancheck?name={search_param}"
    response=requests.get(url)
    if response.status_code!=200:
        return jsonify({"error":"Player not found"}),404
    data=response.json()
    return jsonify(data)
@app.route('/wishlist',methods=['GET'])
def get_wishlist():
    uid=request.args.get('uid')
    name=request.args.get('name')
    search_param=uid if uid else name
    if not search_param:
        return jsonify({"error":"Missing uid or name parameter"}),400
    url=f"https://info.strikerxyash.online/wishlist?uid={search_param}" if search_param.isdigit() else f"https://info.strikerxyash.online/wishlist?name={search_param}"
    response=requests.get(url)
    if response.status_code!=200:
        return jsonify({"error":"Player not found"}),404
    data=response.json()
    return jsonify(data)
@app.route('/leader-info',methods=['GET'])
def get_leader_info():
    uid=request.args.get('uid')
    name=request.args.get('name')
    search_param=uid if uid else name
    if not search_param:
        return jsonify({"error":"Missing uid or name parameter"}),400
    result=fetch_player_data_by_uid_or_name(search_param)
    if result is None:
        return jsonify({"error":"Player not found"}),404
    account_id,player_name,region,data=result
    captain_information=data.get("captainBasicInfo",{})
    if not captain_information.get("accountId"):
        return jsonify({"error":"Leader not found"}),404
    leader_uid=captain_information.get("accountId")
    url=f"https://info.strikerxyash.online/player-info?uid={leader_uid}"
    response=requests.get(url)
    if response.status_code!=200:
        return jsonify({"error":"Leader data not found"}),404
    leader_data=response.json()
    return jsonify(leader_data)
@app.route('/events',methods=['GET'])
def get_events():
    region=request.args.get('region')
    if not region:
        return jsonify({"error":"Missing region parameter"}),400
    if region not in SUPPORTED_REGIONS:
        return jsonify({"error":"Unsupported region"}),400
    url=f"https://info.strikerxyash.online/events?region={region}"
    response=requests.get(url)
    if response.status_code!=200:
        return jsonify({"error":"Events not found"}),404
    data=response.json()
    return jsonify(data)
@app.route('/map-info',methods=['GET'])
def get_map_info():
    map_code=request.args.get('map_code')
    if not map_code:
        return jsonify({"error":"Missing map_code parameter"}),400
    url=f"https://info.strikerxyash.online/map-info?map_code={map_code}"
    response=requests.get(url)
    if response.status_code!=200:
        return jsonify({"error":"Map not found"}),404
    data=response.json()
    return jsonify(data)
@app.route('/outfit-image',methods=['GET'])
def get_outfit_image():
    avatar_id=request.args.get('avatar_id')
    clothes=request.args.get('clothes','')
    weapon=request.args.get('weapon','')
    if not avatar_id:
        return jsonify({"error":"Missing avatar_id parameter"}),400
    outfit_bytes=fetch_outfit_image(avatar_id,clothes,weapon)
    return send_file(BytesIO(outfit_bytes),mimetype='image/png')
if __name__=='__main__':
    app.run(debug=True,port=5000)