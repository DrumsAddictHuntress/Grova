
from datetime import date, datetime
from config import db

class Survey(db.Model):
    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key=True)

    room_number = db.Column(db.String(50), nullable=False)
    batch_number = db.Column(db.String(50), nullable=False)
    filling_date = db.Column(db.Date)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    compost_amount = db.Column(db.Float)
    compost_kg = db.Column(db.Float)
    missing_section = db.Column(db.String(50))
    total_room_m2 = db.Column(db.Float)
    extra_compost = db.Column(db.Float)
    compost_remarks = db.Column(db.Text)
    compost_arrival = db.Column(db.String(50))
    compost_camion_temp = db.Column(db.Float)

    extra_water = db.Column(db.Float)
    compost_height = db.Column(db.Float)
    compost_moist = db.Column(db.Float)
    compost_length = db.Column(db.Float)
    compost_texture = db.Column(db.Float)
    compost_spawn = db.Column(db.Float)

    relative_humidity = db.Column(db.Float)
    casing_water = db.Column(db.Float)
    casing_bbk = db.Column(db.Float)
    casing_peat_55 = db.Column(db.Float)
    casing_peat_110 = db.Column(db.Float)
    casing_peat_135 = db.Column(db.Float)
    casing_sugar_beet_lime = db.Column(db.Float)
    casing_hydrated_lime = db.Column(db.Float)
    casing_limestone_cacho = db.Column(db.Float)

    filled = db.Column(db.String(50))
    arrived = db.Column(db.String(50))
    in_tunnel = db.Column(db.String(50))
    tunnel_number = db.Column(db.String(50))

    spawn_type_rate = db.Column(db.String(100))
    supplement = db.Column(db.String(100))
    supplement_kg = db.Column(db.Float)
    spawning_n = db.Column(db.Float)
    spawning_ash = db.Column(db.Float)
    spawning_wet_weight = db.Column(db.Float)
    spawning_cellulose = db.Column(db.Float)

    shipping_ph = db.Column(db.Float)
    shipping_days = db.Column(db.Float)
    casing_thickness = db.Column(db.Float)
    casing_ph = db.Column(db.Float)
    casing_humidity = db.Column(db.Float)

    notes = db.Column(db.Text)

    is_completed = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    daily_stats = db.relationship("DailyStat", backref="survey", cascade="all, delete-orphan", lazy="dynamic")


class DailyStat(db.Model):
    __tablename__ = "daily_stats"
    id = db.Column(db.Integer, primary_key=True)

    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.id"), nullable=False)
    stat_date = db.Column(db.Date, nullable=False, default=date.today)

    comp_ctrl = db.Column(db.Float)
    comp_temp = db.Column(db.Float)
    comp_max  = db.Column(db.Float)

    air_ctrl = db.Column(db.Float)
    air_meas = db.Column(db.Float)

    co2 = db.Column(db.Float)
    co2_meas = db.Column(db.Float)
    rh_meas = db.Column(db.Float)
    max_val = db.Column(db.Float)
    ab_val = db.Column(db.Float)

    fresh_air = db.Column(db.Float)
    fresh_air_meas = db.Column(db.Float)

    fan = db.Column(db.Float)
    fan_meas = db.Column(db.Float)

    heat = db.Column(db.Float)
    temp = db.Column(db.Float)
    cool_temp = db.Column(db.Float)
    h2o = db.Column(db.Float)
    ref_temp = db.Column(db.Float)

    remarks = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint("survey_id", "stat_date", name="uq_survey_day"),)
