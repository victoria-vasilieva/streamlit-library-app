from sqlalchemy import create_engine

schema = "lianes_library"
engine = create_engine(f"mysql+pymysql://root:12345678@127.0.0.1:3306/{schema}")
