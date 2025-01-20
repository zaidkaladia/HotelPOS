from flask import Flask, request, render_template, jsonify
import json
import os
import sqlite3
from flask import redirect

import logging
from datetime import datetime


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


def get_db_connection():
    conn = sqlite3.connect("database.db")
    print("Connected to database successfully")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json  # JSON data sent from frontend

    # Validate received data
    required_fields = [
        "hotelName",
        "address",
        "phone",
        "email",
        "floors",
        "floorDetails",
    ]
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
    return render_template("checkinform.html", hotel_data=data, checkin_data=None)


@app.route("/checkin", methods=["POST"])
def checkin():
    data = load_data()
    try:
        form_data = request.form

        print(form_data)
        # Input validation (example - add more as needed)
        # required_fields = ['primaryGuestName', 'primaryGuestMobileNumber', 'roomNumber', 'checkinDate']
        # for field in required_fields:
        #     if field not in form_data:
        #         return jsonify({"error": f"Missing required field: {field}"}), 400

        with get_db_connection() as conn:
            cursor = conn.cursor()

            insert_query = """
        INSERT INTO HotelManagement (
            primary_person_name, primary_person_gender, primary_person_mobile, alternate_number, 
            primary_person_address, primary_person_nationality, primary_person_id_type, 
            primary_person_id_number, secondary_person_name, secondary_person_gender, 
            secondary_person_id_type, secondary_person_id_number, room_no, check_in, 
            bed_type, room_type, tour_type, company_name, gst, company_address, no_of_adults, no_of_children, no_of_extra_bed, check_in
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """

            cursor.execute(
                insert_query,
                (
                    form_data.get("primaryGuestName"),
                    form_data.get("primaryGuestGender"),
                    form_data.get("primaryGuestMobileNumber"),
                    form_data.get("primaryGuestAlternateNumber") or None,
                    form_data.get("primaryGuestAddress"),
                    form_data.get("primaryGuestNationality"),
                    form_data.get("primaryGuestIdType"),
                    form_data.get("primaryGuestIdNumber"),
                    form_data.get("secondaryGuestName") or None,
                    form_data.get("secondaryGuestGender") or None,
                    form_data.get("secondaryGuestIdType") or None,
                    form_data.get("secondaryGuestIdNumber") or None,
                    form_data.get("roomNumber"),
                    form_data.get("checkinDate"),
                    form_data.get("bedType"),
                    form_data.get("roomType"),
                    form_data.get("tourType"),
                    form_data.get("primaryGuestCompany") or None,
                    form_data.get("primaryGuestCompanyGST") or None,
                    form_data.get("primaryGuestCompanyAddress") or None,
                    form_data.get("adults", 0),
                    form_data.get("children", 0),
                    form_data.get("extraBeds", 0),
                    form_data.get("checkinDate"),
                ),
            )
            # print("hey hey hey",query_res)
            conn.commit()
            response_message = f"CheckedIn Succesfully"
    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        response_message = f"An error occurred: {e}"
    finally:
        conn.close()

    #     return jsonify({"message": "Checked In Successfully"}), 200

    # except sqlite3.Error as e:
    #     logging.error(f"Database error: {e}")
    #     return jsonify({"error": "An error occurred while processing your request"}), 500
    # except Exception as e:
    #     logging.error(f"Unexpected error: {e}")
    #     return jsonify({"error": "An unexpected error occurred"}), 500

    # End Database Uploading---------------------

    # Start Update the json file changing occupied to true ---------------------
    # Load data from the JSON file
    requiredRoomNumber = form_data["roomNumber"].split(" - ")[0]

    data = load_data()
    # print(requiredRoomNumber)
    floorDetails = data["floorDetails"]
    roomFound = False
    for floor in floorDetails:
        if roomFound:
            break
        for room in floorDetails[floor]:
            if room["number"] == requiredRoomNumber:
                room["occupied"] = True
                roomFound = True
                break

    save_data(data)
    # End Update the json file changing occupied to true ---------------------

    return render_template("dashboard.html", hotel_data=data)


