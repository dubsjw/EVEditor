IF NOT EXIST eveditor_env (
	virtualenv eveditor_env
	pip install -r requirements.txt
)

eveditor_env\\Scripts\\activate.bat