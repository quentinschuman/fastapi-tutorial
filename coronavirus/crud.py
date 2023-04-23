#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from sqlalchemy.orm import Session

from coronavirus import models, schemas


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.province == name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CreateCity):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    if city:
        return db.query(models.Data).filter(models.Data.city.has(province=city))  # 外键关联查询，这里不是像Django ORM那样Data.city.province
    return db.query(models.Data).offset(skip).limit(limit).all()


def get_data_by_country(db: Session, country: str = None):
    data = db.query(models.City).filter(models.City.country == country).all()
    print("get_data_by_country data size:" + str(len(data)))
    return data


def get_data_by_country_code(db: Session, country_code: str = None):
    data = db.query(models.City).filter(models.City.country_code == country_code).all()
    print("get_data_by_country_code data size:" + str(len(data)))
    return data


def get_data_by_city_id(db: Session, id: str):
    data = db.query(models.City).filter(models.City.id == id).first()
    return data


def get_log_by_id(db: Session, id: int):
    data = db.query(models.Log).filter(models.Log.id == id).first()
    return data


def get_log_by_file_name(db: Session, file_name: str):
    data = db.query(models.Log).filter(models.Log.file_name == file_name).all()
    return data


def get_log_by_method_name(db: Session, method_name: str):
    data = db.query(models.Log).filter(models.Log.method_name == method_name).all()
    return data


def create_city_data(db: Session, data: schemas.CreateData, city_id: int):
    db_data = models.Data(**data.dict(), city_id=city_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_log(db: Session, file_name: str, method_name: str):
    db_data = models.Log(file_name=file_name, method_name=method_name)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data