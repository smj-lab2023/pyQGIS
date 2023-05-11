import processing
import time
import os

start = time.time()

##작업 순서
# 토지피복도 병합> 서울 구별로 레이어 분할 > 공간 인덱스 생성 (토지피복도) > 개별 구로 토지피복도 클립

#seoulLandUseFolder = 'C:/sia_source/Day2/pyQGIS/Let03_landcover'
#print (os.listdir(seoulLandUseFolder))
#print (len(os.listdir(seoulLandUseFolder)))


seoulguFolderPath = 'C:/sia_source/Day2/pyQGIS/Lec00_seoulgu'
seoulguPath = os.path.join(seoulguFolderPath,'LARD_ADM_SECT_SGG_11.shp')
os.makedirs(os.path.join(seoulguFolderPath,'splitted'), exist_ok = 1)
splitSavePath = os.path.join(seoulguFolderPath,'splitted')

seoulLandUseFolder = 'C:/sia_source/Day2/pyQGIS/Let03_landcover'
shps = []
for folder in os.listdir(seoulLandUseFolder):
    if os.path.isdir(os.path.join(seoulLandUseFolder, folder))==1:
        for file in os.listdir(os.path.join(seoulLandUseFolder, folder)):
            if file.endswith('shp'):
                shps.append(os.path.join(seoulLandUseFolder, folder, file))

#print(shps)
#print(len(shps))

## 병합
# 일시 산출물
output_merge_landuse = 'memory:output_merge_landuse'
# 병합 파라미터
mergeParamsLanduse = {'LAYERS' : shps, 'CRS' : 'EPSG:5186', 'OUTPUT' : output_merge_landuse}
# 병합 실행
mergeLanduse = processing.run('native:mergevectorlayers', mergeParamsLanduse)
# 병합 결과 추가
QgsProject.instance().addMapLayer(mergeLanduse['OUTPUT'])
print('병합 완료 :', time.time()-start)

##레이어 분할
# 분할 파라미터
splitParams = {'INPUT' : seoulguPath, 'FIELD' : 'SGG_NM', 'FILE_TYPE' : 1, 'OUTPUT' : splitSavePath}
# 분할 실행
splitSeoul = processing.run('native:splitvectorlayer', splitParams)
# 분할 완료
print('분할 완료 :', time.time()-start)

print(os.listdir(splitSavePath))
print(len(os.listdir(splitSavePath)))

##공간 인덱스 생성
# 임시 산출물
output_index_landuse = 'memory:output_index_landuse'
# 인덱스 생성 파라미터
indexParamsLanduse = {'INPUT' : mergeLanduse['OUTPUT'], 'OUTPUT' : output_index_landuse}
# 인덱스 생성 실행
indexLanduse = processing.run('native:createspatialindex', indexParamsLanduse)
# 인덱스 결과 추가
#QgsProject.instance().addMapLayer(indexLanduse['OUTPUT'])
print('인덱스 생성 완료 :', time.time()-start)

##클립
gu_shps = [gu for gu in os.listdir(splitSavePath) if gu.endswith('shp')]
for gu in gu_shps:
    gu_name = gu.split('.')[0].split('_')[-1]
    overlay = os.path.join(splitSavePath, gu)
    # 일시 산출물
    output_clip_gu = 'memory:' + gu_name
    # 클립 파라미터
    clipParamsGu = {'INPUT' : indexLanduse['OUTPUT'], 'OVERLAY' : overlay,'OUTPUT' : output_clip_gu}
    # 클립 실행
    clipGu = processing.run('native:clip', clipParamsGu)
    # 클립 결과 추가
    QgsProject.instance().addMapLayer(clipGu['OUTPUT'])
print('클립 완료 :', time.time()-start)