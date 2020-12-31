from flask import Flask, jsonify, request
from Repository import AccountRepo, SubjectRepo
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()

# region BASIC AUTHENTICATION


@auth.verify_password
def is_valid_account(username, input_password):
    print(username + ":" + input_password)
    if username is not None and input_password is not None:
        if AccountRepo.get_account_by(username, input_password) != "":
            return True
    return False


# endregion

# region SUBJECT_API


@app.route("/subject", methods=["GET"])
@auth.login_required
def api_get_all_subject():
    return jsonify(SubjectRepo.get_all_subject())


@app.route('/subject/<int:subject_id>', methods=['GET'])
@auth.login_required
def api_get_by_subject_id(subject_id):
    return jsonify(SubjectRepo.get_by_subject_id(subject_id))


@app.route('/subject/create', methods=['POST'])
@auth.login_required
def api_create_subject():
    subject_info = {
       'name': request.json.get('name'),
       'teacher': request.json.get('teacher'),
       'required': request.json.get('required')
    }
    if SubjectRepo.create_subject(subject_info):
        return jsonify("Created Successfully !!!")
    return jsonify("Created Failed !!!")


@app.route('/subject/update', methods=['PUT'])
@auth.login_required
def api_update_subject():
    subject_info = {
       'id': request.json.get('id'),
       'name': request.json.get('name'),
       'teacher': request.json.get('teacher'),
       'required': request.json.get('required')
    }
    if SubjectRepo.update_subject(subject_info):
        return jsonify("Updated Successfully !!!")
    return jsonify("Updated Failed !!!")


@app.route('/subject/delete', methods=['DELETE'])
@auth.login_required
def api_delete_subject():
    if SubjectRepo.delete_subject(request.json.get('id')):
        return jsonify("Deleted Successfully !!!")
    return jsonify("Deleted Failed !!!")


# endregion


if __name__ == '__main__':
    app.run(debug=True)