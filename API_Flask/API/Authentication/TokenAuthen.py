# g variable:
#  => stands for “global”
#  => the stored data is global
#  => lost after the request ends
#  => NOT an appropriate place to store data between requests.
#     Use the "session" or a database to store data across requests.
from flask import Flask, jsonify, request, g
from API_Flask.Repository import *
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TMA Company'
app.config['TOKEN_TIME_LIFE'] = 120 # second
auth = HTTPBasicAuth()

# region TOKEN AUTHENTICATION


@auth.verify_password
def is_valid_account(username, input_password):
    print("=====> Username: " + username)
    print("=====> Password: " + input_password)
    if username is not None and input_password is not None:
        g.account_id = AccountRepo.get_account_by(username, input_password)
        if g.account_id != "":
            return True
    return False


@app.route("/token", methods=["GET"])
@auth.login_required
def generate_auth_token():
    token = AccountRepo.generate_auth_token(g.account_id, app.config['TOKEN_TIME_LIFE'], app.config['SECRET_KEY'])
    return jsonify({'token': token, 'duration': app.config['TOKEN_TIME_LIFE']})


def is_valid_token(headers):
    if "Authorization" in headers:
        token = headers['Authorization']
        print("=====> Token: " + token)
        if AccountRepo.verify_auth_token(token, app.config['SECRET_KEY']) != "":
            print("=====> Token is valid")
            return True
    return False


# endregion

# region SUBJECT_API


@app.route("/subject", methods=["GET"])
def api_get_all_subject():
    if is_valid_token(request.headers):
        return jsonify(SubjectRepo.get_all_subject())
    return jsonify('Your token has problem')


@app.route('/subject/<int:subject_id>', methods=['GET'])
def api_get_by_subject_id(subject_id):
    if is_valid_token(request.headers):
        return jsonify(SubjectRepo.get_by_subject_id)
    return jsonify('Your token has problem')


@app.route('/subject/create', methods=['POST'])
def api_create_subject():
    if is_valid_token(request.headers):
        subject_info = {
            'name': request.json.get('name'),
            'teacher': request.json.get('teacher'),
            'required': request.json.get('required')
        }
        if SubjectRepo.create_subject(subject_info):
            return jsonify("Created Successfully !!!")
        return jsonify("Created Failed !!!")
    return jsonify('Your token has problem')


@app.route('/subject/update', methods=['PUT'])
def api_update_subject():
    if is_valid_token(request.headers):
        subject_info = {
            'id': request.json.get('id'),
            'name': request.json.get('name'),
            'teacher': request.json.get('teacher'),
            'required': request.json.get('required')
        }
        if SubjectRepo.update_subject(subject_info):
            return jsonify("Updated Successfully !!!")
        return jsonify("Updated Failed !!!")
    return jsonify('Your token has problem')


@app.route('/subject/delete', methods=['DELETE'])
def api_delete_subject():
    if is_valid_token(request.headers):
        if SubjectRepo.delete_subject(request.json.get('id')):
            return jsonify("Deleted Successfully !!!")
        return jsonify("Deleted Failed !!!")
    return jsonify('Your token has problem')


# endregion


if __name__ == '__main__':
    app.run(debug=True)