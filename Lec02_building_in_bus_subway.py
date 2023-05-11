import processing
import time

start = time.time()

##작업 순서
# shp 재투영 (버스, 메트로) > 버퍼 생성 (버스, 메트로) > 클립 (버스 버퍼, 메트로 버퍼) > 공간 인덱스 생성 (클립, 건물) > 위치로 추출 (클립, 건물)

## shp paths
busesPath = 'C:/sia_source/Day2/pyQGIS/Lec02_busstop/seoul_bus_stops.shp'
metrosPath = 'C:/sia_source/Day2/pyQGIS/Lec02_subwaystation/seoul_metro.shp'
buildingsPath = 'C:/sia_source/Day2/pyQGIS/Lec02_building/check/check2/F_FAC_BUILDING_11_202304.shp'

##재투영
# 일시 산출물
output_re_bus = 'memory:re_bus'
output_re_metro = 'memory:re_metro'
# 재투영 파라미터
reParams_Buses = {'INPUT' : busesPath, 'TARGET_CRS' : 'EPSG:5186', 'OUTPUT' : output_re_bus}
reParams_Metros = {'INPUT' : metrosPath, 'TARGET_CRS' : 'EPSG:5186', 'OUTPUT' : output_re_metro}
# 재투영 실행
reBuses = processing.run('native:reprojectlayer', reParams_Buses)
reMetros = processing.run('native:reprojectlayer', reParams_Metros)
# 재투영 결과 추가
QgsProject.instance().addMapLayer(reBuses['OUTPUT'])
QgsProject.instance().addMapLayer(reMetros['OUTPUT'])
print('재투영 완료 :', time.time()-start)

##버퍼
# 버퍼 길이
buffer_distance_bus = 200
buffer_distance_metro = 500
# 일시 산출물
output_temp_bus = 'memory:buff_bus'
output_temp_metro = 'memory:buff_metro'
# 버퍼 파라미터
bufferParams_buses = {'INPUT' : reBuses['OUTPUT'], 'DISTANCE' : buffer_distance_bus, 'OUTPUT' : output_temp_bus}
bufferParams_metros = {'INPUT' : reMetros['OUTPUT'], 'DISTANCE' : buffer_distance_metro, 'OUTPUT' : output_temp_metro}
# 버퍼 실행
bufferBus = processing.run('native:buffer', bufferParams_buses)
bufferMetro = processing.run('native:buffer', bufferParams_metros)
# 버퍼 결과 추가
QgsProject.instance().addMapLayer(bufferBus['OUTPUT'])
QgsProject.instance().addMapLayer(bufferMetro['OUTPUT'])
print('버퍼 완료 :', time.time()-start)

##클립
# 일시 산출물
output_temp_clip = 'memory:clipped'
# 클립 파라미터
clipParams = {'INPUT' : bufferBus['OUTPUT'], 'OVERLAY' : bufferMetro['OUTPUT'], 'OUTPUT' : output_temp_clip}
# 클립 실행
clipped = processing.run('native:clip', clipParams)
# 클립 결과 추가
QgsProject.instance().addMapLayer(clipped['OUTPUT'])
print('클립 완료 :', time.time()-start)

##공간 인덱스 생성
# 임시 산출물
output_index_clip = 'memory:clip_indexed'
output_index_build = 'memory:build_indexed'
# 인덱스 생성 파라미터
indexParams_clip = {'INPUT' : clipped['OUTPUT'], 'OUTPUT' : output_index_clip}
indexParams_build = {'INPUT' : buildingsPath, 'OUTPUT' : output_index_build}
# 인덱스 생성 실행
indexClip = processing.run('native:createspatialindex', indexParams_clip)
indexBuild = processing.run('native:createspatialindex', indexParams_build)
print('인덱스 생성 완료 :', time.time()-start)

##위치로 추출
# 0: intersect, 1: 포함(contain), 2: 분절(disjoint), 3: 동등(equal), 4: 접촉(touch), 5: 중첩(overlap), 6: 내부(are within), 7: 공간 교차(cross)
# 임시 산출물
output_temp_ext = 'memory:extracted_intersect'
# 추출 파라미터
extractParams = {'INPUT' : indexBuild['OUTPUT'], 'PREDICATE' : 0, 'INTERSECT' : indexClip['OUTPUT'], 'OUTPUT' : output_temp_ext}
# 추출 실행
extracted = processing.run('native:extractbylocation', extractParams)
# 추출 결과 추가
QgsProject.instance().addMapLayer(extracted['OUTPUT'])
print('추출 완료 :', time.time()-start)