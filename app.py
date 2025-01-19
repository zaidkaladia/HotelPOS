from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)

# Path to JSON file
DATA_FILE = "hotel_data.json"

# Load existing data or initialize empty data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json  # JSON data sent from frontend

    # Validate received data
    required_fields = ["hotelName", "address", "phone", "email", "floors", "floorDetails"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Save data to JSON file
    try:
        save_data(data)
        return jsonify({"message": "Data saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/dashboard")
def dashboard():
    # Load data from the JSON file
    data = load_data()
    return render_template("dashboard.html", hotel_data=data)

@app.route("/checkin-form")
def checkinForm():
    # Load data from the JSON file
    data = load_data()
    return render_template("checkinform.html", hotel_data=data)

@app.route("/checkin", methods=['POST', 'OPTIONS'])
def checkin():
    data = load_data()
    formData = request.form
    print(formData)
    # Load data from the JSON file
    # data = load_data()
    # requiredRoomNumber = request.get_json('roomNumber')['roomNumber']
    # print(requiredRoomNumber)
    # floorDetails = data['floorDetails']

    # roomFound = False
    # for floor in floorDetails:
    #     if roomFound:
    #         break
    #     for room in floorDetails[floor]:
    #         if room['number'] == requiredRoomNumber:
    #             room['occupied'] = True
    #             roomFound = True
    #             break

    # save_data(data)
    # print(data['floorDetails'])
    # print("hello from after save data")

    # return jsonify({
    #     'status': 200,
    #     'message': 'Occupancy detail updated successfully.'
    # })
    # return render_template("dashboard.html", hotel_data=data)
    return render_template("checkinform.html", hotel_data=data)


@app.route("/occupancy", methods=['POST'])
def occupancy():
    # Load data from the JSON file
    data = load_data()
    requiredRoomNumber = request.get_json('roomNumber')['roomNumber']
    print(requiredRoomNumber)
    floorDetails = data['floorDetails']

    roomFound = False
    for floor in floorDetails:
        if roomFound:
            break
        for room in floorDetails[floor]:
            if room['number'] == requiredRoomNumber:
                room['occupied'] = True
                roomFound = True
                break

    save_data(data)
    # print(data['floorDetails'])
    # print("hello from after save data")

    return jsonify({
        'status': 200,
        'message': 'Occupancy detail updated successfully.'
    })

if __name__ == "__main__":
    app.run(debug=True)