@app.route("/checkin-checkout", methods=["POST"])
def checkin_checkout():
    try:
        form_data = request.form

        print(form_data)
        # Input validation (example - add more as needed)
        # required_fields = ['primaryGuestName', 'primaryGuestMobileNumber', 'roomNumber', 'checkinDate']
        # for field in required_fields:
        #     if field not in form_data:
        #         return jsonify({"error": f"Missing required field: {field}"}), 400

        with get_db_connection() as conn:
            cursor = conn.cursor()

            insert_query = """
        INSERT INTO HotelManagement (
            primary_person_name, primary_person_gender, primary_person_mobile, alternate_number, 
            primary_person_address, primary_person_nationality, primary_person_id_type, 
            primary_person_id_number, secondary_person_name, secondary_person_gender, 
            secondary_person_id_type, secondary_person_id_number, room_no, check_in, 
            bed_type, room_type, tour_type, company_name, gst, company_address, no_of_adults, no_of_children, no_of_extra_bed, check_in
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """

            cursor.execute(
                insert_query,
                (
                    form_data.get("primaryGuestName"),
                    form_data.get("primaryGuestGender"),
                    form_data.get("primaryGuestMobileNumber"),
                    form_data.get("primaryGuestAlternateNumber") or None,
                    form_data.get("primaryGuestAddress"),
                    form_data.get("primaryGuestNationality"),
                    form_data.get("primaryGuestIdType"),
                    form_data.get("primaryGuestIdNumber"),
                    form_data.get("secondaryGuestName") or None,
                    form_data.get("secondaryGuestGender") or None,
                    form_data.get("secondaryGuestIdType") or None,
                    form_data.get("secondaryGuestIdNumber") or None,
                    form_data.get("roomNumber"),
                    form_data.get("checkinDate"),
                    form_data.get("bedType"),
                    form_data.get("roomType"),
                    form_data.get("tourType"),
                    form_data.get("primaryGuestCompany") or None,
                    form_data.get("primaryGuestCompanyGST") or None,
                    form_data.get("primaryGuestCompanyAddress") or None,
                    form_data.get("adults", 0),
                    form_data.get("children", 0),
                    form_data.get("extraBeds", 0),
                    form_data.get("checkinDate"),
                ),
            )
            # print("hey hey hey",query_res)
            conn.commit()
            response_message = f"CheckedIn Succesfully"
    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        response_message = f"An error occurred: {e}"
    finally:
        conn.close()

    # Start Update the json file changing occupied to true ---------------------
    # Load data from the JSON file
    requiredRoomNumber = form_data["roomNumber"].split(" - ")[0]

    data = load_data()
    # print(requiredRoomNumber)
    floorDetails = data["floorDetails"]
    roomFound = False
    for floor in floorDetails:
        if roomFound:
            break
        for room in floorDetails[floor]:
            if room["number"] == requiredRoomNumber:
                room["occupied"] = True
                roomFound = True
                break

    save_data(data)
    # End Update the json file changing occupied to true ---------------------

    return redirect("billing")


# when edit button on the dashboard is pressed
@app.route("/checkin-form-edit")
def checkin_edit_form():
    hotelData = load_data()

    room_number = request.args.get("roomNumber")
    room_name = request.args.get("roomName")

    table_room_no = f"{room_number} - {room_name}"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM HotelManagement WHERE invoice_no IS NULL AND room_no = ?"
        cursor.execute(query, (table_room_no,))

        row = cursor.fetchone()

        if row:
            result = dict(row)
            # return jsonify(result), 200
            print(result)
            return render_template(
                "checkinformedit.html", checkin_data=result, hotelData=hotelData
            )
        else:
            return jsonify({"message": "No matching record found"}), 404

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

    # 1. Get room no and name from request
    # 2. create room no matech the database formate roomNo - roomName
    # 3. get the data from dataset as nomno and invoice null
    # 4. send checkin data to checkinform.html
    # 5. use the sent datato reflect on checkin form


