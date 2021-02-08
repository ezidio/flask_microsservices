from model import db

class Consulta(db.Model):
    __tablename__ = 'consulta_medica_consulta'
    id = db.Column(
        db.String(64),
        primary_key=True
    )
    start_date = db.Column(
        db.DateTime(), 
        nullable=False
    )
    end_date = db.Column(
        db.DateTime()
    )
    physician_id = db.Column(
        db.String(64), 
        nullable=False
    )
    patient_id = db.Column(
        db.String(64), 
        nullable=False
    )
    price = db.Column(
        db.Numeric(17, 4), 
        nullable=False
    )

def persist(data):
    consulta = Consulta(
        id = data['id'],
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d %H:%M:%S'),
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d %H:%M:%S'),
        physician_id = data['physician_id'],
        patient_id = data['patient_id'],
        price = data['price']
    )
    db.session.add(consulta)
    db.session.commit()
    return consulta

def load_all():
    return Consulta.query.all()