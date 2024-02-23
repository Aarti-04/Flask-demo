from flask import Flask,render_template,request,Response,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import delete
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
# Session=sessionmaker(bind=db)
# session=Session()
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable =False)
    desc=db.Column(db.String(300),nullable=False)
    complete=db.Column(db.Boolean)
    create_at=db.Column(db.DateTime,default=datetime.now())

    def __repr__(self) -> str:
        return f"{self.sno}- {self.title}"
@app.route("/create",methods=['GET','POST'])
def create_todo():
    # db.create_all()
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        completed=True if (request.form['completed'])=="True" else False
        todo=Todo(title=title,desc=desc,complete=completed)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    return render_template("index.html")
@app.route("/")
def show_todo():
    todo=Todo.query.all()
    print(todo)
    return render_template("index.html",todos=todo)
@app.route("/delete/<int:id>")
def delete_todo(id):
    id=id
    print(id)
    stmt = delete(Todo).where(Todo.sno==id)
    db.session.execute(stmt)
    # todo = Todo.query.get_or_404(id)
    # db.session.delete(todo)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:id>",methods=['GET','POST'])
def update_todo(id):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        completed=True if (request.form['completed'])=="True" else False
        db.session.query(Todo).filter(Todo.sno==id).update({"title":title,"desc":desc,"complete":completed},synchronize_session=False)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.get(id)
    return render_template("update.html",todo=todo)

if __name__=="__main__":
    app.run(debug=True)
