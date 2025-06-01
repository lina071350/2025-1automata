# Strategical Analysis Project
전략적 분석 프로젝트는 오토마타를 활용한 응용사례로 간단한 워게임에 대한 시뮬레이션 분석 환경입니다. 
해당 프로젝트 내에서는 공격(어뢰)와 방어(수상함과 기만기)를 수행하여 공격과 방어에 대한 전략을 개발합니다. 

## 설치 요구사항
```
pip install -r requirements
```

## 프로그램 실행방법
- Windows
```
(venv) C:\repo\strategic_analysis_project\python project\simulator.py
```
- Linux/Mac
```
(venv) ~/ python project/simulator.py
```

## 수정 불가한 파일
 - manuever.py
 - detetor.py
 - self_propelled_decoy.py
 - stationary_decoy.py
 - surfaceship.py
 - torpedo.py
 - tracking_manuever.py
 - mobject 폴더 내 모든 python 파일들

## 가정사항
 - 수상함의 위치와 어뢰의 위치는 변경할 수 없다. 
 - 수상함의 속도와 어뢰의 속도는 변경할 수 없다. 
 - 기만기는 언제든지 발사할 수 있다. 
 - 총 비용 10에서 고정식, 자항식 기만기는 자율적으로 운용할 수 있으며 총 비용 10을 초과할 수 없다. 
  - 단, 고정식 기만기는 비용 1, 자항식 기만기의 비용은 2.5이다. 
  - 예1) 고정식 기만기 10개를 시간차를 두고 운용(총 비용: 10)
  - 예2) 자항식 기만기를 3개 고정식 기만기를 2개 운용(총 비용: 9.5)
 - 동점인 경우(공격과 방어에 모두 성공, 모두 실패 등) 기만기를 적게 사용하는 경우 가산점을 준다. 

## 수정 불가한 파라미터
 - ManueverObject 파라미터
 - DetectorObject 파라미터
 - decoy_deployment_range 파라미터

## pyjevsim
### Introduction
pyjevsim is a DEVS(discrete event system specification) environment that provides journaling functionality.
It provides the ability to snapshot and restore models or simulation engines.
It's compatible with Python versions 3.10+.
   
For more information, see the documentation. : [pyjevsim](https://pyjevsim.readthedocs.io/en/main/)
   
### Installing
You can install pyjevsim via
```
git clone https://github.com/eventsim/pyjevsim
```
   
### Dependencies
The only dependency required by pyjevsim is dill ~= 0.3.6 for model serialization and restoration.  
dill is an essential library for serializing models and simulation states and can be installed via. 
```
pip install dill
```
   
#### Optional Dependencies
pytest is an optional dependency required for running test cases and example executions. 
You can install pyjevsim via
```
pip install pytest
```
   
Additionally, you can install all necessary libraries, including optional dependencies, by running the following command:
```
pip install -r requirements.txt
```

### License   
Author: Changbeom Choi (@cbchoi)   
Copyright (c) 2014-2020 Handong Global University      
Copyright (c) 2021-2024 Hanbat National University    
License: MIT.  The full license text is available at:   
 - https://github.com/eventsim/pyjevsim/blob/main/LICENSE   