@app.route("/checkin-edit", methods=["POST"])
def checkin_edit():
    try:
        form_data = request.form
        print(form_data)

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # First, find the entry to update
            find_query = """
            SELECT id FROM HotelManagement
            WHERE invoice_no IS NULL AND room_no = ?
            """
            cursor.execute(find_query, (form_data.get("roomNumber"),))
            results = cursor.fetchall()

            if len(results) == 1:
                # We found exactly one matching entry
                entry_id = results[0][0]

                update_query = """
                UPDATE HotelManagement
                SET primary_person_name = ?, primary_person_gender = ?, primary_person_mobile = ?, 
                    alternate_number = ?, primary_person_address = ?, primary_person_nationality = ?, 
                    primary_person_id_type = ?, primary_person_id_number = ?, secondary_person_name = ?, 
                    secondary_person_gender = ?, secondary_person_id_type = ?, secondary_person_id_number = ?, 
                    check_in = ?, bed_type = ?, room_type = ?, tour_type = ?, company_name = ?, 
                    gst = ?, company_address = ?, no_of_adults = ?, no_of_children = ?, no_of_extra_bed = ?, check_in = ?
                WHERE id = ?
                """

                cursor.execute(
                    update_query,
                    (
                        form_data.get("primaryGuestName"),
                        form_data.get("primaryGuestGender"),
                        form_data.get("primaryGuestMobileNumber"),
                        form_data.get("primaryGuestAlternateNumber") or None,
                        form_data.get("primaryGuestAddress"),
                        form_data.get("primaryGuestNationality"),
                        form_data.get("primaryGuestIdType"),
                        form_data.get("primaryGuestIdNumber"),
                        form_data.get("secondaryGuestName") or None,
                        form_data.get("secondaryGuestGender") or None,
                        form_data.get("secondaryGuestIdType") or None,
                        form_data.get("secondaryGuestIdNumber") or None,
                        form_data.get("checkinDate"),
                        form_data.get("bedType"),
                        form_data.get("roomType"),
                        form_data.get("tourType"),
                        form_data.get("primaryGuestCompany") or None,
                        form_data.get("primaryGuestCompanyGST") or None,
                        form_data.get("primaryGuestCompanyAddress") or None,
                        form_data.get("adults", 0),
                        form_data.get("children", 0),
                        form_data.get("extraBeds", 0),
                        form_data.get("checkinDate"),
                        entry_id,
                    ),
                )

                conn.commit()
                response_message = "Entry updated successfully"
            elif len(results) > 1:
                response_message = "Multiple entries found for this room number without an invoice. Please provide more information to identify the correct entry."
            else:
                response_message = (
                    "No matching entry found or entry already has an invoice number"
                )

    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        response_message = f"An error occurred: {e}"
    finally:
        conn.close()

    data = load_data()
    return render_template("dashboard.html", hotel_data=data)


