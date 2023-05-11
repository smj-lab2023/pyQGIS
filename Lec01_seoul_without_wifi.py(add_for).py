import processing
import time

start = time.time()

##작업 순서
# shp 재투영 (와이파이) > 버퍼 생성 (디졸브) (와이파이) > 빼기 (서울 경계-와이파이 버퍼)

## shp paths
wifiPath = 'D:/inflearn/00.publicdata/서울시/공공와이파이/seoul_public_WIFI.shp'
seoulguPath = 'D:/inflearn/00.publicdata/서울시/구경계/LARD_ADM_SECT_SGG_11.shp'

## 재투영
# 일시 산출물
output_wifi_re = 'memory:wifi_re'
# 재투영 파라미터
reParams = {'INPUT' : wifiPath, 'TARGET_CRS' : 'EPSG:5186', 'OUTPUT' : output_wifi_re}
# 재투영 실행
reWifi = processing.run('native:reprojectlayer', reParams)
# 재투영 결과 추가
QgsProject.instance().addMapLayer(reWifi['OUTPUT'])
print('재투영 완료 :', time.time()-start)

##버퍼
# 버퍼 길이
buffer_distance = 100
# 일시 산출물
output_wifi_buffer = 'memory:wifi_buffer'
# 버퍼 파라미터
bufferParams = {'INPUT' : reWifi['OUTPUT'], 'DISTANCE' : buffer_distance, 'DISSOLVE' : 1,'OUTPUT' : output_wifi_buffer}
# 버퍼 실행
bufferWifi = processing.run('native:buffer', bufferParams)
# 버퍼 결과 추가
QgsProject.instance().addMapLayer(bufferWifi['OUTPUT'])
print('버퍼 완료 :', time.time()-start)

##공간 인덱스 생성
# 임시 산출물
output_index_wifi = 'memory:wifi_index'
output_index_seoul = 'memory:seoul_index'
# 인덱스 생성 파라미터
indexParams_wifi = {'INPUT' : bufferWifi['OUTPUT'], 'OUTPUT' : output_index_wifi}
indexParams_seoul = {'INPUT' : seoulguPath, 'OUTPUT' : output_index_seoul}
# 인덱스 생성 실행
indexWifi = processing.run('native:createspatialindex', indexParams_wifi)
indexSeoul = processing.run('native:createspatialindex', indexParams_seoul)
print('인덱스 생성 완료 :', time.time()-start)

##빼기
# 임시 산출물
output_seoul_diff_wifi = 'memory:seoul_diff_wifi'
# 빼기 파라미터
diffParams = {'INPUT' : indexSeoul['OUTPUT'], 'OVERLAY' : indexWifi['OUTPUT'],'OUTPUT' : output_seoul_diff_wifi}
# 빼기 실행
seoul_diff_wifi = processing.run('native:difference', diffParams)
# 빼기 결과 추가
QgsProject.instance().addMapLayer(seoul_diff_wifi['OUTPUT'])
print('빼기 완료 :', time.time()-start)
#---------------------------------
import processing
import time

start = time.time()

##sequence of the work
# shp reproject (wifi) > create buffer (dissolve) (wifi) > subtract (seoul border-wifi buffer)

## shp paths
wifiPath = 'D:/inflearn/00.publicdata/Seoul City/public wifi/seoul_public_WIFI.shp'
seoulguPath = 'D:/inflearn/00.publicdata/Seoul city/Gugyeong-gye/LARD_ADM_SECT_SGG_11.shp'

## reproject
# temporary output
output_wifi_re = 'memory:wifi_re'
# reprojection parameters
reParams = {'INPUT' : wifiPath, 'TARGET_CRS' : 'EPSG:5186', 'OUTPUT' : output_wifi_re}
# Run reprojection
reWifi = processing.run('native:reprojectlayer', reParams)
# Add reprojection result
QgsProject.instance().addMapLayer(reWifi['OUTPUT'])
print('Reprojection complete:', time.time()-start)

##create spatial index
# Temporary artifacts
output_index_wifi = 'memory:wifi_index'
output_index_seoul = 'memory:seoul_index'
# index creation parameters
indexParams_wifi = {'INPUT' : reWifi['OUTPUT'], 'OUTPUT' : output_index_wifi}
indexParams_seoul = {'INPUT' : seoulguPath, 'OUTPUT' : output_index_seoul}
# Run index creation
indexWifi = processing.run('native:createspatialindex', indexParams_wifi)
indexSeoul = processing.run('native:createspatialindex', indexParams_seoul)
print('Index created:', time.time()-start)

##iterate over buffer distances
buffer_distances = [100, 200, 300] #example buffer distances to test
for distance in buffer_distances:
    ##buffer
    # temporary output
    output_wifi_buffer = f'memory:wifi_buffer_{distance}'
    # buffer parameter
    bufferParams = {'INPUT' : reWifi['OUTPUT'], 'DISTANCE' : distance, 'DISSOLVE' : 1,'OUTPUT' : output_wifi_buffer}
    # run buffer
    bufferWifi = processing.run('native:buffer', bufferParams)
    # Add buffer result
    QgsProject.instance().addMapLayer(bufferWifi['OUTPUT'])
    print(f'Buffer done for distance {distance}:', time.time()-start)

    ##subtract
    # Temporary artifacts
    output_seoul_diff_wifi = f'memory:seoul_diff_wifi_{distance}'
    # Subtract parameter
    diffParams = {'INPUT' : indexSeoul['OUTPUT'], 'OVERLAY' : bufferWifi['OUTPUT'],'OUTPUT' : output_seoul_diff_wifi}
    # Execute subtraction
    seoul_diff_wifi = processing.run('native:difference', diffParams)
    # Add subtraction result
    QgsProject.instance().addMapLayer(seoul_diff_wifi['OUTPUT'])
    print(f'Subtraction complete for distance {distance}:', time.time()-start)

