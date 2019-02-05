from aquaurban import app, socketio

if __name__ == '__main__':
	socketio.run(app)


'''
publish(topico, mensagem)
subscribe(topico)

subscribe('teste')

publish('teste', 'sucesso')

def f (x):
	print(x)

'''