from flask import Flask, jsonify, request
from Repository import SubjectRepo
app = Flask(__name__)

# region SUBJECT_API


@app.route("/subject", methods=["GET"])
def api_get_all_subject():
    return jsonify(SubjectRepo.get_all_subject())


@app.route('/subject/<int:subject_id>', methods=['GET'])
def api_get_by_subject_id(subject_id):
    return jsonify(SubjectRepo.get_by_subject_id(subject_id))


@app.route('/subject/create', methods=['POST'])
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
def api_delete_subject():
    if SubjectRepo.delete_subject(request.json.get('id')):
        return jsonify("Deleted Successfully !!!")
    return jsonify("Deleted Failed !!!")


# endregion


if __name__ == '__main__':
    app.run(debug=True)