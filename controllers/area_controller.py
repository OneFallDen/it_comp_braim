from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Union
import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString

from sql import models
from models import schemas
from controllers.validation_controller import valid_string, valid_location, valid_int
from sql.crud import get_area_by_name, get_all_areas, get_area_points, area_add, area_get, area_delete, area_update


def add_new_area(area: schemas.AreaToAdd, db: Session):
    points = []
    valid_string(area.name)
    if not area.areaPoints:
        raise HTTPException(status_code=400)
    # areaPoints содержит меньше трех точек
    if len(area.areaPoints) < 3:
        raise HTTPException(status_code=400)
    long = area.areaPoints[0]['longitude']
    long_count = 0
    lati = area.areaPoints[0]['latitude']
    lati_count = 0
    for ap in area.areaPoints:
        if not ap:
            raise HTTPException(status_code=400)
        if ap['longitude'] == long:
            long_count += 1
        if ap['latitude'] == lati:
            lati_count += 1
        valid_location(ap['latitude'], ap['longitude'])
        points.append((ap['longitude'], ap['latitude']))
    # Новая зона имеет дубликаты точек
    sets = []
    for a in area.areaPoints:
        sets.append((a['latitude'], a['longitude']))
    setarr = set(sets)
    if not len(sets) == len(setarr):
        raise HTTPException(status_code=409)
    # Все точки лежат на одной прямой
    if len(area.areaPoints) == long_count:
        raise HTTPException(status_code=400)
    if len(area.areaPoints) == lati_count:
        raise HTTPException(status_code=400)
    s = gpd.GeoSeries(Polygon(points))
    # Границы новой зоны пересекаются между собой
    for i in range(len(points)):
        if i == (len(points) - 1):
            points2 = [points[i], points[0]]
        else:
            points2 = [points[i], points[i + 1]]
        l = LineString(points2)
        f = s.crosses(l)
        try:
            if f.bool():
                raise HTTPException(status_code=400)
        except:
            if bool(f):
                raise HTTPException(status_code=400)
    d = 0
    exists_points = []
    try:
        areas = get_all_areas(db)
        d = 1
    except:
        pass
    if d > 0:
        for a in areas:
            exists_area_points = get_area_points(a.id, db)
            for eap in exists_area_points:
                exists_points.append((eap.longitude, eap.latitude))
            s1 = Polygon(exists_points)
            s2 = Polygon(points)
            # Зона, состоящая из таких точек, уже существует.
            if len(exists_points) == len(points):
                a_points = set(points)
                b_points = set(exists_points)
                if a_points == b_points:
                    raise HTTPException(status_code=409)
            # Граница новой зоны находятся внутри границ существующей зоны
            if s1.covers(s2):
                raise HTTPException(status_code=400)
            # Границы существующей зоны находятся внутри границ новой зоны
            if s2.covers(s1):
                raise HTTPException(status_code=400)
            # Границы новой зоны пересекают границы уже существующей зоны
            for i in range(len(points)):
                if i == (len(points) - 1):
                    points2 = [points[i], points[0]]
                else:
                    points2 = [points[i], points[i + 1]]
                l = LineString(points2)
                f = s1.crosses(l)
                try:
                    if f.bool():
                        raise HTTPException(status_code=400)
                except:
                    if bool(f):
                        raise HTTPException(status_code=400)
            exists_points.clear()
    # Зона с таким name уже существует
    x = 0
    try:
        get_area_by_name(area.name, db)
        x = 1
    except:
        pass
    if x > 0:
        raise HTTPException(status_code=409)
    return area_add(area, db)


def update_area_by_id(areaId: int, area: schemas.AreaToAdd, db: Session):
    points = []
    valid_string(area.name)
    if not area.areaPoints:
        raise HTTPException(status_code=400)
    # areaPoints содержит меньше трех точек
    if len(area.areaPoints) < 3:
        raise HTTPException(status_code=400)
    long = area.areaPoints[0]['longitude']
    long_count = 0
    lati = area.areaPoints[0]['latitude']
    lati_count = 0
    for ap in area.areaPoints:
        if not ap:
            raise HTTPException(status_code=400)
        if ap['longitude'] == long:
            long_count += 1
        if ap['latitude'] == lati:
            lati_count += 1
        valid_location(ap['latitude'], ap['longitude'])
        points.append((ap['longitude'], ap['latitude']))
    # Новая зона имеет дубликаты точек
    sets = []
    for a in area.areaPoints:
        sets.append((a['latitude'], a['longitude']))
    setarr = set(sets)
    if not len(sets) == len(setarr):
        raise HTTPException(status_code=409)
    # Все точки лежат на одной прямой
    if len(area.areaPoints) == long_count:
        raise HTTPException(status_code=400)
    if len(area.areaPoints) == lati_count:
        raise HTTPException(status_code=400)
    s = gpd.GeoSeries(Polygon(points))
    # Границы новой зоны пересекаются между собой
    for i in range(len(points)):
        if i == (len(points) - 1):
            points2 = [points[i], points[0]]
        else:
            points2 = [points[i], points[i + 1]]
        l = LineString(points2)
        f = s.crosses(l)
        try:
            if f.bool():
                raise HTTPException(status_code=400)
        except:
            if bool(f):
                raise HTTPException(status_code=400)
    d = 0
    exists_points = []
    try:
        areas = get_all_areas(db)
        d = 1
    except:
        pass
    if d > 0:
        for a in areas:
            exists_area_points = get_area_points(a.id, db)
            for eap in exists_area_points:
                exists_points.append((eap.longitude, eap.latitude))
            s1 = Polygon(exists_points)
            s2 = Polygon(points)
            # Зона, состоящая из таких точек, уже существует.
            if len(exists_points) == len(points):
                a_points = set(points)
                b_points = set(exists_points)
                if a_points == b_points:
                    raise HTTPException(status_code=409)
            # Граница новой зоны находятся внутри границ существующей зоны
            if s1.covers(s2):
                raise HTTPException(status_code=400)
            # Границы существующей зоны находятся внутри границ новой зоны
            if s2.covers(s1):
                raise HTTPException(status_code=400)
            # Границы новой зоны пересекают границы уже существующей зоны
            for i in range(len(points)):
                if i == (len(points) - 1):
                    points2 = [points[i], points[0]]
                else:
                    points2 = [points[i], points[i + 1]]
                l = LineString(points2)
                f = s1.crosses(l)
                try:
                    if f.bool():
                        raise HTTPException(status_code=400)
                except:
                    if bool(f):
                        raise HTTPException(status_code=400)
            exists_points.clear()
    # Зона с таким name уже существует
    x = 0
    try:
        get_area_by_name(area.name, db)
        x = 1
    except:
        pass
    if x > 0:
        raise HTTPException(status_code=409)
    return area_update(areaId, area, db)


def get_area_by_id(areaId: int, db: Session):
    valid_int(areaId)
    try:
        return area_get(areaId, db)
    except:
        raise HTTPException(status_code=404)


def delete_area_by_id(areaId: int, db: Session):
    valid_int(areaId)
    try:
        area_delete(areaId, db)
    except:
        raise HTTPException(status_code=404)
