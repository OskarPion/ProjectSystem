from app import create_app, celery

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
