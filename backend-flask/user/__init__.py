import os

from flask import Flask


def create_app(test_config=None):
	# 创建 Flask 实例
	# __name__ 是当前 Python 模块的名称
	# instance_relative_config=True 告诉应用配置文件是相对于 instance folder 的相对路径
	# 实例文件夹在 user 包的外面，用于存放本地数据（例如配置密钥和数据库）
	app = Flask(__name__, instance_relative_config=True)

	# 设置一个应用的缺省配置
	# SECRET_KEY 是被 Flask 和扩展用于保证数据安全的。开发过程可以设置为 'dev' ，发布时应当使用一个随机值重载
	# DATABASE SQLite 数据库文件存放在路径，位于 Flask 用于存放实例的 app.instance_path 之内
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'user.sqlite'),
	)

	# 如果 config.py 存在的话使用 config.py 中的值来重载缺省配置
	# test_config 也会被传递给工厂，并且会替代实例配置
	if test_config is None:
		# 不测试时加载实例配置（如果存在）
		app.config.from_pyfile('config.py', silent=True)
	else:
		# 如果传入，则加载测试配置
		app.config.from_mapping(test_config)

	# 确保 app.instance_path 存在
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# 一个简单的页面打招呼
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	return app