@app.route("/checkin-edit-checkout", methods=["POST"])
def checkin_edit_checkout():
    try:
        form_data = request.form
        print(form_data)

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # First, find the entry to update
            find_query = """
            SELECT id FROM HotelManagement
            WHERE invoice_no IS NULL AND room_no = ?
            """
            cursor.execute(find_query, (form_data.get("roomNumber"),))
            results = cursor.fetchall()

            if len(results) == 1:
                # We found exactly one matching entry
                entry_id = results[0][0]

                update_query = """
                UPDATE HotelManagement
                SET primary_person_name = ?, primary_person_gender = ?, primary_person_mobile = ?, 
                    alternate_number = ?, primary_person_address = ?, primary_person_nationality = ?, 
                    primary_person_id_type = ?, primary_person_id_number = ?, secondary_person_name = ?, 
                    secondary_person_gender = ?, secondary_person_id_type = ?, secondary_person_id_number = ?, 
                    check_in = ?, bed_type = ?, room_type = ?, tour_type = ?, company_name = ?, 
                    gst = ?, company_address = ?, no_of_adults = ?, no_of_children = ?, no_of_extra_bed = ?, check_in = ?
                WHERE id = ?
                """

                cursor.execute(
                    update_query,
                    (
                        form_data.get("primaryGuestName"),
                        form_data.get("primaryGuestGender"),
                        form_data.get("primaryGuestMobileNumber"),
                        form_data.get("primaryGuestAlternateNumber") or None,
                        form_data.get("primaryGuestAddress"),
                        form_data.get("primaryGuestNationality"),
                        form_data.get("primaryGuestIdType"),
                        form_data.get("primaryGuestIdNumber"),
                        form_data.get("secondaryGuestName") or None,
                        form_data.get("secondaryGuestGender") or None,
                        form_data.get("secondaryGuestIdType") or None,
                        form_data.get("secondaryGuestIdNumber") or None,
                        form_data.get("checkinDate"),
                        form_data.get("bedType"),
                        form_data.get("roomType"),
                        form_data.get("tourType"),
                        form_data.get("primaryGuestCompany") or None,
                        form_data.get("primaryGuestCompanyGST") or None,
                        form_data.get("primaryGuestCompanyAddress") or None,
                        form_data.get("adults", 0),
                        form_data.get("children", 0),
                        form_data.get("extraBeds", 0),
                        form_data.get("checkinDate"),
                        entry_id,
                    ),
                )

                conn.commit()
                response_message = "Entry updated successfully"
            elif len(results) > 1:
                response_message = "Multiple entries found for this room number without an invoice. Please provide more information to identify the correct entry."
            else:
                response_message = (
                    "No matching entry found or entry already has an invoice number"
                )

    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        response_message = f"An error occurred: {e}"
    finally:
        conn.close()

    data = load_data()
    return render_template("billing.html")


@app.route("/dashboard-billing")
def dashboard_checkout():
    roomNumber = request.args.get("roomNumber")
    try:
        with get_db_connection() as conn:
            print("[INFO] Hello from dashboard-billing")
            cursor = conn.cursor()
            # First, find the entry to update
            find_query = """
            SELECT * FROM HotelManagement
            WHERE invoice_no IS NULL AND room_no = ?
            """
            cursor.execute(find_query, (roomNumber,))
            results = cursor.fetchall()
            matches = len(results)
            record = dict(results[0])
            # print(results)

            now = datetime.now()
            check_out_date_time = now.strftime("%Y-%m-%dT%H:%M")
            if matches == 1:
                entry_id = record["id"]
                update_query = """
                                UPDATE HotelManagement
                                SET check_out = ?
                                WHERE id = ?
                            """
                check_out_date_update_response = cursor.execute(
                    update_query, (check_out_date_time, entry_id)
                )
                print(f"[INFO] response: {check_out_date_update_response}")

                # conn.commit()
                response_message = "Entry updated successfully"
                print(f"[INFO] {response_message}")
            elif matches > 1:
                response_message = f"[INFO] {matches} matches found for room number.: {request.args.get('roomNumber')}"
                print(response_message)
            else:
                response_message = (
                    "No matching entry found or entry already has an invoice number"
                )
            # First, find the entry to update
            find_query = """
            SELECT * FROM HotelManagement
            WHERE invoice_no IS NULL AND room_no = ?
            """
            cursor.execute(find_query, (roomNumber,))
            results = dict(cursor.fetchall()[0])
            print(results)

    except sqlite3.Error as e:
        conn.rollback()
        print(f"[ERROR] Some error occured: {e}")
    finally:
        conn.close()

    data = load_data()
    return render_template("billing.html", hotel_data=data, data=results)


if __name__ == "__main__":
    app.run(debug=True, port=54321)
