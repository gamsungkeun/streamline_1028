제9강_미션 수행형 중간고사 (Open Book Mission) - 2026.10.28

학번 :
이름 :

[배포 주소]
- GitHub Repository : https://github.com/<GitHub아이디>/<저장소이름>
- Streamlit 앱 주소  : https://<앱이름>.streamlit.app

[추가한 메뉴]
- 블록리게임   : https://blockly.games/?lang=ko  (iframe, app.py)
- 테트리스게임 : https://play.tetris.com/        (iframe, app.py)

[제출 파일]
- app.py, app_bak.py, database.py, mycom.db, mycom.sql, requirements.txt, README.md, readme.txt
- capture_blockly.png  (블록리게임 실행 화면)
- capture_tetris.png   (테트리스게임 실행 화면)

[작동 테스트]
- 로컬 실행(streamlit run app.py) 후 사이드바 Menu에서 두 메뉴를 선택하여
  메인 화면에 iframe(블록리게임/테트리스게임)이 표시되는 것을 확인함

[실행 방법]
pip install -r requirements.txt
streamlit run app.py
