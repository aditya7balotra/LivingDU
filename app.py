from flask import Flask , render_template , url_for , make_response , request , redirect , send_file
import json
from io import BytesIO
import pandas as pd

app = Flask(__name__)

#ensuring the file
try:
    with open('data.json' , 'r') as file:
        pass
except:
    with open('data.json' , 'w') as file:
        json.dump([] , file , indent= 4)
        
try:
    with open('downloads.json' , 'r') as file:
        pass
except:
    with open('downloads.json' , 'w') as file:
        json.dump({'name':[] , 'college':[] , 'state':[]} , file , indent= 4)
    
    
@app.route('/')
def index():
    is_cookie = request.cookies.get('entered')
    if is_cookie:
        return render_template('thanq.html')
    else:
        response = make_response(render_template('home.html'))
        # response.set_cookie('entered' , 'yes' , 120)
    
    return response

@app.route('/save' , methods = ['POST' , 'GET'])
def save():
    if request.method == 'POST':
        #lets check the cookie as well
        cookie = request.cookies.get('entered')
        if cookie:
            return redirect(url_for('index'))
        else:
            pass
        
    # Retrieve form data
        clg_name = request.form.get('college')
        area = request.form.get('area')
        room_type = request.form.get('room_type')
        money = request.form.get('money')
        living = request.form.get('living')
        contract = request.form.get('contract')
        security_charge = request.form.get('security_charge')
        transport = request.form.get('transport')
        food = request.form.get('food')
        facilities = request.form.get('facilities')
        gender_specific = request.form.get('gender_specific')
        distance = request.form.get('distance')
        rating = request.form.get('rating')
        mention = request.form.get('mention')
        consent = request.form.get('consent')

    # Process the form data as needed

        
        new_data = {
            'college': clg_name,
            'area': area,
            'room_type': room_type,
            'money_per_month': money,
            'living': living,
            'contract': contract,
            'security_charge': security_charge,
            'transport': transport,
            'food_type': food,
            'facilities': facilities,
            'gender_specific': gender_specific,
            'distance': distance,
            'rating': rating,
            'mention': mention
        }

        
        #fetching pre data
        with open('data.json') as file:
            data = json.load(file)
        
        #row in which the new data is inserting
        data_len = len(data)
        #updating the data
        data.append(new_data)
        
        with open('data.json' , 'w') as file:
            data = json.dump(data , file , indent= 4)
            
        response = make_response(render_template('thanq.html'))
        response.set_cookie('entered' , str(data_len) , 600)
        
        return response
    
    elif request.method == 'GET':
        return render_template('thanq.html')

@app.route('/get')
def get_data():
    #fetching the file data
    with open('data.json') as file:
        data = json.load(file)
        
    return render_template('data.html' , data = data)

@app.route('/download' , methods = ['GET' , 'POST'])
def download():
    if request.method == 'GET':
        return render_template('pre_download.html')
    elif request.method == 'POST':
        name = request.form.get('name').lower()
        college = request.form.get('college').lower()
        area = request.form.get('state').lower()
        
        #saving the download user data
        with open('downloads.json') as file:
            data = json.load(file)
        
        data['name'].append(name)
        data['college'].append(college)
        data['state'].append(area)
        
        with open('downloads.json' , 'w') as file:
            json.dump(data , file , indent= 4)
        
        #loading the asked data
        with open('data.json') as file:
            data = json.load(file)
        # preparing the asked data
        df = pd.DataFrame(data)
        # print(df)
        df.college = df.college.apply(lambda x : x.lower())
        df = df[df['college'] == college]
        df.rename(columns={
            'college': 'College',
            'area': 'Area / Locality',
            'room_type': 'Room Type',
            'money_per_month': 'Monthly Rent (Per Person Share)',
            'living': 'People Sharing the Room',
            'contract': 'Contract Duration',
            'security_charge': 'Security Deposit',
            'transport': 'Nearest Transport (Distance)',
            'food_type': 'Food Means',
            'facilities': 'Facilities Included',
            'gender_specific': 'Room Allowed For',
            'distance': 'Distance to College',
            'rating': 'Overall Rating (Out of 5)',
            'mention': 'Additional Comments'
        }, inplace=True)

        buffer = BytesIO()
        df.to_excel(buffer , index=False)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'{name}_{college}_{area}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
@app.route('/edit')
def edit():
    # print(request.cookies.get('entered'))
    row_num = int(str(request.cookies.get('entered')))
    # fetching the pre details
    with open('data.json') as file:
        data = json.load(file)[row_num]
        
    
    return render_template('edit.html' , data = data)
  
@app.route('/edit_save' , methods = ['POST'])
def edit_home():
    row_num = int(request.cookies.get('entered'))
    #fetching the data
    clg_name = request.form.get('college')
    area = request.form.get('area')
    room_type = request.form.get('room_type')
    money = request.form.get('money')
    living = request.form.get('living')
    contract = request.form.get('contract')
    security_charge = request.form.get('security_charge')
    transport = request.form.get('transport')
    food = request.form.get('food')
    facilities = request.form.get('facilities')
    gender_specific = request.form.get('gender_specific')
    distance = request.form.get('distance')
    rating = request.form.get('rating')
    mention = request.form.get('mention')
    consent = request.form.get('consent')

    # Process the form data as needed

    
    new_data = {
        'college': clg_name,
        'area': area,
        'room_type': room_type,
        'money_per_month': money,
        'living': living,
        'contract': contract,
        'security_charge': security_charge,
        'transport': transport,
        'food_type': food,
        'facilities': facilities,
        'gender_specific': gender_specific,
        'distance': distance,
        'rating': rating,
        'mention': mention
    }
    
    #updating the previous data
    with open('data.json') as file:
        data = json.load(file)
    
    data[row_num] = new_data
    
    with open('data.json' , 'w') as file:
        json.dump(data , file , indent = 4)
        
    return redirect(url_for('index'))
        
    
    
if __name__ == '__main__':
    app.run(
        debug= False
    )
    