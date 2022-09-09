from database.DB import Session


def connect_session_database(func):

    def data_on_func(session_, data):
        
        with Session() as session:
            func(session, data)
    
    return data_on_func


@connect_session_database
def insert_data(session: Session, data):
    session.add(data)
    session.commit()