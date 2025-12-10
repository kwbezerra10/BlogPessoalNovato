from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
from utils import verify_password
import models



#cria as tabelas
models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure os templates usando caminho absoluto também
templates = Jinja2Templates(directory='templates')

#-----------------Todos os GET-----------------#



# 🔵 GET /articles/new-article → Chama a pagina do formulario de artigo
@app.get("/articles/new-article")
def create_article_page (request: Request):    
    return templates.TemplateResponse("new-article.html", {"request": request})

# 🔵 GET /home → Chama a pagina home e mandas para o template todos os artigos
@app.get("/home")
def list_articles(request: Request, db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return templates.TemplateResponse("home.html", {"request": request, "articles": articles})


# 🔵 GET /admin -> Chama a pagina de login
@app.get("/admin")
def goto_admin_login(request: Request):    
    return templates.TemplateResponse("login.html", {"request": request})



## 🔵 GET /article/{id_article} -> Chama a pagina com o article completo
@app.get("/article/{id_article}")
def goto_article_complete(request: Request, id_article: int, db: Session=Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id_article).first()
    return templates.TemplateResponse("article.html", {"request": request, "article": article})

## 🔵 GET /edit/{id_article} -> Chama a pagina para edição do artigo
@app.get("/edit/{id_article}")
def goto_article_edit(request:Request, id_article: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id_article).first()
    return templates.TemplateResponse("edit.html", {"request": request, "article": article})



#-----------------Todos os POST-----------------#

# 🟢 POST /admin/logged -> valida usuario e redireciona para pagina de loggin.

@app.post("/admin/logged")
def goto_admin_page(request: Request, user: str=Form(), password: str=Form(), db: Session = Depends(get_db)):
    user_admin_object = db.query(models.User).filter(models.User.id == 1).first()
    
    USER_ADMIN = user_admin_object.username
    PASS_ADMIN = user_admin_object.password
    if user == USER_ADMIN and password == PASS_ADMIN:
        articles = db.query(models.Article).all()    
        return templates.TemplateResponse("admin.html", {"request": request, "articles": articles})
    else:
        RedirectResponse(url="/admin", status_code=303)



# 🟢 POST /articles -> Criar artigo
@app.post("/articles")
def create_article(title: str=Form(), content: str=Form(), db: Session = Depends(get_db)):
    db_article = models.Article(title=title, content=content) 

    db.add(db_article)
    db.commit()    
    
    return RedirectResponse(url="/admin", status_code=303)



# 🔴 POST /articles/{id} → deletar artigo
@app.post("/delete/{id_article}")
def delete_article(id_article: int, db: Session = Depends(get_db)):
    db_article = db.query(models.Article).filter(models.Article.id == id_article).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)



#-----------------Todos os PUT-----------------#

# 🟡 PUT /edit/{id} → atualizar artigo
@app.post("/edit/{id_article}")
def update_article(id_article: int, title: str=Form(), content: str=Form(), db : Session = Depends(get_db)):
    db_article = db.query(models.Article).filter(models.Article.id == id_article).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db_article.title   = title
    db_article.content = content
    db.commit()
    db.refresh(db_article)
    return RedirectResponse(url="/admin", status_code=303)

