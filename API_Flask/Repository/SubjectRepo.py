from Database.DB import session, Subject


def get_all_subject():
    all_subjects = session.query(Subject).all()
    json_list = []
    if len(all_subjects) > 0:
        for subject in all_subjects:
            json_list.append(subject.json_format())
    return json_list


def get_by_subject_id(subject_id):
    subject = session.query(Subject).get(subject_id)
    if subject is None:
        return {}
    return subject.json_format()


def create_subject(info):
    try:
        new_subject = Subject(
            name=info["name"],
            teacher=info["teacher"],
            required=info["required"]
        )
        # create
        session.add(new_subject)
        session.commit()
        return True
    except Exception as e:
        print("Error! ", e)
    return False


def update_subject(info):
    try:
        editing_subject = session.query(Subject).filter(Subject.id == info["id"]).first()
        if editing_subject is not None:
            if info["name"]:
                editing_subject.name = info["name"]
            if info["teacher"]:
                editing_subject.teacher = info["teacher"]
            if info["required"] is True or info["required"] is False:
                editing_subject.required = info["required"]
            # update
            session.commit()
            return True
    except Exception as e:
        print("Error! ", e)
    return False


def delete_subject(subject_id):
    try:
        subject = session.query(Subject).filter(Subject.id == subject_id).first()
        if subject is not None:
            # delete
            session.delete(subject)
            session.commit()
            return True
    except Exception as e:
        print("Error! ", e)
    return False

